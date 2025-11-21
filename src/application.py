from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple, Any

from tree import BinaryMinHeap


@dataclass
class ScheduledTask:
    """Domain object for a scheduled task."""
    name: str
    duration_minutes: int

    def __str__(self) -> str:
        return f"{self.name} ({self.duration_minutes} min)"


task_menu = """
Task Scheduler using Binary Min-Heap
====================================
1) Add task
2) View next task (peek)
3) Run next task (extract)
4) Change task priority
5) Visualize heap
6) List all tasks (unsorted)
7) Quit
"""


class TaskScheduler:
    """Task scheduler built on top of a BinaryMinHeap.

    The scheduler stores (priority, ScheduledTask) pairs in the heap.
    Lower priority numbers mean the task should run sooner.
    """

    def __init__(self) -> None:
        self._heap = BinaryMinHeap()
        # Map heap node ids to ScheduledTask, so the CLI can show tasks.
        self._tasks: dict[int, ScheduledTask] = {}

    def add_task(self, name: str, priority: int, duration_minutes: int) -> int:
        """Add a task to the scheduler.

        Returns the heap handle used to refer to this task later.

        Time: O(log n) due to heap insert.
        Space: O(1) extra space.
        """
        task = ScheduledTask(name=name, duration_minutes=duration_minutes)
        node_id = self._heap.insert(priority, task)
        self._tasks[node_id] = task
        return node_id

    def load_from_csv(self, csv_path: Path) -> None:
        """Load tasks from a CSV file.

        The file must have headers: name,priority,duration.

        Time: O(k log n) where k is number of rows.
        Space: O(k) for the new tasks.
        """
        with csv_path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    name = row["name"]
                    priority = int(row["priority"])
                    duration = int(row.get("duration", 0))
                except (KeyError, ValueError):
                    # Skip malformed rows.
                    continue
                self.add_task(name=name, priority=priority, duration_minutes=duration)

    def next_task(self) -> Optional[Tuple[int, int, ScheduledTask]]:
        """Remove and return the highest-priority task.

        Returns:
            (handle, priority, task) or None if no tasks.

        Time: O(log n)
        Space: O(1) extra space.
        """
        result = self._heap.extract_min()
        if result is None:
            return None
        priority, payload, node_id = result
        task = self._tasks.pop(node_id, payload)
        return node_id, priority, task

    def peek_next(self) -> Optional[Tuple[int, int, ScheduledTask]]:
        """Return the next task without removing it.

        Time: O(1)
        Space: O(1)
        """
        result = self._heap.peek_min()
        if result is None:
            return None
        priority, payload, node_id = result
        task = self._tasks.get(node_id, payload)
        return node_id, priority, task

    def change_priority(self, handle: int, new_priority: int) -> bool:
        """Update the priority of an existing task.

        Time: O(log n)
        Space: O(1)
        """
        updated = self._heap.change_priority(handle, new_priority)
        return updated

    def visualize_heap(self) -> str:
        """Return a simple level-order visualization of the heap.

        Each level of the binary tree is printed on its own line.

        Time: O(n)
        Space: O(n) for the returned string.
        """
        level_order = self._heap.to_level_order()
        if not level_order:
            return "[empty heap]"

        lines: list[str] = []
        level = 0
        index = 0
        n = len(level_order)
        while index < n:
            level_width = 2 ** level
            slice_end = min(index + level_width, n)
            items = level_order[index:slice_end]
            line = "  ".join(f"{prio}" for prio, _ in items)
            lines.append(line)
            index = slice_end
            level += 1
        return "\n".join(lines)


def run_cli() -> None:
    """Simple command-line interface for the scheduler."""
    scheduler = TaskScheduler()
    project_root = Path(__file__).resolve().parent.parent
    data_file = project_root / "data" / "tasks.csv"

    if data_file.exists():
        print(f"Loading sample tasks from {data_file} ...")
        scheduler.load_from_csv(data_file)

    while True:
        print(task_menu)
        choice = input("Select an option (1-7): ").strip()

        if choice == "1":
            name = input("Task name: ").strip()
            try:
                priority = int(input("Priority (small = urgent): ").strip())
                duration = int(input("Duration in minutes: ").strip())
            except ValueError:
                print("Priority and duration must be integers.")
                continue
            handle = scheduler.add_task(name=name, priority=priority, duration_minutes=duration)
            print(f"Added task with handle {handle} and priority {priority}.")

        elif choice == "2":
            result = scheduler.peek_next()
            if result is None:
                print("No tasks in the queue.")
            else:
                handle, priority, task = result
                print(f"Next task -> handle={handle}, priority={priority}, task={task}")

        elif choice == "3":
            result = scheduler.next_task()
            if result is None:
                print("No tasks to run.")
            else:
                handle, priority, task = result
                print(f"Running task -> handle={handle}, priority={priority}, task={task}")

        elif choice == "4":
            try:
                handle = int(input("Task handle: ").strip())
                new_priority = int(input("New priority: ").strip())
            except ValueError:
                print("Handle and priority must be integers.")
                continue
            if scheduler.change_priority(handle, new_priority):
                print("Priority updated.")
            else:
                print("No such task handle in the heap.")

        elif choice == "5":
            print("Heap visualization (priorities by level):")
            print(scheduler.visualize_heap())

        elif choice == "6":
            heap_view = scheduler._heap.to_level_order()
            if not heap_view:
                print("No tasks in the queue.")
            else:
                print("Tasks in heap storage order:")
                for prio, payload in heap_view:
                    print(f"  priority={prio}, task={payload}")

        elif choice == "7":
            print("Goodbye.")
            break

        else:
            print("Invalid option. Please choose a number between 1 and 7.")


if __name__ == "__main__":
    run_cli()
