from datetime import datetime, timedelta
import streamlit as st
from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# ---------------------------------------------------------
# Step 2: Manage Application Memory (st.session_state)
# ---------------------------------------------------------
if "owner" not in st.session_state:
    # Initialize the default Owner object in session state
    st.session_state.owner = Owner(name="Jordan", email="jordan@example.com")

if "scheduler" not in st.session_state:
    # Initialize Scheduler linked directly to that persistent owner
    st.session_state.scheduler = Scheduler(owner=st.session_state.owner)

owner: Owner = st.session_state.owner
scheduler: Scheduler = st.session_state.scheduler

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ dashboard. Your front-end interface is now linked to your 
backend domain logic in `pawpal_system.py`.
"""
)

st.divider()

# ---------------------------------------------------------
# Step 3: Wire Pet Management
# ---------------------------------------------------------
st.subheader("1. Pet Registration")

col_p1, col_p2, col_p3 = st.columns(3)
with col_p1:
    owner_name_input = st.text_input("Owner Name", value=owner.name)
    if owner_name_input != owner.name:
        owner.name = owner_name_input

with col_p2:
    pet_name_input = st.text_input("Pet Name", value="Mochi")

with col_p3:
    species_input = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Register / Add Pet"):
    existing_pet = next((p for p in owner.pets if p.name.lower() == pet_name_input.strip().lower()), None)
    if existing_pet:
        st.info(f"'{pet_name_input.strip()}' is already registered to {owner.name}.")
    else:
        new_pet = Pet(
            name=pet_name_input.strip(),
            species=species_input,
            breed="Mixed",
            age=2
        )
        owner.add_pet(new_pet)
        st.success(f"Added {new_pet.name} to {owner.name}'s household!")

# Show currently registered pets
if owner.pets:
    pet_names = [f"{p.name} ({p.species})" for p in owner.pets]
    st.write(f"**Registered Pets:** {', '.join(pet_names)}")
else:
    st.info("No pets registered yet. Click 'Register / Add Pet' above.")

st.divider()

# ---------------------------------------------------------
# Step 3: Wire Task Creation to Pet Objects
# ---------------------------------------------------------
st.subheader("2. Schedule a Task")

if not owner.pets:
    st.warning("Please register at least one pet before creating tasks.")
else:
    # Select which pet this task belongs to
    pet_map = {p.name: p for p in owner.pets}
    selected_pet_name = st.selectbox("Assign Task To Pet", list(pet_map.keys()))
    selected_pet: Pet = pet_map[selected_pet_name]

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task Title", value="Morning walk")
    with col2:
        start_hour = st.number_input("Hour (24h format)", min_value=0, max_value=23, value=8)
    with col3:
        frequency = st.selectbox("Frequency", ["daily", "once", "weekly"])

    if st.button("Add Task to Pet"):
        now = datetime.now()
        due_time = now.replace(hour=int(start_hour), minute=0, second=0, microsecond=0)
        
        # Instantiate Task class and append to Pet's task list
        new_task = Task(
            description=task_title.strip(),
            due_datetime=due_time,
            frequency=frequency
        )
        selected_pet.add_task(new_task)
        st.success(f"Added task '{new_task.description}' to {selected_pet.name}!")

# Display all tasks currently stored in memory
all_tasks = owner.get_all_tasks()
if all_tasks:
    st.write(f"**Total Tasks in Memory ({len(all_tasks)}):**")
    task_rows = [
        {
            "Pet": pet.name,
            "Task": task.description,
            "Scheduled Time": task.due_datetime.strftime("%I:%M %p"),
            "Frequency": task.frequency,
            "Completed": task.is_completed,
        }
        for pet, task in all_tasks
    ]
    st.table(task_rows)
else:
    st.info("No tasks recorded yet.")

st.divider()

# ---------------------------------------------------------
# Step 3: Wire Scheduler Generation
# ---------------------------------------------------------
st.subheader("3. Build Today's Schedule")

if st.button("Generate Today's Schedule"):
    today_schedule = scheduler.get_today_schedule()
    
    if not today_schedule:
        st.warning("No tasks found scheduled for today.")
    else:
        st.success(f"Found {len(today_schedule)} tasks scheduled for today:")
        for pet, task in today_schedule:
            time_display = task.due_datetime.strftime("%I:%M %p")
            status_badge = "✅ Done" if task.is_completed else "⏳ Pending"
            st.markdown(f"- **{time_display}** — **{pet.name}**: {task.description} ({status_badge})")