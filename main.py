from datetime import datetime, date, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler

def main():
    # 1. Create an Owner
    owner = Owner(user_id="U001", name="Ryan")

    # 2. Create at least two Pets
    # The Owner.add_pet method takes a dictionary of pet_info
    owner.add_pet({
        "pet_id": "P001",
        "name": "Buddy",
        "species": "Dog",
        "age": 3,
        "weight": 30.5
    })
    
    owner.add_pet({
        "pet_id": "P002",
        "name": "Luna",
        "species": "Cat",
        "age": 2,
        "weight": 10.0
    })

    # Retrieve the pets created
    pets = owner.view_all_pets()
    buddy_id = pets[0].pet_id
    luna_id = pets[1].pet_id

    print(f"Created Owner: {owner.name}")
    for pet in pets:
        print(f" - Added Pet: {pet.get_details()}")

    # 3. Create a scheduler and tasks
    scheduler = Scheduler()

    # Create dates for today
    today = datetime.now()
    time1 = today.replace(hour=8, minute=0, second=0, microsecond=0)
    time2 = today.replace(hour=13, minute=0, second=0, microsecond=0)
    time3 = today.replace(hour=18, minute=30, second=0, microsecond=0)
    
    # Intentionally duplicate time3 for a conflict test
    time4 = time3

    # Add at least three Tasks with different times, intentionally inserted OUT OF ORDER
    task1 = Task(
        task_id="T001",
        pet_id=buddy_id,
        description="Evening Walk and Play",
        due_date_time=time3, # Late time
        task_type="Activity",
        frequency="Daily" # Note the recurring property
    )
    
    task2 = Task(
        task_id="T002",
        pet_id=luna_id,
        description="Morning Feeding",
        due_date_time=time1, # Early time
        task_type="Feeding"
    )
    
    task3 = Task(
        task_id="T003",
        pet_id=buddy_id,
        description="Afternoon Walk",
        due_date_time=time2, # Middle time
        task_type="Walking"
    )
    
    task4 = Task(
        task_id="T004",
        pet_id=luna_id,
        description="Evening Grooming (CONFLICT)",
        due_date_time=time4, # Same exact time as task1
        task_type="Grooming"
    )

    # Insert tasks into the scheduler raw
    scheduler.tasks.extend([task1, task2, task3, task4])

    print("\n=== Testing Sorting ===")
    sorted_tasks = scheduler.sort_tasks_by_time(scheduler.tasks)
    for t in sorted_tasks:
        print(f"[{t.due_date_time.strftime('%I:%M %p')}] {t.description}")
        
    print("\n=== Testing Conflict Detection ===")
    conflicts = scheduler.detect_conflicts()
    for warning in conflicts:
        print(f"⚠️  {warning}")
        
    print("\n=== Testing Recurring Automation ===")
    print("Marking the Daily 'Evening Walk and Play' as complete...")
    scheduler.complete_task("T001")
    
    # We should now see a new task added tomorrow!
    new_recurring_task = scheduler.tasks[-1]
    print(f"Total tasks in scheduler is now: {len(scheduler.tasks)}")
    print(f"Next iteration created for: {new_recurring_task.due_date_time.strftime('%Y-%m-%d %I:%M %p')}")

    # 4. Print "Today's Schedule" to the terminal
    print("\n=== Today's Schedule (Filtered for Pending Options) ===")
    pending_tasks_today = scheduler.filter_tasks(status="Pending")
    
    if not pending_tasks_today:
        print("No pending tasks scheduled for today.")
    else:
        # Print all tasks
        for task in scheduler.sort_tasks_by_time(pending_tasks_today):
            # Find the pet name associated with the task
            pet_name = next((p.name for p in pets if p.pet_id == task.pet_id), "Unknown")
            print(f"[{task.due_date_time.strftime('%I:%M %p')}] {pet_name} - {task.task_type}: {task.description}")

if __name__ == "__main__":
    main()