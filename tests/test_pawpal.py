import pytest
from datetime import datetime, timedelta
from pawpal_system import Pet, Task, Scheduler

def test_task_completion():
    """Verify that calling mark_completed() actually changes the task's status."""
    task = Task(
        task_id="T001",
        pet_id="P001",
        description="Morning Walk",
        due_date_time=datetime.now() + timedelta(hours=1),
        task_type="Walking"
    )
    
    # Status should initially be Pending (or Overdue if due_date_time is past, but we used a future time)
    assert task.get_status() == "Pending"
    assert not task.is_completed

    # Mark as complete
    task.mark_completed()

    # Verify status changed
    assert task.is_completed
    assert task.get_status() == "Completed"

def test_task_addition_to_scheduler():
    """Verify that adding a task to the scheduler increases the task count for that pet."""
    scheduler = Scheduler()
    
    # Initially no tasks
    assert len(scheduler.tasks) == 0
    
    # Add tasks
    task1 = Task(task_id="T001", pet_id="P001", description="Feed", due_date_time=datetime.now(), task_type="Food")
    task2 = Task(task_id="T002", pet_id="P002", description="Walk", due_date_time=datetime.now(), task_type="Activity")
    task3 = Task(task_id="T003", pet_id="P001", description="Medication", due_date_time=datetime.now(), task_type="Meds")
    
    scheduler.tasks.extend([task1, task2, task3])

    # Filter by specific pet
    pet1_tasks = scheduler.filter_by_pet("P001")["tasks"]
    pet2_tasks = scheduler.filter_by_pet("P002")["tasks"]

    # Assert correct counts for each pet
    assert len(pet1_tasks) == 2
    assert len(pet2_tasks) == 1
