from datetime import date, datetime, time, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def test_mark_complete_changes_task_status():
    task = Task("Feed the dog", datetime.now())

    task.mark_complete()

    assert task.is_completed is True


def test_adding_task_increases_pet_task_count():
    pet = Pet(name="Luna", species="Dog", breed="Beagle", age=4)
    task = Task("Morning walk", datetime.now())
    initial_count = len(pet.tasks)

    pet.add_task(task)

    assert len(pet.tasks) == initial_count + 1


def make_pet(name: str) -> Pet:
    return Pet(name=name, species="Dog", breed="Beagle", age=4)


def test_sort_by_time_orders_tasks_chronologically():
    pet = make_pet("Luna")
    pet.add_task(Task("Evening walk", datetime(2026, 11, 1, 18, 0), "once"))
    pet.add_task(Task("Morning walk", datetime(2026, 11, 1, 8, 0), "once"))
    scheduler = Scheduler(Owner(name="Alex", email="alex@example.com", pets=[pet]))

    sorted_tasks = scheduler.sort_by_time()

    assert [task.description for _, task in sorted_tasks] == [
        "Morning walk",
        "Evening walk",
    ]


def test_filter_tasks_by_completion_and_pet_name():
    luna = make_pet("Luna")
    mittens = make_pet("Mittens")
    completed_task = Task("Breakfast", datetime(2026, 11, 1, 8, 0), "once")
    completed_task.mark_complete()
    luna.add_task(completed_task)
    luna.add_task(Task("Evening walk", datetime(2026, 11, 1, 18, 0), "once"))
    mittens.add_task(Task("Dinner", datetime(2026, 11, 1, 19, 0), "once"))
    scheduler = Scheduler(
        Owner(name="Alex", email="alex@example.com", pets=[luna, mittens])
    )

    filtered_tasks = scheduler.filter_tasks(completed=False, pet_name="lUnA")

    assert [(pet.name, task.description) for pet, task in filtered_tasks] == [
        ("Luna", "Evening walk")
    ]


def test_scheduler_handles_pet_with_no_tasks():
    pet = make_pet("Luna")
    scheduler = Scheduler(Owner(name="Alex", email="alex@example.com", pets=[pet]))

    assert scheduler.sort_by_time() == []
    assert scheduler.filter_tasks() == []
    assert scheduler.find_conflicts() == []


def test_completing_daily_task_creates_occurrence_tomorrow_at_same_time():
    pet = make_pet("Luna")
    task = Task("Morning walk", datetime(2020, 1, 1, 8, 30))
    pet.add_task(task)
    scheduler = Scheduler(Owner(name="Alex", email="alex@example.com", pets=[pet]))

    next_task = scheduler.complete_task(pet, task)

    assert task.is_completed
    assert next_task is not None
    assert next_task.due_datetime.date() == date.today() + timedelta(days=1)
    assert next_task.due_datetime.time() == time(8, 30)
    assert next_task.frequency == task.frequency
    assert next_task in pet.tasks


def test_completing_weekly_task_creates_next_week_occurrence():
    pet = make_pet("Luna")
    task = Task("Grooming", datetime(2026, 11, 1, 9, 0), "weekly")
    scheduler = Scheduler(Owner(name="Alex", email="alex@example.com", pets=[pet]))

    next_task = scheduler.complete_task(pet, task)

    assert next_task is not None
    assert next_task.due_datetime == task.due_datetime + timedelta(weeks=1)


def test_completing_once_task_does_not_create_an_occurrence():
    pet = make_pet("Luna")
    task = Task("Vet appointment", datetime(2026, 11, 1, 10, 0), "once")
    scheduler = Scheduler(Owner(name="Alex", email="alex@example.com", pets=[pet]))

    next_task = scheduler.complete_task(pet, task)

    assert task.is_completed
    assert next_task is None
    assert pet.tasks == []


def test_find_conflicts_reports_tasks_at_the_same_time():
    luna = make_pet("Luna")
    mittens = make_pet("Mittens")
    same_time = datetime(2026, 11, 1, 8, 0)
    luna.add_task(Task("Morning walk", same_time, "once"))
    mittens.add_task(Task("Breakfast", same_time, "once"))
    scheduler = Scheduler(
        Owner(name="Alex", email="alex@example.com", pets=[luna, mittens])
    )

    warnings = scheduler.find_conflicts()

    assert len(warnings) == 1
    assert "2026-11-01 at 08:00 AM" in warnings[0]
    assert "Luna — Morning walk" in warnings[0]
    assert "Mittens — Breakfast" in warnings[0]


def test_find_conflicts_returns_no_warnings_for_different_times():
    pet = make_pet("Luna")
    pet.add_task(Task("Morning walk", datetime(2026, 11, 1, 8, 0), "once"))
    pet.add_task(Task("Evening walk", datetime(2026, 11, 1, 18, 0), "once"))
    scheduler = Scheduler(Owner(name="Alex", email="alex@example.com", pets=[pet]))

    assert scheduler.find_conflicts() == []