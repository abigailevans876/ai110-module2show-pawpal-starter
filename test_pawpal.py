from datetime import datetime

from pawpal_system import Pet, Task


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