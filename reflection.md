# PawPal+ Project Reflection

## 1. System Design

Three core actions the user should be able to perform:

- Be able to add/manage multiple pets.
- Schedule vet appointments.
- Create/manage/see list of tasks like feeding the pets and going out for walks.

**a. Initial design**

- Briefly describe your initial UML design.
    - The inital UML design was designed around core actions around pets and tasks. Tasks and appointments can be scheuled. Pets are handeld by Owners.
- What classes did you include, and what responsibilities did you assign to each?
    - I chose to include a Task, Pet, Appointment, Scheduler, and Owner classes. The pet class contains logic only about that pet. The task class contains data and logic for that one task. The appointment class holds data for that one appointment and can be rescheduled. The Scheduler holds lists of tasks and appointments and can retrieve upcoming events and filter by a pet. The owner controls a list of pets.

**b. Design changes**

- Did your design change during implementation?
    - My design did not change. When designing the UML, I was clear in my prompting of what I wanted to see happen.
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
    - The scheduler considers completion status and time overlap.
- How did you decide which constraints mattered most?
    - It seemed more natural to me to only consider completion status and time overlaps, as someone cannot do 2 tasks at once and normally new tasks are created if something needs to be redone. Scheuling based on priority would have created another dimension of complexity.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
    - The conflict detection only checks if two tasks have the exact same start time, rather than checking if their total durations overlap.
- Why is that tradeoff reasonable for this scenario?
    - For a simple pet scheduler, alerting the user only when they schedule two things to start at the exact same minute is enough of a warning mechanism without making the code overly complex.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
    - I used AI for the UML diagream creation, some designing, debugging, and a lot of the implementation.
- What kinds of prompts or questions were most helpful?
    - I asked clarifying questions to understand the code it generated. During the planning phase, I found it helpful to be specific on what I wanted and how I wanted the classes to be organized.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
    - I tested task completion status updates, pet filtering, recursive automation creation, sorting, and conflict warnings.
- Why were these tests important?
    - These tests were important to ensure the logic worked before spending time connecting everything to the frontend.

**b. Confidence**

- How confident are you that your scheduler works correctly?
    - I am very confident in the scheduler's ability to work correctly. 5 stars
- What edge cases would you test next if you had more time?
    - I didn't test different time zones.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
    - First planning with the UML diagram made copilot's suggestions/edits better with less attempts of reprompting.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
    - With more time, I would have tried persisting the data.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
    - It is good to plan first before letting copiolot start editing. It will save time and help both the developer and agent know what is in the code.
