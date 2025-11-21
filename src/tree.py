from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class HeapNode:
    """Internal node used by BinaryMinHeap.

    Attributes:
        priority: Smaller values mean higher priority.
        id: Unique handle used to refer to this node.
        payload: Arbitrary Python object stored in the heap.
    """
    priority: int
    id: int
    payload: Any


class BinaryMinHeap:
    """Binary min-heap for (priority, payload) pairs.

    This heap keeps the smallest priority value at the root.

    Performance summary (n = number of elements in the heap):
        insert:         O(log n) time, O(1) extra space
        extract_min:    O(log n) time, O(1) extra space
        peek_min:       O(1) time, O(1) extra space
        change_priority:O(log n) time, O(1) extra space
        merge:          O(m log(n + m)) time, O(1) extra space besides the new items
    """

    def __init__(self) -> None:
        """Create an empty heap.

        Time: O(1)
        Space: O(1)
        """
        self._nodes: List[HeapNode] = []
        self._positions: Dict[int, int] = {}  # node_id -> index in _nodes
        self._next_id: int = 0

    def __len__(self) -> int:
        """Return number of items in the heap.

        Time: O(1)
        Space: O(1)
        """
        return len(self._nodes)

    def is_empty(self) -> bool:
        """Return True if heap has no elements.

        Time: O(1)
        Space: O(1)
        """
        return not self._nodes

    def insert(self, priority: int, payload: Any) -> int:
        """Insert a new (priority, payload) pair.

        Args:
            priority: Task priority, lower means "more urgent".
            payload: Arbitrary Python value to store.

        Returns:
            An integer handle (node id) that can be used with change_priority().

        Time: O(log n) because we bubble the new node up the tree.
        Space: O(1) extra space besides the new node itself.
        """
        node_id = self._next_id
        self._next_id += 1

        node = HeapNode(priority=priority, id=node_id, payload=payload)
        self._nodes.append(node)
        index = len(self._nodes) - 1
        self._positions[node_id] = index
        self._bubble_up(index)
        return node_id

    def peek_min(self) -> Optional[Tuple[int, Any, int]]:
        """Return the smallest-priority item without removing it.

        Returns:
            (priority, payload, node_id) for the root element, or None if empty.

        Time: O(1)
        Space: O(1)
        """
        if not self._nodes:
            return None
        node = self._nodes[0]
        return node.priority, node.payload, node.id

    def extract_min(self) -> Optional[Tuple[int, Any, int]]:
        """Remove and return the smallest-priority item.

        Returns:
            (priority, payload, node_id) for the removed element, or None if empty.

        Time: O(log n) due to bubbling down the new root.
        Space: O(1) extra space.
        """
        if not self._nodes:
            return None

        min_node = self._nodes[0]
        last_index = len(self._nodes) - 1

        # Move last node to root and shrink list.
        if last_index == 0:
            self._nodes.pop()
            self._positions.pop(min_node.id, None)
        else:
            last_node = self._nodes.pop()
            self._nodes[0] = last_node
            self._positions[last_node.id] = 0
            self._positions.pop(min_node.id, None)
            self._bubble_down(0)

        return min_node.priority, min_node.payload, min_node.id

    def change_priority(self, node_id: int, new_priority: int) -> bool:
        """Update the priority of an existing node.

        Args:
            node_id: Handle returned by insert().
            new_priority: New integer priority.

        Returns:
            True if the node existed and was updated, False otherwise.

        Time: O(log n) from bubbling the node up or down.
        Space: O(1) extra space.
        """
        index = self._positions.get(node_id)
        if index is None:
            return False

        node = self._nodes[index]
        old_priority = node.priority
        node.priority = new_priority

        if new_priority < old_priority:
            self._bubble_up(index)
        elif new_priority > old_priority:
            self._bubble_down(index)
        # If equal, heap property still holds.

        return True

    def merge(self, other: "BinaryMinHeap") -> None:
        """Merge another heap into this one.

        The other heap is left unchanged, but any handles you hold from the
        other heap will not work on this heap.

        Args:
            other: Another BinaryMinHeap instance.

        Time: O(m log(n + m)) where:
            n = current size of this heap
            m = size of other heap
        Space: O(1) extra space besides the inserted nodes.
        """
        for node in other._nodes:
            self.insert(node.priority, node.payload)

    def to_level_order(self) -> List[Tuple[int, Any]]:
        """Return a level-order view of the heap.

        Each element is (priority, payload) in the order stored in the array.

        This is useful for simple visualizations.

        Time: O(n)
        Space: O(n) for the returned list.
        """
        return [(node.priority, node.payload) for node in self._nodes]

    # ----- Internal helper methods below -----

    def _bubble_up(self, index: int) -> None:
        """Restore heap property by moving node at index upward.

        Time: O(log n)
        Space: O(1)
        """
        while index > 0:
            parent_index = (index - 1) // 2
            if self._nodes[index].priority < self._nodes[parent_index].priority:
                self._swap(index, parent_index)
                index = parent_index
            else:
                break

    def _bubble_down(self, index: int) -> None:
        """Restore heap property by moving node at index downward.

        Time: O(log n)
        Space: O(1)
        """
        size = len(self._nodes)
        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            smallest = index

            if left < size and self._nodes[left].priority < self._nodes[smallest].priority:
                smallest = left
            if right < size and self._nodes[right].priority < self._nodes[smallest].priority:
                smallest = right

            if smallest != index:
                self._swap(index, smallest)
                index = smallest
            else:
                break

    def _swap(self, i: int, j: int) -> None:
        """Swap two nodes in the underlying array and update positions.

        Time: O(1)
        Space: O(1)
        """
        self._nodes[i], self._nodes[j] = self._nodes[j], self._nodes[i]
        self._positions[self._nodes[i].id] = i
        self._positions[self._nodes[j].id] = j


if __name__ == "__main__":
    # Simple manual test to verify basic behavior.
    heap = BinaryMinHeap()
    ids = []
    ids.append(heap.insert(3, "wash dishes"))
    ids.append(heap.insert(1, "finish homework"))
    ids.append(heap.insert(5, "watch TV"))

    print("Initial heap (level order):", heap.to_level_order())
    print("Peek:", heap.peek_min())
    print("Extract:", heap.extract_min())
    print("After extract:", heap.to_level_order())

    heap.change_priority(ids[2], 2)
    print("After change_priority:", heap.to_level_order())
