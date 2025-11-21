from __future__ import annotations

import sys
from pathlib import Path

# Make sure we can import src/tree.py when running this file directly.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from tree import BinaryMinHeap  # type: ignore[import]


def basic_insert_extract_test() -> None:
    heap = BinaryMinHeap()
    heap.insert(3, "c")
    heap.insert(1, "a")
    heap.insert(2, "b")

    assert heap.peek_min()[0] == 1
    assert heap.extract_min()[0] == 1
    assert heap.extract_min()[0] == 2
    assert heap.extract_min()[0] == 3
    assert heap.extract_min() is None


def change_priority_test() -> None:
    heap = BinaryMinHeap()
    h1 = heap.insert(5, "slow")
    heap.insert(1, "fast")

    # Make "slow" more urgent than "fast".
    heap.change_priority(h1, 0)
    assert heap.peek_min()[1] == "slow"


def run_all_tests() -> None:
    basic_insert_extract_test()
    change_priority_test()
    print("All heap tests passed.")


if __name__ == "__main__":
    run_all_tests()
