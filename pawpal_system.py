"""Domain logic for PawPal+."""

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import List, Optional
import uuid


@dataclass
class Task:
    """Represent a pet care activity."""
    description: str
    due_datetime: datetime
    frequency: str = "daily"
    is_completed: bool = False
    task_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.is_completed = True

    def mark_pending(self) -> None:
        """Mark this task as pending."""
        self.is_completed = False


@dataclass
class Pet:
    """Store a pet's details and scheduled tasks."""
    name: str
    species: str
    breed: str
    age: int
    notes: str = ""
    tasks: List[Task] = field(default_factory=list)
    pet_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's schedule."""
        self.tasks.append(task)

    def get_pending_tasks(self) -> List[Task]:
        """Return this pet's incomplete tasks."""
        return [task for task in self.tasks if not task.is_completed]

    def get_summary(self) -> str:
        """Return a short summary of this pet."""
        return f"{self.name} ({self.species}, {self.breed}, {self.age} yrs)"


@dataclass
class Owner:
    """Manage an owner's pets and their tasks."""
    name: str
    email: str
    owner_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's household."""
        self.pets.append(pet)

    def get_pet_by_id(self, pet_id: str) -> Optional[Pet]:
        """Find a pet by its ID."""
        return next((pet for pet in self.pets if pet.pet_id == pet_id), None)

    def get_all_tasks(self) -> List[tuple[Pet, Task]]:
        """Return all tasks paired with their pets."""
        return [(pet, task) for pet in self.pets for task in pet.tasks]


class Scheduler:
    """Sort, filter, and coordinate tasks for an owner."""

    def __init__(self, owner: Owner) -> None:
        """Create a scheduler for an owner."""
        self.owner = owner

    def sort_by_time(
        self, tasks: Optional[List[tuple[Pet, Task]]] = None
    ) -> List[tuple[Pet, Task]]:
        """Return tasks sorted by their due date and time."""
        tasks_to_sort = tasks if tasks is not None else self.owner.get_all_tasks()
        return sorted(tasks_to_sort, key=lambda pair: pair[1].due_datetime)

    def filter_tasks(
        self,
        completed: Optional[bool] = None,
        pet_name: Optional[str] = None,
    ) -> List[tuple[Pet, Task]]:
        """Filter tasks by completion status and/or pet name."""
        return [
            (pet, task)
            for pet, task in self.owner.get_all_tasks()
            if (completed is None or task.is_completed == completed)
            and (pet_name is None or pet.name.casefold() == pet_name.casefold())
        ]

    def get_schedule_for_date(self, target_date: date) -> List[tuple[Pet, Task]]:
        """Return tasks due on a date, sorted by time."""
        tasks = [
            (pet, task)
            for pet, task in self.owner.get_all_tasks()
            if task.due_datetime.date() == target_date
        ]
        return self.sort_by_time(tasks)

    def get_today_schedule(self) -> List[tuple[Pet, Task]]:
        """Return today's tasks, sorted by time."""
        return self.get_schedule_for_date(datetime.now().date())

    def get_all_pending(self) -> List[tuple[Pet, Task]]:
        """Return all incomplete tasks."""
        return self.filter_tasks(completed=False)

    def complete_task(self, pet: Pet, task: Task) -> Optional[Task]:
        """Complete a task and add its next daily or weekly occurrence."""
        task.mark_complete()

        if task.frequency == "daily":
            next_due = datetime.combine(
                datetime.now().date() + timedelta(days=1),
                task.due_datetime.time(),
            )
        elif task.frequency == "weekly":
            next_due = task.due_datetime + timedelta(weeks=1)
        else:
            return None

        next_task = Task(
            description=task.description,
            due_datetime=next_due,
            frequency=task.frequency,
        )
        pet.add_task(next_task)
        return next_task

    def find_conflicts(self) -> List[str]:
        """Return warnings for tasks scheduled at exactly the same time."""
        tasks = self.sort_by_time()
        warnings = []

        for index, (pet, task) in enumerate(tasks):
            for other_pet, other_task in tasks[index + 1:]:
                if other_task.due_datetime != task.due_datetime:
                    break
                warnings.append(
                    f"Conflict at {task.due_datetime:%I:%M %p}: "
                    f"{pet.name} — {task.description} and "
                    f"{other_pet.name} — {other_task.description}"
                )

        return warnings


__all__ = ["Owner", "Pet", "Scheduler", "Task"]