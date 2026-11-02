from datetime import date, datetime, time

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    owner = Owner(name="Alex", email="alex@example.com")
    luna = Pet(name="Luna", species="Dog", breed="Beagle", age=4)
    mittens = Pet(name="Mittens", species="Cat", breed="Tabby", age=2)
    owner.add_pet(luna)
    owner.add_pet(mittens)

    today = date.today()

    # Added out of time order; two tasks share the same time to demonstrate conflict detection.
    luna.add_task(Task("Evening walk", datetime.combine(today, time(18, 0))))
    mittens.add_task(Task("Breakfast", datetime.combine(today, time(8, 0))))
    luna.add_task(Task("Morning walk", datetime.combine(today, time(8, 0))))

    scheduler = Scheduler(owner)

    print("Today's Schedule (sorted)")
    for pet, task in scheduler.get_today_schedule():
        print(f"{task.due_datetime:%I:%M %p} — {pet.name}: {task.description}")

    print("\nLuna's pending tasks")
    for pet, task in scheduler.filter_tasks(completed=False, pet_name="Luna"):
        print(f"{pet.name}: {task.description}")

    print("\nConflict warnings")
    for warning in scheduler.find_conflicts():
        print(f"Warning: {warning}")

    completed_task = luna.tasks[0]
    next_task = scheduler.complete_task(luna, completed_task)
    if next_task:
        print(
            f"\nRecurring task created: {next_task.description} "
            f"({next_task.due_datetime:%Y-%m-%d %I:%M %p})"
        )


if __name__ == "__main__":
    main()