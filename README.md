# Mini-Project 3: Heap-Based Task Scheduler

## Project Overview

This project implements a **binary min-heap** in Python and uses it to build a small but realistic **task scheduler**. The scheduler keeps track of tasks with integer priorities. Lower numbers mean higher urgency, so the scheduler always runs the most urgent task first.

The project is written in Python and organized under the `src/` directory.

- **Tree implemented:** Binary min-heap (`BinaryMinHeap` in `src/tree.py`)
- **Application:** Command-line task scheduler (`TaskScheduler` in `src/application.py`)
- **Intended users:** Students, developers, or anyone who wants a simple example of why heaps are the right tool for priority queues.

## Tree Choice and Application

### What tree did you implement?

I implemented a binary min-heap. The heap stores `(priority, payload)` pairs and supports:

- `insert`
- `extract_min`
- `peek_min`
- `change_priority`
- `merge`
- `to_level_order` (for visualization)

### What does the application do?

The application is a command-line program that:

- Lets the user add tasks with a name, priority, and estimated duration.
- Lets the user peek at the next task without removing it.
- Lets the user run (extract) the next task.
- Lets the user change the priority of a task using its handle.
- Shows a simple visualization of the heap as levels of priorities.

It demonstrates at least five heap operations inside a real use case, not just a synthetic demo.

### Who would use this and why?

Someone would use this application if they want:

- A small, concrete example of a priority queue in action.
- A starting point for building more advanced schedulers.
- A way to see how different priorities affect task ordering.

It is aimed at students in a 300-level algorithms or data structures course, and at instructors who want a clean example to show in class.

## Team Members

- **Ethan Bucy** – design, implementation, and documentation.

## Installation and Setup

### Prerequisites

- Python 3.10 or later (run it as `python3`, no virtual environment required).
- Standard library only. No third-party packages are needed.

### Getting the code

From a terminal:

```bash
git clone <your-repo-url> heap-task-scheduler
cd heap-task-scheduler
```

### How to run the application

Because the source files live under `src/`, run the program from that directory so that `tree.py` can be imported correctly.

```bash
cd src
python3 application.py
```

If `data/tasks.csv` exists at the project root, the application will load those demo tasks on startup.

## Usage Guide

When you run `python3 application.py`, you will see a menu:

1. Add task
2. View next task (peek)
3. Run next task (extract)
4. Change task priority
5. Visualize heap
6. List all tasks (unsorted)
7. Quit

### Example workflow

1. Start the program:

   ```bash
   cd src
   python3 application.py
   ```

2. Option `1` – Add a few tasks:

   * Name: `Finish algorithms homework`, Priority: `1`, Duration: `90`
   * Name: `Wash dishes`, Priority: `4`, Duration: `15`
   * Name: `Exercise`, Priority: `3`, Duration: `45`

3. Option `2` – View the next task. You should see the task with priority `1`.

4. Option `5` – Visualize the heap to see priorities arranged by level.

5. Option `3` – Run the next task. The heap will remove the minimum and re-balance.

6. Option `7` – Quit the program when you are done.

### Expected input and output

* Inputs: menu selections (1–7), task names (strings), integer priorities, integer durations, and task handles (integers) for changing priority.
* Outputs: human-readable messages describing what task will run next, what was run, and how the heap currently looks.

The program guards against invalid integers and missing tasks, so it should fail gracefully on typical user mistakes rather than crash.

## Data Files

Sample tasks live in:

* `data/tasks.csv`

This CSV file has the headers:

```text
name,priority,duration
```

The application reads each row and calls `add_task`. You can edit or extend this file with your own tasks.

## Tree Implementation Details

The `BinaryMinHeap` class is defined in `src/tree.py`. It stores:

* A list of `HeapNode` objects, each with `priority`, `id`, and `payload`.
* A dictionary from `id` to index in the list, so that `change_priority` can find nodes in `O(1)` time.

### Key operations and complexity

Let `n` be the current number of elements.

* `insert(priority, payload) -> int`

  * Time: `O(log n)` (bubble up)
  * Space: `O(1)` extra

* `peek_min() -> Optional[Tuple[int, Any, int]]`

  * Time: `O(1)`
  * Space: `O(1)`

* `extract_min() -> Optional[Tuple[int, Any, int]]`

  * Time: `O(log n)` (bubble down)
  * Space: `O(1)` extra

* `change_priority(handle: int, new_priority: int) -> bool`

  * Time: `O(log n)` after a constant-time lookup in the dictionary
  * Space: `O(1)` extra

* `merge(other: BinaryMinHeap) -> None`

  * Time: `O(m log(n + m))`, where `m` is the size of the other heap
  * Space: `O(1)` extra beyond the elements we insert

* `to_level_order() -> list[tuple[int, Any]]`

  * Time: `O(n)`
  * Space: `O(n)` for the returned list

These time bounds show why the heap is better than a simple list. With a plain unsorted list, `extract_min` would cost `O(n)` because we must scan the whole list. With the heap, both `insert` and `extract_min` stay at `O(log n)`.

## Evolution of the Interface

Initial design:

* `insert`
* `extract_min`
* `peek_min`
* `is_empty`
* `__len__`

During implementation, I added:

* `change_priority(handle, new_priority)` to let the scheduler adjust priorities when plans change.
* `merge(other)` to match typical heap APIs and make it possible to combine workloads.
* `to_level_order()` to support a simple tree visualization in the CLI.

These additions came from actually building the application and seeing what felt missing. The main lesson is that API design is iterative: once you plug a data structure into a real workflow, you quickly learn which extra operations are worth supporting.

## Challenges and Solutions

**Challenge 1 – Efficient change of priority.**
A naive `change_priority` would scan the list to find the item, which would be `O(n)`. To avoid this, the heap keeps a dictionary from node id to its index in the list. This lets the method find a node in constant time and then run the usual `O(log n)` bubble-up or bubble-down procedure.

**Challenge 2 – Keeping the interface simple for users.**
The heap returns an integer handle for each inserted element. The `TaskScheduler` hides this detail as much as possible, only exposing handles when a user wants to change a task’s priority. This separation keeps the scheduler’s code clear and keeps the heap reusable in other contexts.

**Challenge 3 – File organization and relative paths.**
Because the code lives under `src/`, the CLI needs to discover the project root before loading data files. The program uses `Path(__file__).resolve()` and `parent.parent` to compute the root directory, and then reads `data/tasks.csv` from there.

## Future Enhancements

If I had more time, I would:

* Add deadlines and compute priorities from both urgency and estimated duration.
* Write unit tests under `tests/` to exercise edge cases more thoroughly.
* Add support for saving and loading the current heap to disk between runs.
* Provide a small web interface or GUI that wraps the same `TaskScheduler` API.
* Extend the visualization to draw an actual tree diagram instead of just printing levels.

