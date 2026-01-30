"""
Example data structure implementations for testing the pytest generator
This file contains custom data structure classes and functions
"""

from typing import Any, List, Optional, Iterator

class Stack:
    """A simple stack implementation using a list."""
    
    def __init__(self, max_size: Optional[int] = None):
        """
        Initialize a stack with optional maximum size.
        
        Args:
            max_size: Maximum number of elements (None for unlimited)
        """
        self._items = []
        self._max_size = max_size
    
    def push(self, item: Any) -> None:
        """
        Push an item onto the stack.
        
        Args:
            item: The item to push
            
        Raises:
            OverflowError: If stack is at maximum capacity
        """
        if self._max_size is not None and len(self._items) >= self._max_size:
            raise OverflowError("Stack is full")
        self._items.append(item)
    
    def pop(self) -> Any:
        """
        Pop an item from the stack.
        
        Returns:
            The popped item
            
        Raises:
            IndexError: If stack is empty
        """
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self._items.pop()
    
    def peek(self) -> Any:
        """
        View the top item without removing it.
        
        Returns:
            The top item
            
        Raises:
            IndexError: If stack is empty
        """
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self._items[-1]
    
    def is_empty(self) -> bool:
        """Check if the stack is empty."""
        return len(self._items) == 0
    
    def size(self) -> int:
        """Get the current size of the stack."""
        return len(self._items)

class Queue:
    """A simple queue implementation using a list."""
    
    def __init__(self, max_size: Optional[int] = None):
        """
        Initialize a queue with optional maximum size.
        
        Args:
            max_size: Maximum number of elements (None for unlimited)
        """
        self._items = []
        self._max_size = max_size
    
    def enqueue(self, item: Any) -> None:
        """
        Add an item to the rear of the queue.
        
        Args:
            item: The item to add
            
        Raises:
            OverflowError: If queue is at maximum capacity
        """
        if self._max_size is not None and len(self._items) >= self._max_size:
            raise OverflowError("Queue is full")
        self._items.append(item)
    
    def dequeue(self) -> Any:
        """
        Remove and return the front item from the queue.
        
        Returns:
            The front item
            
        Raises:
            IndexError: If queue is empty
        """
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self._items.pop(0)
    
    def front(self) -> Any:
        """
        View the front item without removing it.
        
        Returns:
            The front item
            
        Raises:
            IndexError: If queue is empty
        """
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self._items[0]
    
    def is_empty(self) -> bool:
        """Check if the queue is empty."""
        return len(self._items) == 0
    
    def size(self) -> int:
        """Get the current size of the queue."""
        return len(self._items)

class Node:
    """A simple node for linked list implementation."""
    
    def __init__(self, data: Any, next_node: Optional['Node'] = None):
        """
        Initialize a node.
        
        Args:
            data: The data to store in the node
            next_node: Reference to the next node
        """
        self.data = data
        self.next = next_node

class LinkedList:
    """A simple singly linked list implementation."""
    
    def __init__(self):
        """Initialize an empty linked list."""
        self.head = None
        self._size = 0
    
    def append(self, data: Any) -> None:
        """
        Add an element to the end of the list.
        
        Args:
            data: The data to append
        """
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self._size += 1
    
    def prepend(self, data: Any) -> None:
        """
        Add an element to the beginning of the list.
        
        Args:
            data: The data to prepend
        """
        new_node = Node(data, self.head)
        self.head = new_node
        self._size += 1
    
    def delete(self, data: Any) -> bool:
        """
        Delete the first occurrence of data from the list.
        
        Args:
            data: The data to delete
            
        Returns:
            True if deleted, False if not found
        """
        if not self.head:
            return False
        
        if self.head.data == data:
            self.head = self.head.next
            self._size -= 1
            return True
        
        current = self.head
        while current.next:
            if current.next.data == data:
                current.next = current.next.next
                self._size -= 1
                return True
            current = current.next
        
        return False
    
    def find(self, data: Any) -> bool:
        """
        Check if data exists in the list.
        
        Args:
            data: The data to find
            
        Returns:
            True if found, False otherwise
        """
        current = self.head
        while current:
            if current.data == data:
                return True
            current = current.next
        return False
    
    def size(self) -> int:
        """Get the size of the list."""
        return self._size
    
    def is_empty(self) -> bool:
        """Check if the list is empty."""
        return self.head is None
    
    def to_list(self) -> List[Any]:
        """Convert the linked list to a Python list."""
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

def binary_search(arr: List[int], target: int) -> int:
    """
    Perform binary search on a sorted array.
    
    Args:
        arr: Sorted array of integers
        target: The value to search for
        
    Returns:
        Index of target if found, -1 otherwise
        
    Raises:
        ValueError: If array is not sorted
    """
    if arr != sorted(arr):
        raise ValueError("Array must be sorted for binary search")
    
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1

def merge_sorted_arrays(arr1: List[int], arr2: List[int]) -> List[int]:
    """
    Merge two sorted arrays into one sorted array.
    
    Args:
        arr1: First sorted array
        arr2: Second sorted array
        
    Returns:
        Merged sorted array
    """
    result = []
    i = j = 0
    
    while i < len(arr1) and j < len(arr2):
        if arr1[i] <= arr2[j]:
            result.append(arr1[i])
            i += 1
        else:
            result.append(arr2[j])
            j += 1
    
    # Add remaining elements
    result.extend(arr1[i:])
    result.extend(arr2[j:])
    
    return result

def quick_sort(arr: List[int]) -> List[int]:
    """
    Sort an array using the quicksort algorithm.
    
    Args:
        arr: Array to sort
        
    Returns:
        Sorted array
    """
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quick_sort(left) + middle + quick_sort(right)

def find_duplicates(arr: List[Any]) -> List[Any]:
    """
    Find all duplicate elements in an array.
    
    Args:
        arr: Array to check for duplicates
        
    Returns:
        List of duplicate elements (without duplicates in result)
    """
    seen = set()
    duplicates = set()
    
    for item in arr:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)
    
    return list(duplicates)

def rotate_array(arr: List[Any], positions: int) -> List[Any]:
    """
    Rotate an array to the right by given positions.
    
    Args:
        arr: Array to rotate
        positions: Number of positions to rotate (can be negative for left rotation)
        
    Returns:
        Rotated array
    """
    if not arr:
        return arr
    
    # Normalize positions to be within array length
    positions = positions % len(arr)
    
    if positions == 0:
        return arr[:]
    
    return arr[-positions:] + arr[:-positions]

def matrix_transpose(matrix: List[List[Any]]) -> List[List[Any]]:
    """
    Transpose a matrix (swap rows and columns).
    
    Args:
        matrix: 2D list representing the matrix
        
    Returns:
        Transposed matrix
        
    Raises:
        ValueError: If matrix is empty or rows have different lengths
    """
    if not matrix:
        raise ValueError("Matrix cannot be empty")
    
    if not all(len(row) == len(matrix[0]) for row in matrix):
        raise ValueError("All rows must have the same length")
    
    rows, cols = len(matrix), len(matrix[0])
    transposed = [[matrix[i][j] for i in range(rows)] for j in range(cols)]
    
    return transposed