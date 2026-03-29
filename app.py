import streamlit as st
import uuid
from datetime import datetime, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler, Appointment

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

# --- Step 2: Manage the Application "Memory" ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner(user_id="U001", name="Jordan")

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()

st.subheader("1. Manage Pets")
owner_name = st.text_input("Owner name", value=st.session_state.owner.name)
if owner_name != st.session_state.owner.name:
    st.session_state.owner.name = owner_name

col_pet_name, col_species, col_age, col_weight = st.columns(4)
with col_pet_name:
    pet_name = st.text_input("Pet name", value="Mochi")
with col_species:
    species = st.selectbox("Species", ["Dog", "Cat", "Other"])
with col_age:
    age = st.number_input("Age", min_value=0, value=2)
with col_weight:
    weight = st.number_input("Weight (lbs)", min_value=0.0, value=12.5)

# --- Step 3: Wiring UI Actions to Logic (Add Pet) ---
if st.button("Add Pet"):
    pet_id = f"P_{str(uuid.uuid4())[:6]}"
    st.session_state.owner.add_pet({
        "pet_id": pet_id,
        "name": pet_name,
        "species": species,
        "age": age,
        "weight": weight
    })
    st.success(f"Added {pet_name} to your pets!")

st.markdown("**Your Current Pets:**")
if st.session_state.owner.view_all_pets():
    for pet in st.session_state.owner.view_all_pets():
        st.write(f"- {pet.get_details()} (ID: {pet.pet_id})")
else:
    st.info("No pets added yet.")

st.divider()

st.markdown("### 2. Schedule Tasks")
st.caption("Add a few tasks and tie them to a specific pet.")

all_pets = st.session_state.owner.view_all_pets()

if not all_pets:
    st.warning("Please add a pet above before scheduling tasks!")
else:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        task_title = st.text_input("Task description", value="Morning walk")
    with col2:
        task_type = st.selectbox("Type", ["Walking", "Feeding", "Medication", "Grooming", "Other"])
    with col3:
        # Create a dropdown mapping pet names to IDs
        pet_options = {pet.name: pet.pet_id for pet in all_pets}
        selected_pet_name = st.selectbox("Which Pet?", list(pet_options.keys()))
        selected_pet_id = pet_options[selected_pet_name]
    with col4:
        # Add hours to current time for simplicity in UI
        time_offset = st.number_input("Hours from now", min_value=-24, max_value=72, value=1)
    
    # --- Step 3: Wiring UI Actions to Logic (Add Task) ---
    if st.button("Add Task"):
        task_id = f"T_{str(uuid.uuid4())[:6]}"
        due_time = datetime.now() + timedelta(hours=time_offset)
        
        new_task = Task(
            task_id=task_id,
            pet_id=selected_pet_id,
            description=task_title,
            due_date_time=due_time,
            task_type=task_type
        )
        st.session_state.scheduler.tasks.append(new_task)
        st.success(f"Added task: {task_title} for {selected_pet_name}")

if st.session_state.scheduler.tasks:
    st.write("**Current Tasks:**")
    for t in st.session_state.scheduler.tasks:
        target_pet = next((p.name for p in all_pets if p.pet_id == t.pet_id), "Unknown")
        st.write(f"- **{t.task_type}**: {t.description} (*{target_pet}*) - Due: {t.due_date_time.strftime('%b %d %I:%M %p')} - Status: {t.get_status()}")
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("3. Today's Schedule")

if st.button("View Today's Plan"):
    today = datetime.now().date()
    schedule = st.session_state.scheduler.get_daily_schedule(today)
    
    st.write(f"### Plan for {today.strftime('%B %d, %Y')}")
    
    tasks_today = schedule["tasks"]
    if not tasks_today:
        st.write("No tasks scheduled for today.")
    else:
        for t in tasks_today:
            target_pet = next((p.name for p in all_pets if p.pet_id == t.pet_id), "Unknown")
            st.write(f"- ⏳ [{t.due_date_time.strftime('%I:%M %p')}] {target_pet} ({t.task_type}): {t.description} - {t.get_status()}")
