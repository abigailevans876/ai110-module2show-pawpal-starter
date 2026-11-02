# PawPal+ Project Reflection

## 1. System Design
### Core Actions
1. **Add & Manage Pets:** Register pets with vital statistics (species, breed, age) and special care notes.
2. **Schedule Daily Tasks:** Set time-stamped care obligations (walks, medication, feedings) tied directly to a specific pet.
3. **Daily Agenda Tracking:** Filter and view all tasks due on the current day, with the ability to mark them completed.

**a. Initial design**

- Briefly describe your initial UML design.

The design uses an object-oriented domain layer separating data models from scheduling operations:
- **`Pet` (Dataclass):** Encapsulates pet identity and care requirements.
- **`Task` (Dataclass):** Encapsulates task metadata, target execution timestamp, completion state, and an explicit foreign key reference (`pet_id`) linking it to a `Pet`.
- **`Owner` (Dataclass):** Represents the user entity who maintains 1-to-many ownership over `Pet` instances.
- **`Scheduler` (Service Class):** Decouples schedule management from the entities themselves. It handles filtering (by date, pet, or status) and task lifecycle updates without burdening the data classes with operational queries.
- What classes did you include, and what responsibilities did you assign to each?


**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Design Changes & AI Review Insights
- **Decoupled Task Ownership:** Initially, tasks could have been stored directly inside each `Pet` object (`Pet.tasks`). However, moving task collection and filtering into a dedicated `Scheduler` avoids tight coupling and simplifies global operations like "Show all tasks across all pets for today."
- **Lightweight Identifiers:** Assigned auto-generated short UUIDs (`pet_id`, `task_id`) so entities reference each other cleanly by ID rather than keeping circular object references.
- **Dataclass `field(default_factory=...)` Pattern:** Used `default_factory` for mutable default parameters (like `pets: List[Pet]`) to prevent Python's shared-state mutable default argument trap.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

The scheduler detects conflicts only when two tasks have the exact same due date and time; it does not calculate whether tasks with durations overlap. This keeps conflict detection lightweight and gives the owner a useful warning without requiring duration data, but it can miss tasks that are scheduled close together and would overlap in practice. For this simple scheduler, exact-time matching is a clear first step.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
