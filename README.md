# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

Today's Schedule
08:00 AM — Luna: Morning walk
08:00 AM — Mittens: Breakfast
06:00 PM — Luna: Evening walk

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## Smarter Scheduling

| Feature | Method(s) | Behavior |
|---------|-----------|----------|
| Task sorting | `Scheduler.sort_by_time()` | Returns tasks ordered chronologically by their `due_datetime`. |
| Filtering | `Scheduler.filter_tasks()` | Filters across all pets by completion status, pet name, or both. Pet names are compared without case sensitivity. |
| Conflict detection | `Scheduler.find_conflicts()` | Returns warning strings for any pair of tasks with the exact same date and time, including tasks belonging to different pets. It does not raise an exception or check overlapping durations. |
| Recurring tasks | `Scheduler.complete_task()` | Marks a task complete and creates its next occurrence tomorrow at the same time for `daily` tasks or one week after the scheduled date for `weekly` tasks. `once` tasks do not recur. |

`Scheduler.get_schedule_for_date()` and `Scheduler.get_today_schedule()` use the sorting method to return chronological schedules. The `main.py` terminal demo adds tasks out of order, prints filtered tasks, displays conflict warnings, and demonstrates a recurring task.

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. Run `python main.py` to see the terminal scheduling demo.
2. Review the chronologically sorted schedule, despite the tasks being added out of order.
3. Check the pending tasks filtered for Luna.
4. See the warning for Luna and Mittens' tasks scheduled at the same time.
5. See the next occurrence printed after a daily task is completed.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
