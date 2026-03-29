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

    # Add at least three Tasks with different times
    task1 = Task(
        task_id="T001",
        pet_id=buddy_id,
        description="Morning Walk",
        due_date_time=time1,
        task_type="Walking"
    )
    
    task2 = Task(
        task_id="T002",
        pet_id=luna_id,
        description="Afternoon Feeding",
        due_date_time=time2,
        task_type="Feeding"
    )
    
    task3 = Task(
        task_id="T003",
        pet_id=buddy_id,
        description="Evening Walk and Play",
        due_date_time=time3,
        task_type="Activity"
    )

    # Insert tasks into the scheduler
    scheduler.tasks.extend([task1, task2, task3])

    # 4. Print "Today's Schedule" to the terminal
    print("\n=== Today's Schedule ===")
    schedule = scheduler.get_daily_schedule(today.date())
    
    # Check if there are tasks or appointments
    if not schedule['tasks'] and not schedule['appointments']:
        print("No tasks or appointments scheduled for today.")
    else:
        # Print all tasks
        for task in schedule['tasks']:
            # Find the pet name associated with the task
            pet_name = next((p.name for p in pets if p.pet_id == task.pet_id), "Unknown")
            status = task.get_status()
            print(f"[{task.due_date_time.strftime('%I:%M %p')}] {pet_name} - {task.task_type}: {task.description} ({status})")

if __name__ == "__main__":
    main()