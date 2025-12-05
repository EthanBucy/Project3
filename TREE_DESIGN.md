# Binary Min-Heap Design (tree.py)


## Tree Selection


Chosen tree: Binary min-heap implemented as an array-backed complete binary tree.


I chose a heap because it is the standard data structure for priority queues. It supports fast insertion of new items and fast removal of the most important item. These operations match what a task scheduler needs, constantly adding tasks and repeatedly asking for the next task to run.


## Use Cases


- Task scheduling by priority (this project)
- Event queues in simulations
- Dijkstra’s shortest path algorithm
- Keeping the smallest or largest *kelements in a stream


In all of these, the important operation is to insert new work and quickly pull out the best candidate.


## Properties and Performance


Properties:


- The heap is a complete binary tree stored in a Python list.
- It satisfies the heap property: every parent node has a priority less than or equal to its children.
- The height of the tree is O(log n)


### Asymptotic performance (summary)


Let n be the current number of elements in the heap.


- insert: O(log n) time, O(1) extra space
- extract_min: O(log n) time, O(1) extra space
- peek_min: O(1) time, O(1) extra space
- change_priority: O(log n) time, O(1) extra space
- merge: O(m log(n + m)) time, O(1) extra space (besides the new items)
- to_level_order: O(n) time, O(n) space to build the list


## Interface Design


The concrete heap lives in src/tree.py as BinaryMinHeap. Conceptually, its interface looks like this:


python
# This is a design sketch, not the actual implementation.
from typing import Any, Optional, Protocol, Tuple, List




class IMinHeap(Protocol):
   def insert(self, priority: int, payload: Any) -> int:
       """Insert (priority, payload) into the heap.


       Returns an integer handle that can later be used to
       update the priority.


       Time: O(log n)
       Space: O(1) extra space plus the new node.
       """


   def peek_min(self) -> Optional[Tuple[int, Any, int]]:
       """Return (priority, payload, handle) for the current minimum,
       without removing it. If the heap is empty, return None.


       Time: O(1)
       Space: O(1)
       """


   def extract_min(self) -> Optional[Tuple[int, Any, int]]:
       """Remove and return (priority, payload, handle) for the minimum
       element. If the heap is empty, return None.


       Time: O(log n)
       Space: O(1) extra space.
       """


   def change_priority(self, handle: int, new_priority: int) -> bool:
       """Update the priority of an existing element, identified by its handle.


       Returns True if the handle existed, False otherwise.


       Time: O(log n) using the index map and heap bubbling.
       Space: O(1) extra space.
       """


   def merge(self, other: "IMinHeap") -> None:
       """Insert all elements from another heap into this heap.


       Time: O(m log(n + m)), where:
           n = current size of this heap
           m = size of the other heap
       Space: O(1) extra space beyond the inserted elements.
       """


   def to_level_order(self) -> List[Tuple[int, Any]]:
       """Return a level-order listing of (priority, payload) pairs.


       Time: O(n)
       Space: O(n) for the output list.
       """


   def is_empty(self) -> bool:
       """Return True if the heap is empty.


       Time: O(1)
       Space: O(1)
       """


   def __len__(self) -> int:
       """Return the number of elements in the heap.


       Time: O(1)
       Space: O(1)
       """




## Implementation Notes


The heap is stored in a Python list of HeapNode objects. Each node holds:


 priority: int
 id: int (a unique handle)
 payload: Any (the actual task or value)
A dictionary node_id -> index tracks where each node lives in the list. This map lets change_priority find the correct node in O(1) time before bubbling.


Core algorithms:


Insert:


 Append the new node to the end of the list.
 Bubble it up while its priority is smaller than its parent’s priority.
Extract-min:


 Swap the root with the last element, remove the last element, then bubble the new root down until the heap property is restored.
Change priority:


 Look up the node’s index from the dictionary.
 Update its priority.
 Bubble up if the new priority is smaller, or bubble down if it is larger.
Merge:


 The merge method re-inserts each node from the other heap into this heap using insert. This keeps the code easy to reason about, at the cost of O(m log(n + m)) time.