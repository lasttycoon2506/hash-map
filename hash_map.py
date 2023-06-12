# Name: william roberts
# OSU Email: robertw5@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 7
# Due Date: 12/3 11:59 pm
# Description: implements a hash  map with an underlying dyn array data structure where a linked list is used to resolve
# collisions within the hash map. familiar methods are implemented such as clear, add(put), delete etc that all manipulate 
# the hashmap data once it has been properly hashed onto the dyn array


# Import pre-written DynamicArray and LinkedList classes
from a7_include import *


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

#--------------------------------------------------------------------------------------------------


    def clear(self) -> None:
        """
        entirely clears contents of hash map without changing its capacity
        """
        #checks to make sure a bucket isnt empty at that index(hashed location) of the dyn array
        #then sets that bucket (linked list object) equal to empty ll obj
        for i in range(self.capacity):
            if self.buckets.get_at_index(i).length() != 0:
                self.buckets.set_at_index(i, LinkedList())
        self.size = 0
            
        

    def get(self, key: str) -> object:
        """
        returns value paired with given key, returning none if key doesnt exist
        """
        #first find correct hash number by applying given key to hash func then dividing by capacity to ensure no out of bounds
        #index within dyn array
        hash = self.hash_function(key)
        index = hash % self.capacity
        #getatindex returns a ll object which can then call on ll class method contains to see if key exists at that bucket
        #contains returns pointer to node with key value pair, then access its value and return
        if self.buckets.get_at_index(index).contains(key):
            key_match = self.buckets.get_at_index(index).contains(key)
            value_match = key_match.value
            return value_match
        else:
            return None



    def put(self, key: str, value: object) -> None:
        """
        updates key value pair in hash map, replacing its value if key already exists,
        creating new key value pair otherwise 
        """

        hash = self.hash_function(key)
        index = hash % self.capacity
        #if key already exists in hash map then overwrite its previous key value pair
        #otherwise increase size of hashmap (# of distinct key value pairs) and insert new key value pair
        if self.contains_key(key):
            duplicate = self.buckets.get_at_index(index).contains(key)
            duplicate.value = value
        else:
            self.size = self.size + 1
            self.buckets.get_at_index(index).insert(key, value)
        
        

    def remove(self, key: str) -> None:
        """
        removes key value pair from hash map
        """
        hash = self.hash_function(key)
        index = hash % self.capacity
        #remove func from ll class returns boolean whether node (key value pair) was removed
        #making sure to decrease hash map size by 1 if a key value pair was removed
        if self.buckets.get_at_index(index).remove(key):
            self.size -= 1



    def contains_key(self, key: str) -> bool:
        """
        returns true if key is in hash map and false otherwise
        """
        hash = self.hash_function(key)
        index = hash % self.capacity
        #uses ll object to call on contains func where pointer to node is returned if key exists in ll at that bucket
        if self.buckets.get_at_index(index).contains(key) is not None:
            return True
        else:
            return False



    def empty_buckets(self) -> int:
        """
        returns # of empty buckets in hash table
        """
        #by default states hash table is completely empty then update as needed
        empty_buckets = self.capacity
        for i in range(self.capacity):
            #if ll at each particular bucket has at least one node, then that bucket isnt empty
            if self.buckets.get_at_index(i).length() != 0:
                empty_buckets -= 1
            
        return empty_buckets



    def table_load(self) -> float:
        """
        returns current hash table load factor
        """
        # total elements represents all of distinct key value pairs in entire hash  map
        #where load factor is calculated as total elem / capacity bec capacity always fixed to ensure consistent equation results
        total_elements = 0
        for i in range(self.capacity):
            total_elements += self.buckets.get_at_index(i).length()

        load_factor = total_elements / self.capacity 

        return load_factor



    def resize_table(self, new_capacity: int) -> None:
        """
        changes capacity of internal hash table where same key value pairs are moved over
        but are newly rehashed to larger table
        """
        if new_capacity < 1:
            return
        #creates newhash obj that will receive new key value pair hashings and new updated size
        new_hash_func = self.hash_function
        new_hash = HashMap(new_capacity, new_hash_func)
        #loops through original hashmap(dyn array) and if ll obj at that bucket has at least a node then loop through each 
        #node putting its key value pair into newhash obj
        for i in range(self.capacity):
            if self.buckets.get_at_index(i).length() != 0:
                for node in self.buckets.get_at_index(i):
                    new_hash.put(node.key, node.value)
        #sets selfs contents and capacity size equal to newhash obj effectively finishing upsize using newhash as temp variable
        self.buckets = new_hash.buckets
        self.capacity = new_capacity
        self.size = new_hash.size
        


    def get_keys(self) -> DynamicArray:
        """
        returns dyn array containing all keys stored in hash map 
        where order doesnt matter
        """
        #if ll obj contains something at that bucket add each nodes key to allkeys dyn array
        all_keys = DynamicArray()
        for i in range(self.capacity):
            if self.buckets.get_at_index(i).length() != 0:
                for node in self.buckets.get_at_index(i):
                    all_keys.append(node.key)

        return all_keys



#----------------------------------------------------------------------------------------------------------
# BASIC TESTING
if __name__ == "__main__":

    # print("\nPDF - empty_buckets example 1")
    # print("-----------------------------")
    # m = HashMap(100, hash_function_1)
    # print(m.empty_buckets(), m.size, m.capacity)
    # m.put('key1', 10)
    # print(m.empty_buckets(), m.size, m.capacity)
    # m.put('key2', 20)
    # print(m.empty_buckets(), m.size, m.capacity)
    # m.put('key1', 30)
    # print(m.empty_buckets(), m.size, m.capacity)
    # m.put('key4', 40)
    # print(m.empty_buckets(), m.size, m.capacity)


    # print("\nPDF - empty_buckets example 2")
    # print("-----------------------------")
    # m = HashMap(50, hash_function_1)
    # for i in range(150):
    #     m.put('key' + str(i), i * 100)
    #     if i % 30 == 0:
    #         print(m.empty_buckets(), m.size, m.capacity)


    # print("\nPDF - table_load example 1")
    # print("--------------------------")
    # m = HashMap(100, hash_function_1)
    # print(m.table_load())
    # m.put('key1', 10)
    # print(m.table_load())
    # m.put('key2', 20)
    # print(m.table_load())
    # m.put('key1', 30)
    # print(m.table_load())


    # print("\nPDF - table_load example 2")
    # print("--------------------------")
    # m = HashMap(50, hash_function_1)
    # for i in range(50):
    #     m.put('key' + str(i), i * 100)
    #     if i % 10 == 0:
    #         print(m.table_load(), m.size, m.capacity)


    # print("\nPDF - clear example 1")
    # print("---------------------")
    # m = HashMap(100, hash_function_1)
    # print(m.size, m.capacity)
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key1', 30)
    # print(m.size, m.capacity)
    # m.clear()
    # print(m.size, m.capacity)


    # print("\nPDF - clear example 2")
    # print("---------------------")
    # m = HashMap(50, hash_function_1)
    # print(m.size, m.capacity)
    # m.put('key1', 10)
    # print(m.size, m.capacity)
    # m.put('key2', 20)
    # print(m.size, m.capacity)
    # m.resize_table(100)
    # print(m.size, m.capacity)
    # m.clear()
    # print(m.size, m.capacity)


    # print("\nPDF - put example 1")
    # print("-------------------")
    # m = HashMap(50, hash_function_1)
    # for i in range(150):
    #     m.put('str' + str(i), i * 100)
    #     if i % 25 == 24:
    #         print(m.empty_buckets(), m.table_load(), m.size, m.capacity)


    # print("\nPDF - put example 2")
    # print("-------------------")
    # m = HashMap(40, hash_function_2)
    # for i in range(50):
    #     m.put('str' + str(i // 3), i * 100)
    #     if i % 10 == 9:
    #         print(m.empty_buckets(), m.table_load(), m.size, m.capacity)


    # print("\nPDF - contains_key example 1")
    # print("----------------------------")
    # m = HashMap(10, hash_function_1)
    # print(m.contains_key('key1'))
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key3', 30)
    # print(m.contains_key('key1'))
    # print(m.contains_key('key4'))
    # print(m.contains_key('key2'))
    # print(m.contains_key('key3'))
    # m.remove('key3')
    # print(m.contains_key('key3'))


    # print("\nPDF - contains_key example 2")
    # print("----------------------------")
    # m = HashMap(75, hash_function_2)
    # keys = [i for i in range(1, 1000, 20)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.size, m.capacity)
    # result = True
    # for key in keys:
    #     # all inserted keys must be present
    #     result &= m.contains_key(str(key))
    #     # NOT inserted keys must be absent
    #     result &= not m.contains_key(str(key + 1))
    # print(result)


    # print("\nPDF - get example 1")
    # print("-------------------")
    # m = HashMap(30, hash_function_1)
    # print(m.get('key'))
    # m.put('key1', 10)
    # print(m.get('key1'))


    # print("\nPDF - get example 2")
    # print("-------------------")
    # m = HashMap(150, hash_function_2)
    # for i in range(200, 300, 7):
    #     m.put(str(i), i * 10)
    # print(m.size, m.capacity)
    # for i in range(200, 300, 21):
    #     print(i, m.get(str(i)), m.get(str(i)) == i * 10)
    #     print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)


    # print("\nPDF - remove example 1")
    # print("----------------------")
    # m = HashMap(50, hash_function_1)
    # print(m.get('key1'))
    # m.put('key1', 10)
    # print(m.get('key1'))
    # m.remove('key1')
    # print(m.get('key1'))
    # m.remove('key4')


    # print("\nPDF - resize example 1")
    # print("----------------------")
    # m = HashMap(20, hash_function_1)
    # m.put('key1', 10)
    # print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    # m.resize_table(30)
    # print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))


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


    # print("\nPDF - get_keys example 1")
    # print("------------------------")
    # m = HashMap(10, hash_function_2)
    # for i in range(100, 200, 10):
    #     m.put(str(i), str(i * 10))
    # print(m.get_keys())

    # m.resize_table(1)
    # print(m.get_keys())

    # m.put('200', '2000')
    # m.remove('100')
    # m.resize_table(2)
    # print(m.get_keys())
