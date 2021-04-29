# Course: CS261 - Data Structures
# Assignment: 5 Part 2
# Student: Chelsey Beck
# Description: A Min-Heap ADT utilizing a DynamicArray data structure. The first index contains the node with the min
# key value or highest priority level. The heap is maintained as a complete tree with the final level being filled
# from left to right. The only data member is the array containing the keys in the heap. Contains methods is_empty,
# add, get_min, remove_min, and build_heap.


# Import pre-written DynamicArray and LinkedList classes
from a5_include import *


class MinHeapException(Exception):
    """
    Custom exception to be used by MinHeap class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class MinHeap:
    def __init__(self, start_heap=None):
        """
        Initializes a new MinHeap
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.heap = DynamicArray()

        # populate MH with initial values (if provided)
        # before using this feature, implement add() method
        if start_heap:
            for node in start_heap:
                self.add(node)

    def __str__(self) -> str:
        """
        Return MH content in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'HEAP ' + str(self.heap)

    def is_empty(self) -> bool:
        """
        Return True if no elements in the heap, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.heap.length() == 0

    def add(self, node: object) -> None:
        """
        Begins by adding the new node to the available spot at the end of the array (leftmost open position in the
        bottom level of the heap). Then computes the index of the parent node. If the new node has a higher priority
        (lower value) than the parent, the node and its parent are swapped. The current index of the node is then
        updated and the new parent index is calculated. The comparison and swaps continue until the new node is placed
        in the correct index position.
        """
        self.heap.append(node)
        i = self.heap.length()-1
        pi = (i-1)//2
        while pi >= 0 and self.heap[i] < self.heap[pi]:
            self.heap.swap(i, pi)
            i = pi
            pi = (i-1)//2
        pass

    def get_min(self) -> object:
        """
        For non-empty heaps, returns the node containing the minimum key value (highest priority) in the heap.
        """
        if self.is_empty():
            raise MinHeapException
        else:
            return self.heap[0]

    def remove_min(self) -> object:
        """
        For non-empty heaps, removes the minimum key node (highest priority) and returns the node object. The node
        occupying th last available index is swapped with the min node. The pop method is called to remove the min node
        from the end of the array and the node is stored with the "min" variable to be returned at the end. Then the
        replacement node in index 0 is percolated down the heap to the correct position. This is done while the
        replacement node has at least one child. The minimum key child is determined and the index computed. If the
        min child has a lower key value than the replacement node, they are swapped. This continues down the tree until
        the replacement node no longer has any children or it has no children with lower key values (higher priority).
        """
        if self.is_empty():
            raise MinHeapException
        else:
            self.heap.swap(0, self.heap.length() - 1)
            min = self.heap.pop()
            i = 0                                               # the swapped node is at index 0
            ic = (2 * i) + 1                                    # left child index is computed
            while (2 * i) + 1 < self.heap.length():             # while the child indices are not both out of bounds
                if (2 * i) + 2 < self.heap.length():            # if the right child is in bounds
                    if self.heap[(2*i)+1] > self.heap[(2*i)+2]:    # if the right is the min child
                        ic += 1                                     # the index of min child is right child
                if self.heap[ic] < self.heap[i]:                # if the child is less than parent
                    self.heap.swap(i, ic)                       # swap child and parent
                    i = ic                                      # update index of node being percolated
                    ic = (2 * i) + 1                            # update child index to left child and repeat loop
                else:                                           # if the node does not need to be swapped, we're done
                    break
            return min

    def build_heap(self, da: DynamicArray) -> None:
        """
        Builds a valid heap from an unordered array and replaces the current heap dynamic array with the newly built
        heap. Begins by copying over the contents of the passed array to a new DynamicArray. Then locates index of
        parent of last leaf in array and percolates down the subheap from that node checking validity (making swaps when
        a higher priority child is encountered). As each subheap is validated, decrements the index working toward the
        first node until the whole heap has been validated.
        """
        new_da = DynamicArray()                      # overwrites existing data with empty da
        for i in range(0, da.length()):              # iterates over the passed array
            new_da.append(da[i])                     # adding each node to the heap (percolated in add method)
        i = (new_da.length() - 1) // 2               # finds parent of largest index leaf (leaves are valid subtrees)
        while i >= 0:
            ic = (2 * i) + 1
            while (2 * i) + 1 < new_da.length():             # while the child indices are not both out of bounds
                if (2 * i) + 2 < new_da.length():            # if the right child is in bounds
                    if new_da[(2*i)+1] > new_da[(2*i)+2]:    # if the right is the min child
                        ic += 1                                     # the index of min child is right child
                if new_da[ic] < new_da[i]:                # if the child is less than parent
                    new_da.swap(i, ic)                       # swap child and parent
                    i = ic                                      # update index of node being percolated
                    ic = (2 * i) + 1                            # update child index to left child and repeat loop
                else:                                           # if the node does not need to be swapped, we're done
                    break
            i -= 1
        self.heap = new_da
        pass


# BASIC TESTING
if __name__ == '__main__':

    print("\nPDF - add example 1")
    print("-------------------")
    h = MinHeap()
    print(h, h.is_empty())
    for value in range(300, 200, -15):
        h.add(value)
        print(h)

    print("\nPDF - add example 2")
    print("-------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    for value in ['monkey', 'zebra', 'elephant', 'horse', 'bear']:
        h.add(value)
        print(h)


    print("\nPDF - get_min example 1")
    print("-----------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    print(h.get_min(), h.get_min())


    print("\nPDF - remove_min example 1")
    print("--------------------------")
    h = MinHeap([1, 10, 2, 9, 3, 8, 4, 7, 5, 6])
    while not h.is_empty():
        print(h, end=' ')
        print(h.remove_min())


    print("\nPDF - build_heap example 1")
    print("--------------------------")
    da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    h = MinHeap(['zebra', 'apple'])
    print(h)
    h.build_heap(da)
    print(h)
    da.set_at_index(0, 500)
    print(da)
    print(h)
