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
    pet1_tasks = scheduler.filter_tasks("P001")
    pet2_tasks = scheduler.filter_tasks("P002")

    # Assert correct counts for each pet
    assert len(pet1_tasks) == 2
    assert len(pet2_tasks) == 1

def test_sorting_correctness():
    """Verify tasks are returned in chronological order."""
    scheduler = Scheduler()
    now = datetime.now()
    
    # Create tasks explicitly out of order
    task_late = Task(task_id="T001", pet_id="P001", description="Late", due_date_time=now + timedelta(hours=5), task_type="Activity")
    task_early = Task(task_id="T002", pet_id="P001", description="Early", due_date_time=now + timedelta(hours=1), task_type="Activity")
    task_mid = Task(task_id="T003", pet_id="P001", description="Mid", due_date_time=now + timedelta(hours=3), task_type="Activity")
    
    expected_order = [task_early, task_mid, task_late]
    scheduler.tasks.extend([task_late, task_early, task_mid])
    
    # Sort and verify order matches exactly
    sorted_tasks = scheduler.sort_tasks_by_time(scheduler.tasks)
    assert sorted_tasks == expected_order

def test_recurrence_logic():
    """Confirm that marking a daily task complete creates a new task for the following day."""
    scheduler = Scheduler()
    now = datetime.now()
    
    task1 = Task(
        task_id="T001", 
        pet_id="P001", 
        description="Daily Meds", 
        due_date_time=now, 
        task_type="Meds",
        frequency="Daily"
    )
    scheduler.tasks.append(task1)
    
    # Mark it complete using the new Scheduler-level function that creates recurring tasks natively
    scheduler.complete_task("T001")
    
    # Verify a clone has been pushed to the stack
    assert len(scheduler.tasks) == 2
    
    # Select the new object and verify date math
    new_task = scheduler.tasks[-1]
    assert new_task.is_completed == False
    assert new_task.task_id != "T001" # It generated a new UUID
    assert new_task.description == "Daily Meds"
    
    # Ensure interval math was precisely +1 days to the minute
    expected_new_date = (now + timedelta(days=1))
    assert new_task.due_date_time == expected_new_date

def test_conflict_detection():
    """Verify that the Scheduler flags duplicate times."""
    scheduler = Scheduler()
    conflict_time = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
    
    # Schedule two tasks at the exact same time
    task1 = Task(task_id="T001", pet_id="P001", description="Clashing Event A", due_date_time=conflict_time, task_type="Activity")
    task2 = Task(task_id="T002", pet_id="P002", description="Clashing Event B", due_date_time=conflict_time, task_type="Activity")
    task3 = Task(task_id="T003", pet_id="P001", description="Safe Event", due_date_time=conflict_time + timedelta(hours=3), task_type="Activity")
    
    scheduler.tasks.extend([task1, task2, task3])
    
    conflicts = scheduler.detect_conflicts()
    
    assert len(conflicts) == 1
    # Ensure warnings string output mentions both items by inspecting output contents
    assert "Clashing Event A" in conflicts[0]
    assert "Clashing Event B" in conflicts[0]
