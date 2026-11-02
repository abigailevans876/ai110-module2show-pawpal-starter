# PawPal+ Project Reflection

## 1. System Design
### Core Actions
1. **Add & Manage Pets:** Register pets with vital statistics (species, breed, age) and special care notes.
2. **Schedule Daily Tasks:** Set time-stamped care obligations (walks, medication, feedings) tied directly to a specific pet.
3. **Daily Agenda Tracking:** Filter and view all tasks due on the current day, with the ability to mark them completed.

**a. Initial design**

The initial UML separated the `Owner`, `Pet`, and `Task` data models from a `Scheduler` service. In the final design, `Owner` owns a list of pets; each `Pet` stores its own task list; `Scheduler` holds an `Owner` reference and queries the owner's pets and tasks to sort, filter, build schedules, complete recurring tasks, and find conflicts. `Task` stores description, due date/time, recurrence frequency, and completion state. The final diagram in `diagrams/uml_final.mmd` reflects these relationships and methods.

**b. Design changes**

The design stayed with pet-owned tasks rather than moving every task into a separate scheduler-owned collection. This keeps the relationship intuitive while the scheduler can still perform household-wide queries through `Owner.get_all_tasks()`. During review, daily recurrence was clarified to mean tomorrow at the same time, based on the current date; it no longer depends on a stale task date.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers each task's due date and time, pet, completion state, and recurrence frequency. It sorts by due datetime, filters by pet and completion, and warns about exact date-and-time matches. It does not model task duration, priority, owner availability, or preferences, so it is a task organizer rather than an optimizer. Exact-time ordering and conflicts are the most important constraints in this first implementation because task duration and priority are not fields in the current `Task` model.

**b. Tradeoffs**

The scheduler detects conflicts only when two tasks have the exact same due date and time; it does not calculate whether tasks with durations overlap. This keeps conflict detection lightweight and gives the owner a useful warning without requiring duration data, but it can miss tasks that are scheduled close together and would overlap in practice. For this simple scheduler, exact-time matching is a clear first step.

---

## 3. AI Collaboration

**a. How you used AI**

AI chat was most useful for exploring the `sorted()` key and `timedelta` recurrence patterns, drafting focused tests, reviewing edge cases, and iterating on UI and documentation. Keeping each phase's work focused on a distinct goal helped separate implementation, verification, and final-polish questions; documenting phase outcomes also made it easier to carry decisions forward.

**b. Judgment and verification**

One suggestion I modified during review was to calculate a daily task's next date by adding one day to its previous due datetime. That can leave a stale or overdue task in the past, so I aligned recurrence with the requirement to schedule for tomorrow and preserve the original time. I kept the readable `sorted(..., key=lambda ...)` approach rather than replacing it with a more manual sorting loop. I checked the behavior with automated tests and the CLI demo.

---

## 4. Testing and Verification

**a. What you tested**

The 10 tests cover task completion and addition, chronological sorting, case-insensitive pet/status filtering, empty schedules, daily and weekly recurrence, one-time tasks, and both matching-time and non-conflicting schedules. These checks cover the main algorithms and protect key edge cases, such as a pet with no tasks and a task that should not recur.

**b. Confidence**

I have good but not exhaustive confidence: all 10 automated tests pass, and the CLI example exercises the main flows. I would next test date boundaries, timezone-aware datetimes, duplicate names, and the Streamlit interaction paths with automated UI tests.

---

## 5. Reflection

**a. What went well**

The scheduler methods are small and focused, and the demo and UI call into that shared logic rather than reproducing sorting and filtering themselves.

**b. What you would improve**

I would let users choose a task date directly instead of limiting task creation to an hour on the current day. I would also add automated tests for the Streamlit interaction paths and clearer validation for unusual date and time inputs.

**c. Key takeaway**

Being the lead architect means deciding which suggestions fit the real requirements, checking how changes affect connected parts of the system, and verifying behavior instead of trusting plausible-looking code. AI accelerated implementation and review, but I remained responsible for scope, tradeoffs, tests, and the final design.
