# frontiers.py
# ----------------
# COMP3620/6320 Artificial Intelligence
# The Australian National University
# For full attributions, see attributions.txt on Wattle at the end of the course.

""" This file contains data structures useful for representing search frontiers
    for your depth-first, breadth-first, and a-star search algorithms (Q1-3).

    You do not have to use these, but it is strongly recommended.

    ********** YOU SHOULD NOT CHANGE ANYTHING IN THIS FILE **********
"""

import collections
import heapq
from typing import Any, Callable, Dict, Optional, TypeVar

T = TypeVar('T')


class Stack:
    """ A container with a last-in-first-out (LIFO) queuing policy."""

    def __init__(self):
        """ Make a new empty Stack."""
        self.contents = []

    def push(self, item: Any):
        """ Push item onto the stack."""
        self.contents.append(item)

    def pop(self) -> Any:
        """ Pop and return the most recently pushed item from the stack."""
        return self.contents.pop()

    def peek(self) -> Any:
        """ Return the most recently pushed item from the stack."""
        return self.contents[-1]

    def is_empty(self) -> bool:
        """ Returns True if the stack is empty and False otherwise."""
        return not self.contents

    def find(self, f: Callable[[T], bool]) -> Optional[T]:
        """ Return some item n from the queue such that f(n) is True.
            Return None if there is no such item. Note that the parameter `f`
            is a function. This method can be slow since in the worst case, we
            need to scan through the entire stack.
        """
        for elem in self.contents:
            if f(elem):
                return elem
        return None

    def __str__(self):
        """ Return a string representation of the Stack.
            (Stack) -> str
        """
        return str(self.contents)


class Queue:
    """ A container with a first-in-first-out (FIFO) queuing policy.

        Its contents are stored in a collections.deque. This allows constant
        time insertion and removal of elements at both ends -- whereas a list
        is constant time to add or remove elements at the end, but linear
        time at the head.
    """

    def __init__(self):
        """ Make a new empty Queue."""
        self.contents = collections.deque()

    def push(self, item: Any):
        """ Enqueue the item into the queue"""
        self.contents.append(item)

    def pop(self) -> Any:
        """ Dequeue and return the earliest enqueued item still in the queue."""
        return self.contents.popleft()

    def peek(self) -> Any:
        """ Return the earliest enqueued item still in the queue."""
        return self.contents[0]

    def is_empty(self) -> bool:
        """ Return True if the queue is empty and False otherwise."""
        return not self.contents

    def find(self, f: Callable[[T], bool]) -> Optional[T]:
        """ Return some item n from the queue such that f(n) is True.
            Return None if there is no such item. Note that the parameter `f`
            is a function. This method can be slow since in the worst case, we
            need to scan through the entire queue.
        """
        for elem in self.contents:
            if f(elem):
                return elem
        return None

    def __str__(self):
        """ Return a string representation of the queue.
            (Queue) -> str
        """
        return str(list(self.contents))


class PriorityQueue:
    """ This class implements a priority queue data structure. Each inserted item
        has a priority associated with it and we are usually interested in quick
        retrieval of the lowest-priority item in the queue. This data structure
        allows O(1) access to the lowest-priority item. However, finding
        an item takes O(n) and can be quite slow.
    """

    def __init__(self):
        """ Make a new empty priority queue.
            (PriorityQueue) -> None
        """
        self.heap = []
        self.count = 0

    def push(self, item: Any, priority: float):
        """ Enqueue an item to the priority queue with a given priority."""
        heapq.heappush(self.heap, (priority, self.count, item))
        self.count += 1

    def pop(self) -> Any:
        """ Dequeue and return the item with the lowest priority, breaking ties
            in a FIFO order.
        """
        return heapq.heappop(self.heap)[2]

    def peek(self) -> Any:
        """ Return the item with the lowest priority, breaking ties in a FIFO order."""
        return self.heap[0][2]

    def is_empty(self) -> bool:
        """ Returns True if the queue is empty and False otherwise."""
        return not self.heap

    def find(self, f: Callable[[T], bool]) -> Optional[T]:
        """ Return some item n from the queue such that f(n) is True.
            Return None if there is no such item. Note that the parameter `f`
            is a function. This method can be slow since in the worst case, we
            need to scan through the entire queue.
        """
        for elem in self.heap:
            if f(elem[2]):
                return elem[2]
        return None

    def change_priority(self, item: Any, priority: float):
        """ Change the priority of the given item to the specified value. If
            the item is not in the queue, a ValueError is raised.
        """
        for eid, elem in enumerate(self.heap):
            if elem[2] == item:
                self.heap[eid] = (priority, self.count, item)
                self.count += 1
                heapq.heapify(self.heap)
                return
        raise ValueError("Error: " + str(item) +
                         " is not in the PriorityQueue.")

    def __str__(self):
        """ Return a string representation of the queue. This will not be in
            order.
            (PriorityQueue) -> str
        """
        return str([x[2] for x in self.heap])


class PriorityQueueWithFunction(PriorityQueue):
    """ Implements a priority queue with the same push/pop signature of the
        Queue and the Stack classes. This is designed for drop-in replacement for
        those two classes. The caller has to provide a priority function, which
        extracts each item's priority.

        In addition, every time we push an item into the queue, we will also
        store the item in a lookup table. This lookup table will allow to find
        an item by key. Searching for a node now takes O(1) instead of O(n)
        time, at the expense of using more memory.
    """

    def __init__(self, priority_function: Callable[[Any], float], key_attribute: str):
        """ Make a new priority queue with the given priority function.

            Parameters
            ----------
            priority_function : Callable[[Any], float]
                In order to use this queue, you need to pass it a function
                which takes an item as the input and return its priority number.

            key_attribute : str
                You also need to specify the name of an attribute in the item
                used for lookup. For example, if we wanted to reference nodes
                by their state, we would use "state" as the key_attribute.
                Searching for a node with a given state now takes O(1) instead
                of O(n) time when we use the find_by_key() method.
        """
        super().__init__()
        self.priority_function = priority_function
        self.lookup_table: Dict[str, Any] = {}
        self.key_attribute = key_attribute

    def push(self, item: Any):
        """" Adds an item to the queue with priority from the priority function.
        """
        if hasattr(item, self.key_attribute):
            key = getattr(item, self.key_attribute)
            self.lookup_table[key] = item
        else:
            raise ValueError('Object {} does not have key attribute {}'.format(
                item, self.key_attribute))

        heapq.heappush(self.heap, (self.priority_function(item),
                                   self.count, item))
        self.count += 1

    def pop(self) -> Any:
        """ Dequeue and return the item with the lowest priority, breaking ties
            in a FIFO order.
        """
        item = heapq.heappop(self.heap)[2]
        key = getattr(item, self.key_attribute)
        del self.lookup_table[key]
        return item

    def find_by_key(self, key: str) -> Any:
        """ Find an item from the queue that contains a key."""
        if key in self.lookup_table:
            return self.lookup_table[key]
        return None
