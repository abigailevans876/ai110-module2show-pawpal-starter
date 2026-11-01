"""
pawpal_system.py
Domain logic layer for PawPal+.
Encapsulates Task, Pet, Owner, and Scheduler classes with clean method contracts.
"""

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import List, Optional
import uuid


@dataclass
class Task:
    """Represents a single pet care activity."""
    description: str
    due_datetime: datetime
    frequency: str = "daily"  # e.g., 'once', 'daily', 'weekly'
    is_completed: bool = False
    task_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])

    def mark_complete(self) -> None:
        """Marks the task as completed."""
        self.is_completed = True

    def mark_pending(self) -> None:
        """Reverts the task status back to pending."""
        self.is_completed = False


@dataclass
class Pet:
    """Stores pet attributes and an internal list of scheduled tasks."""
    name: str
    species: str
    breed: str
    age: int
    notes: str = ""
    tasks: List[Task] = field(default_factory=list)
    pet_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])

    def add_task(self, task: Task) -> None:
        """Appends a new care task to the pet's schedule."""
        self.tasks.append(task)

    def get_pending_tasks(self) -> List[Task]:
        """Returns all uncompleted tasks for this pet."""
        return [task for task in self.tasks if not task.is_completed]

    def get_summary(self) -> str:
        """Returns a formatted one-line overview of the pet."""
        return f"{self.name} ({self.species}, {self.breed}, {self.age} yrs)"


@dataclass
class Owner:
    """Manages registered pets and provides unified access to their activities."""
    name: str
    email: str
    owner_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Adds a pet to the owner's household."""
        self.pets.append(pet)

    def get_pet_by_id(self, pet_id: str) -> Optional[Pet]:
        """Finds and returns a pet matching the given ID."""
        for pet in self.pets:
            if pet.pet_id == pet_id:
                return pet
        return None

    def get_all_tasks(self) -> List[tuple[Pet, Task]]:
        """Collects every task across all registered pets paired with its pet."""
        all_tasks: List[tuple[Pet, Task]] = []
        for pet in self.pets:
            for task in pet.tasks:
                all_tasks.append((pet, task))
        return all_tasks


class Scheduler:
    """The central coordinator that retrieves, filters, and formats tasks across pets."""

    def __init__(self, owner: Owner) -> None:
        """Initializes the scheduler bound to a specific pet owner."""
        self.owner = owner

    def get_schedule_for_date(self, target_date: date) -> List[tuple[Pet, Task]]:
        """Retrieves and sorts all tasks due on the target date."""
        matched = [
            (pet, task)
            for pet, task in self.owner.get_all_tasks()
            if task.due_datetime.date() == target_date
        ]
        # Sort chronologically by due time
        return sorted(matched, key=lambda pair: pair[1].due_datetime)

    def get_today_schedule(self) -> List[tuple[Pet, Task]]:
        """Retrieves and sorts all tasks due today."""
        return self.get_schedule_for_date(datetime.now().date())

    def get_all_pending(self) -> List[tuple[Pet, Task]]:
        """Retrieves all incomplete tasks across all pets."""
        return [
            (pet, task)
            for pet, task in self.owner.get_all_tasks()
            if not task.is_completed
        ]


__all__ = ["Owner", "Pet", "Scheduler", "Task"]