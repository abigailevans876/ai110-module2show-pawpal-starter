from datetime import datetime
import streamlit as st
from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# ---------------------------------------------------------
# Step 2: Manage Application Memory (st.session_state)
# ---------------------------------------------------------
if "owner" not in st.session_state or not isinstance(st.session_state.owner, Owner):
    st.session_state.owner = Owner(name="Jordan", email="jordan@example.com")

# Recreate the service to avoid stale class instances after Streamlit hot reloads.
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
    cleaned_pet_name = pet_name_input.strip()
    existing_pet = next(
        (pet for pet in owner.pets if pet.name.casefold() == cleaned_pet_name.casefold()),
        None,
    )
    if not cleaned_pet_name:
        st.warning("Enter a pet name before registering.")
    elif existing_pet:
        st.info(f"'{cleaned_pet_name}' is already registered to {owner.name}.")
    else:
        new_pet = Pet(
            name=cleaned_pet_name,
            species=species_input,
            breed="Mixed",
            age=2,
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
    pet_map = {p.pet_id: p for p in owner.pets}
    selected_pet_id = st.selectbox(
        "Assign Task To Pet",
        list(pet_map),
        format_func=lambda pet_id: pet_map[pet_id].name,
    )
    selected_pet: Pet = pet_map[selected_pet_id]

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task Title", value="Morning walk")
    with col2:
        start_hour = st.number_input("Hour (24h format)", min_value=0, max_value=23, value=8)
    with col3:
        frequency = st.selectbox("Frequency", ["daily", "once", "weekly"])

    if st.button("Add Task to Pet"):
        cleaned_task_title = task_title.strip()
        if not cleaned_task_title:
            st.warning("Enter a task title before scheduling.")
        else:
            now = datetime.now()
            due_time = now.replace(
                hour=int(start_hour), minute=0, second=0, microsecond=0
            )
            new_task = Task(
                description=cleaned_task_title,
                due_datetime=due_time,
                frequency=frequency,
            )
            selected_pet.add_task(new_task)
            st.success(f"Added task '{new_task.description}' to {selected_pet.name}!")

# Display tasks through the scheduler's filtering and sorting methods
st.subheader("3. Browse Tasks")
filter_col1, filter_col2 = st.columns(2)
with filter_col1:
    status_filter = st.selectbox(
        "Completion status",
        ["All", "Pending", "Completed"],
    )
with filter_col2:
    pet_filter_options = {"All pets": None}
    pet_filter_options.update({pet.name: pet.name for pet in owner.pets})
    selected_pet_filter = st.selectbox("Pet", list(pet_filter_options))

completed_filter = {
    "All": None,
    "Pending": False,
    "Completed": True,
}[status_filter]
filtered_tasks = scheduler.filter_tasks(
    completed=completed_filter,
    pet_name=pet_filter_options[selected_pet_filter],
)
filtered_tasks = scheduler.sort_by_time(filtered_tasks)

if filtered_tasks:
    st.write(f"**Matching tasks ({len(filtered_tasks)}):**")
    task_rows = [
        {
            "Pet": pet.name,
            "Task": task.description,
            "Scheduled": task.due_datetime.strftime("%Y-%m-%d %I:%M %p"),
            "Frequency": task.frequency,
            "Status": "Completed" if task.is_completed else "Pending",
        }
        for pet, task in filtered_tasks
    ]
    st.table(task_rows)
else:
    st.info("No tasks match these filters.")

st.divider()

# Show today's schedule using Scheduler's date filtering and sorting.
st.subheader("4. Today's Schedule")
today_schedule = scheduler.get_today_schedule()
if today_schedule:
    st.success(f"Today's schedule has {len(today_schedule)} task(s), sorted by time.")
    today_rows = [
        {
            "Time": task.due_datetime.strftime("%I:%M %p"),
            "Pet": pet.name,
            "Task": task.description,
            "Status": "Completed" if task.is_completed else "Pending",
        }
        for pet, task in today_schedule
    ]
    st.table(today_rows)
else:
    st.info("No tasks are scheduled for today.")

st.divider()

# Show conflicts as actionable warnings rather than interrupting the schedule.
st.subheader("5. Schedule Conflicts")
conflicts = scheduler.find_conflicts()
if conflicts:
    for conflict in conflicts:
        st.warning(
            f"{conflict}. Consider rescheduling one task to a different time."
        )
    st.caption(
        "Warnings indicate exact date-and-time matches; task durations are not "
        "currently used to detect overlapping appointments."
    )
else:
    st.success("No exact-time conflicts found.")

st.divider()

# Completing a task uses Scheduler.complete_task so recurring tasks are created.
st.subheader("6. Complete a Task")
pending_tasks = scheduler.get_all_pending()
if pending_tasks:
    pending_by_id = {task.task_id: (pet, task) for pet, task in pending_tasks}
    selected_task_id = st.selectbox(
        "Select a pending task",
        list(pending_by_id),
        format_func=lambda task_id: (
            f"{pending_by_id[task_id][0].name} — "
            f"{pending_by_id[task_id][1].description} "
            f"({pending_by_id[task_id][1].due_datetime:%Y-%m-%d %I:%M %p})"
        ),
    )
    if st.button("Mark task complete"):
        pet, task = pending_by_id[selected_task_id]
        next_task = scheduler.complete_task(pet, task)
        if next_task:
            st.success(
                f"Completed '{task.description}'. Next {task.frequency} "
                f"occurrence: {next_task.due_datetime:%Y-%m-%d %I:%M %p}."
            )
        else:
            st.success(f"Completed '{task.description}'. This task does not recur.")
else:
    st.info("There are no pending tasks to complete.")

# Display the current task count after any scheduler actions.
all_tasks = scheduler.sort_by_time()
if all_tasks:
    st.caption(f"{len(all_tasks)} task(s) currently stored.")