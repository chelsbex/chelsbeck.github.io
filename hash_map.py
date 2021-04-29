# Course: CS261 - Data Structures
# Assignment: 5 Part 1
# Student: Chelsey Beck
# Description: A Hash Map ADT utilizing a DynamicArray data structure imported from a5_include. Collisions are handled
# through chaining. Each index keys are mapped to contains a LinkedList data structure, also imported from a5_include.
# The key-value pairs are stored as nodes in the linked list located at the hashed index. To initialize the HashMap,
# requires input capacity and hash function. 2 hash functions are included.


# Import pre-written DynamicArray and LinkedList classes
from a5_include import *


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Init new HashMap based on DA with SLL for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
        return out

    def clear(self) -> None:
        """
        Clears the contents of the table without changing the capacity. This is carried out by replacing the
        DynamicArray with an empty one, adding LinkedList objects based on the capacity and resetting the size to 0.
        """
        self.buckets = DynamicArray()
        for _ in range(self.capacity):
            self.buckets.append(LinkedList())
        self.size = 0
        pass

    def get(self, key: str) -> object:
        """
        Hashes the key to locate the becket containing the passed key. Iterates through the bucked to locate the node
        with the specified key. If the bucket is empty (head node is None) or the key was not found in the bucket
        (reaches the end node "None:) returns None. Otherwise, returns the value in the node with the corresponding
        key.
        """
        index = self.hash_function(key) % self.capacity
        bucket = self.buckets[index]
        result = None
        for node in bucket:
            if node.key == key:
                result = node.value
        return result

    def put(self, key: str, value: object) -> None:
        """
        Hashes the key to determine the index of the bucket corresponding to the key. Iterates through the LinkedList
        bucket looking for a node with the specified key. If a node with the matching key is found, updates the value
        of the node. If the key is not found at the hashed index, adds a node with the specified key/value pair to the
        bucket.
        """
        index = self.hash_function(key) % self.capacity
        bucket = self.buckets[index]
        key_present = False
        for node in bucket:
            if node.key == key:
                node.value = value
                key_present = True
        if key_present is False:
            bucket.insert(key, value)
            self.size += 1
        pass

    def remove(self, key: str) -> None:
        """
        Hashes the key to locate the corresponding bucket in the table. Calls the LinkedList remove function to remove
        a node in the list with the corresponding key.
        """
        index = self.hash_function(key) % self.capacity
        bucket = self.buckets[index]
        if bucket.remove(key):
            self.size -= 1
        pass

    def contains_key(self, key: str) -> bool:
        """
        Checks for an element in the table containing the specified key and returns a bool indicating if the table
        contains the key or not. Empty tables return false. If the table is not empty, initializes the "contains"
        variable to False, hashes to key to the matching index position, iterates through the bucket. If the key is
        found, flips "contains" to True. When the end of the list is reached, returns "contains"
        """
        if self.size == 0:
            return False
        else:
            index = self.hash_function(key) % self.capacity
            bucket = self.buckets[index]
            if bucket.contains(key) is None:
                return False
            else:
                return True


    def empty_buckets(self) -> int:
        """
        Determines the number of empty buckets in the hash table. For empty tables, returns the total number of buckets.
        For tables that contains elements, to save time, iterates over the table until the number of elements
        corresponding to the size are located. The number of empty buckets is initialized to the capacity of the table.
        When an occupied bucket is found, decrements this number. When all elements have been located, there cannot be
        any more occupied buckets so the method returns the remaining empty buckets.
        """
        if self.size == 0:  # if there are noe elements in the table, returns the capacity
            return self.capacity
        else:
            empties = self.capacity  # initializes # empties equal to capacity
            count_down = self.size  # counts down as each element is located
            index = 0  # begins at the beginning of the array
            while count_down > 0:  # while we have yet to find all elements
                bucket = self.buckets[index]  # grabs the bucket at the current index
                if bucket.length() != 0:  # if the bucket is not empty
                    empties -= 1  # decrements the number of empties
                    count_down -= bucket.length()  # reduced the # of elements remaining based on the size
                index += 1  # moves to the next bucket
            return empties  # when all elements have been found, returns the number of empties

    def table_load(self) -> float:
        """
        Returns the load factor for the table (the average number of elements per bucket) by dividing the size by the
        capacity.
        """
        return self.size / self.capacity

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the hash table to the specified new capacity as long as that capacity is at least 1. Creates a new
        dynamic array that will replace the one currently holding the collection. Appends empty linked list buckets at
        each index of the new array. Counts down the number of elements in the array as they are found in order to save
        time. Iterates over the buckets in the existing array. When non-empty buckets are found, the first node's key is
        rehashed to the new array and the whole bucket it copied over to the new array in the rehashed index position.
        Once all elements in the old array are found and copied over to their new positions in the new array, the
        capacity is officially updated to the new capacity and the new array of buckets overwrites the old one.
        """
        if new_capacity >= 1:
            new_buckets = DynamicArray()
            for _ in range(new_capacity):
                new_buckets.append(LinkedList())
            for i in range(self.capacity):
                bucket = self.buckets[i]
                if bucket.length() > 0:
                    for node in bucket:
                        new_index = self.hash_function(node.key) % new_capacity
                        new_buckets[new_index].insert(node.key, node.value)
            self.capacity = new_capacity
            self.buckets = new_buckets
        pass

    def get_keys(self) -> DynamicArray:
        """
        Returns a DynamicArray containing all the keys contained in the table. This is done by iterating through each
        bucket in the list until all keys of all elements have been added to the array.
        """
        key_da = DynamicArray()
        count_down = self.size
        index = 0
        while count_down > 0:
            bucket = self.buckets[index]
            count_down -= bucket.length()
            for node in bucket:
                key_da.append(node.key)
            index += 1
        return key_da


# BASIC TESTING
if __name__ == "__main__":

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key2', 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key4', 40)
    print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    print(m.size, m.capacity)
    m.put('key2', 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
