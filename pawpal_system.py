from dataclasses import dataclass, field
from typing import List, Dict, Any
from datetime import datetime, date

@dataclass
class Pet:
    pet_id: str
    name: str
    species: str
    age: int
    weight: float

    def update_info(self, updates: Dict[str, Any]) -> None:
        """Updates the pet's attributes dynamically based on a dictionary."""
        for key, value in updates.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def get_details(self) -> str:
        """Returns a formatted summary of the pet."""
        return f"{self.name} ({self.species}) - Age: {self.age}, Weight: {self.weight}lbs"

@dataclass
class Appointment:
    appointment_id: str
    pet_id: str
    vet_name: str
    location: str
    date_time: datetime
    reason: str
    is_cancelled: bool = False

    def schedule(self, date_time: datetime, details: str) -> None:
        """Sets a new initial date and detail for the appointment."""
        self.date_time = date_time
        self.reason = details
        self.is_cancelled = False

    def reschedule(self, new_date_time: datetime) -> None:
        """Moves the appointment to a different time."""
        self.date_time = new_date_time

    def cancel(self) -> None:
        """Marks this appointment as cancelled."""
        self.is_cancelled = True

@dataclass
class Task:
    task_id: str
    pet_id: str
    description: str
    due_date_time: datetime
    task_type: str
    is_completed: bool = False

    def mark_completed(self) -> None:
        """Marks the task as completed."""
        self.is_completed = True

    def edit_task(self, new_details: Dict[str, Any]) -> None:
        """Edits task properties such as description or due date."""
        for key, value in new_details.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def get_status(self) -> str:
        """Calculates task status based on whether it's completed or overdue."""
        if self.is_completed:
            return "Completed"
        if datetime.now() > self.due_date_time:
            return "Overdue"
        return "Pending"

class Owner:
    def __init__(self, user_id: str, name: str):
        """Initializes an Owner with a user ID, name, and an empty list of pets."""
        self.user_id = user_id
        self.name = name
        self.pets: List[Pet] = []

    def add_pet(self, pet_info: Dict[str, Any]) -> None:
        """Instantiates a Pet object and adds it to the user's pet list."""
        new_pet = Pet(**pet_info)
        self.pets.append(new_pet)

    def remove_pet(self, pet_id: str) -> None:
        """Removes a pet by its pet_id."""
        self.pets = [pet for pet in self.pets if pet.pet_id != pet_id]

    def view_all_pets(self) -> List[Pet]:
        """Returns the list of all pets managed by the user."""
        return self.pets

class Scheduler:
    def __init__(self):
        """Initializes a Scheduler with empty lists for tracking tasks and appointments."""
        self.tasks: List[Task] = []
        self.appointments: List[Appointment] = []

    def get_daily_schedule(self, target_date: date) -> Dict[str, List[Any]]:
        """Returns all uncancelled appointments and tasks scheduled for a specified date."""
        daily_tasks = [t for t in self.tasks if t.due_date_time.date() == target_date]
        daily_appts = [a for a in self.appointments if a.date_time.date() == target_date and not a.is_cancelled]
        return {
            "tasks": daily_tasks,
            "appointments": daily_appts
        }

    def get_upcoming_activities(self) -> List[Any]:
        """Gathers and sorts all pending tasks and future uncancelled appointments by date-time."""
        now = datetime.now()
        upcoming_tasks = [t for t in self.tasks if t.due_date_time > now and not t.is_completed]
        upcoming_appts = [a for a in self.appointments if a.date_time > now and not a.is_cancelled]
        all_activities = upcoming_tasks + upcoming_appts
        # Sort based on the appropriate datetime attribute dynamically
        return sorted(all_activities, key=lambda act: act.due_date_time if hasattr(act, 'due_date_time') else act.date_time)

    def filter_by_pet(self, pet_id: str) -> Dict[str, List[Any]]:
        """Returns all tasks and appointments targeted to a specific pet_id."""
        pet_tasks = [t for t in self.tasks if t.pet_id == pet_id]
        pet_appts = [a for a in self.appointments if a.pet_id == pet_id]
        return {
            "tasks": pet_tasks,
            "appointments": pet_appts
        }
