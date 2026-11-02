# PawPal+

PawPal+ is a simple pet-care scheduler with a Python domain model and a Streamlit interface. It helps an owner keep track of tasks, view schedules, and receive warnings when tasks have an exact date-and-time conflict.

## Features

- Register pets and assign daily, weekly, or one-time care tasks.
- Browse tasks by pet and completion status.
- View a date's tasks in chronological order.
- Mark tasks complete; daily and weekly tasks automatically create their next occurrence.
- Show actionable warnings when two tasks have the exact same date and time.

## Run the application

Install the requirements in a virtual environment, then launch the Streamlit UI:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

The UI lets an owner register pets, schedule tasks for today, filter the task list, review today's schedule, inspect conflicts, and complete pending tasks.

## Smarter Scheduling

| Feature | Method | Behavior |
|---------|--------|----------|
| Time sorting | `Scheduler.sort_by_time()` | Orders tasks chronologically by due date and time. |
| Filtering | `Scheduler.filter_tasks()` | Filters all tasks by completion state, pet name, or both. Pet-name matching is case-insensitive. |
| Date schedule | `Scheduler.get_schedule_for_date()` | Selects tasks for a date and returns them in chronological order. |
| Recurring tasks | `Scheduler.complete_task()` | Marks a task complete and creates its next occurrence for tomorrow at the same time (daily), one week later (weekly), or no new task (once). |
| Conflict detection | `Scheduler.find_conflicts()` | Returns warning messages when tasks share an exact date and time, including tasks for different pets. It does not check overlapping durations. |

## Demo Walkthrough

Run the command-line demonstration with `python main.py`. It adds tasks out of order, prints today's schedule in chronological order, filters Luna's pending tasks, reports an exact-time conflict, and completes a recurring task. The Streamlit UI exposes the same scheduler features with tables and warning messages.

Example CLI output from a successful run:

```text
Today's Schedule (sorted)
08:00 AM — Luna: Morning walk
08:00 AM — Mittens: Breakfast
06:00 PM — Luna: Evening walk

Luna's pending tasks
Luna: Evening walk
Luna: Morning walk

Conflict warnings
Warning: Conflict on 2026-11-01 at 08:00 AM: Luna — Morning walk and Mittens — Breakfast

Recurring task created: Evening walk (2026-11-02 06:00 PM)
```

## Testing PawPal+

Run the automated test suite with:

```bash
python -m pytest
```

The tests cover task creation and completion, chronological sorting, filtering by pet and status, empty schedules, daily and weekly recurrence, one-time tasks, and exact-time conflict warnings.

Successful test run:

```text
============================= test session starts ==============================
platform darwin -- Python 3.13.7, pytest-9.2.0, pluggy-1.7.0
rootdir: /Users/abigailevans/ai110-module2show-pawpal-starter
plugins: anyio-4.16.0
collected 10 items

test_pawpal.py ..........                                                [100%]

============================== 10 passed in 0.04s ==============================
```

**Confidence level:** ★★★★☆ (4/5). The focused suite verifies the core scheduling behaviors, but does not cover every date/time edge case or exercise the Streamlit UI end to end.

The final class relationships and scheduler methods are shown in [uml_final.mmd](uml_final.mmd).
