from datetime import date, datetime, time

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    owner = Owner(name="Alex", email="alex@example.com")

    luna = Pet(name="Luna", species="Dog", breed="Beagle", age=4)
    mittens = Pet(name="Mittens", species="Cat", breed="Tabby", age=2)
    owner.add_pet(luna)
    owner.add_pet(mittens)

    today = date.today()
    luna.add_task(Task("Morning walk", datetime.combine(today, time(8, 0))))
    mittens.add_task(Task("Breakfast", datetime.combine(today, time(8, 30))))
    luna.add_task(Task("Evening walk", datetime.combine(today, time(18, 0))))

    scheduler = Scheduler(owner)
    print("Today's Schedule")
    for pet, task in scheduler.get_today_schedule():
        print(f"{task.due_datetime:%I:%M %p} — {pet.name}: {task.description}")


if __name__ == "__main__":
    main()