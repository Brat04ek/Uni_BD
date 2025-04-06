from typing import List
from math import floor
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
import networkx as nx

class InterfaceNode(ABC):
    

    @abstractmethod
    def minKey(self):
        pass

    @abstractmethod
    def maxKey(self):
        pass

    @abstractmethod
    def numOfKeys(self):
        pass

    @abstractmethod
    def search(self, key):
        pass

    @abstractmethod
    def insert(self, order, key, data):
        pass

    @abstractmethod
    def delete(self, order, key):
        pass



class LeafDataKey:
    def __init__(self, key, data):
        self.key = key
        self.data = data

class Leaf(InterfaceNode):
    nextLeaf = None

    def __init__(self, leafsDataKey: List[LeafDataKey] = None):
        
        if leafsDataKey == None:
            leafsDataKey = []
        
        self.leafsDataKey = leafsDataKey

    def maxKey(self):
        return self.leafsDataKey[-1].key

    def minKey(self):
        return self.leafsDataKey[0].key

    def numOfKeys(self):
        return len(self.leafsDataKey)

    def search(self, key):

        for leaf in self.leafsDataKey:
            if leaf.key == key:
                return leaf.data
            
        return None

    def insert(self, order, key, data):
        i = 0
        while i < len(self.leafsDataKey) and key >= self.leafsDataKey[i].key:
            i += 1
        
        self.leafsDataKey.insert(i, LeafDataKey(key, data))

        maxNumOfKeys = order - 1
        if maxNumOfKeys < len(self.leafsDataKey):
            return self.__split(maxNumOfKeys)
        
        return [None, None]
        
    def __split(self, maxNumOfKeys):

        part_2 = self.leafsDataKey[floor(maxNumOfKeys/2):]
        newLeaf = Leaf(part_2)
        newLeaf.nextLeaf = self.nextLeaf
        newKey = part_2[0].key

        part_1 = self.leafsDataKey[:floor(maxNumOfKeys/2)]
        self.leafsDataKey = part_1
        self.nextLeaf = newLeaf

        return [newKey, newLeaf]
    
    def delete(self, order, key):

        for i in range(len(self.leafsDataKey)):
            if self.leafsDataKey[i].key == key:
                self.leafsDataKey.pop(i)
                return True
        
        return False

class Node(InterfaceNode):

    def __init__(self, keys : List[int], pointers : List[InterfaceNode]):
        self.keys = keys
        self.pointers = pointers

    def maxKey(self):
        return self.keys[-1]

    def minKey(self):
        return self.pointers[0].minKey()

    def numOfKeys(self):
        return len(self.keys)

    def search(self, key):
        i = 0
        while i < len(self.keys) and key >= self.keys[i]:
            i += 1
        
        return self.pointers[i].search(key)
        
    def insert(self, order, key, data):
        i = 0
        while i < len(self.keys) and key >= self.keys[i]:
            i += 1
        
        newKey, newNode = self.pointers[i].insert(order, key, data)

        if newKey == None or newKey == None:
            return [None, None]
        
        self.keys.insert(i, newKey)
        self.pointers.insert(i + 1, newNode)

        maxNumOfKeys = order - 1
        if maxNumOfKeys < len(self.keys):
            return self.__split(maxNumOfKeys)
        
        return [None, None]

    def __split(self, maxNumOfKeys):

        newKey = self.keys[floor(maxNumOfKeys/2)]
        newNode = Node(self.keys[floor(maxNumOfKeys/2) + 1 : ], self.pointers[floor(maxNumOfKeys/2) + 1 : ])

        self.keys = self.keys[:floor(maxNumOfKeys/2)]
        self.pointers = self.pointers[ : floor(maxNumOfKeys/2) + 1]

        return [newKey, newNode]
    
    def delete(self, order, key):
        i = 0
        while i < len(self.keys) and key >= self.keys[i]:
            i += 1

        response = self.pointers[i].delete(order, key)

        if response == False:
            return False
        maxNumOfKeys = order - 1
        if self.pointers[i].numOfKeys() < floor(maxNumOfKeys / 2):
            
            if len(self.pointers) > i + 1 and self.pointers[i+1].numOfKeys() > floor(maxNumOfKeys/2):  
                self.__takeFromRight(i)
                
            elif i != 0 and self.pointers[i-1].numOfKeys() > floor(maxNumOfKeys/2):          
                self.__takeFromLeft(i)
   
            elif len(self.pointers) > i + 1:
                self.__merge(i)
            else: 
                self.__merge(i-1)

        if key in self.keys:
            
            key_id = self.keys.index(key)
            if key_id == i:
                i = key_id + 1
            new_key = self.pointers[i].minKey()
        
            self.keys[key_id] = new_key

        return True

    def __takeFromRight(self, i):
        recipientNode = self.pointers[i]
        donorNode = self.pointers[i + 1]

        key_id = i # - 1 if i != 0 else 0
        if isinstance(recipientNode, Leaf) and isinstance(donorNode, Leaf):
            if donorNode.minKey() == self.keys[i]: 
                self.keys[key_id] = donorNode.leafsDataKey[1].key
            else: 
                self.keys[key_id] = donorNode.leafsDataKey[0].key
            
            newDataKey = donorNode.leafsDataKey.pop(0)
            recipientNode.leafsDataKey.append(newDataKey)

        elif isinstance(recipientNode, Node) and isinstance(donorNode, Node):

            newKey = donorNode.keys.pop(0)
            recipientNode.keys.append(self.keys[key_id])
            
            newPointer = donorNode.pointers.pop(0)
            recipientNode.pointers.append(newPointer)

            self.keys[key_id] = newKey



    def __takeFromLeft(self, i):
        recipientNode = self.pointers[i]
        donorNode = self.pointers[i - 1]

        key_id = i - 1 if i != 0 else 0
        if isinstance(recipientNode, Leaf) and isinstance(donorNode, Leaf):
            
            self.keys[key_id] = donorNode.leafsDataKey[-1].key
            newDataKey = donorNode.leafsDataKey.pop(-1)
            recipientNode.leafsDataKey.insert(0, newDataKey)

        elif isinstance(recipientNode, Node) and isinstance(donorNode, Node):
            
            donorNode.keys.pop(-1)
            newKey = recipientNode.minKey()
            recipientNode.keys.insert(0, newKey)
            
            newPointer = donorNode.pointers.pop(-1)
            recipientNode.pointers.insert(0, newPointer)

            self.keys[key_id] = recipientNode.minKey()

    def __merge(self, i):
        main = self.pointers[i]
        toBeMerged = self.pointers[i + 1]

        if isinstance(main, Leaf) and isinstance(toBeMerged, Leaf):
            
            main.nextLeaf = toBeMerged.nextLeaf
            for data in toBeMerged.leafsDataKey:
                main.leafsDataKey.append(data)

            self.keys.pop(i)
            if len(self.pointers) > 1:
                self.pointers.pop(i + 1)

        elif isinstance(main, Node) and isinstance(toBeMerged, Node):

            newkeys = main.keys + self.keys + toBeMerged.keys
            newPointers = main.pointers + toBeMerged.pointers
            
            self.keys = newkeys
            self.pointers = newPointers


            # self.keys.pop(i)
            # self.pointers.pop(i)

        
        
        
class Bp_tree:

    def __init__(self, order = 3):
        self.order = order
        self.root = Leaf()

    def search(self, key):
        return self.root.search(key)

    def insert(self, key, data):
        newKey, newNode = self.root.insert(self.order, key, data)
        
        if newKey == None or newKey == None:
            return None 
        
        newRoot = Node([newKey], [self.root, newNode])
        self.root = newRoot
        
        return None

    def delete(self, key):
        return self.root.delete(self.order, key)

    def visualize(self):
        G = nx.DiGraph()
        node_labels = {}
        positions = {}
        level_dict = {}  # To keep track of nodes at each level

        def add_edges(node, parent=None, level=0, pos_x=0):
            node_id = id(node)
            if isinstance(node, Leaf):
                label = f"Leaf: {[leaf.key for leaf in node.leafsDataKey]}"
            else:
                label = f"Node: {node.keys}"

            G.add_node(node_id, level=level)
            node_labels[node_id] = label
            
            if level not in level_dict:
                level_dict[level] = []
            level_dict[level].append(node_id)

            if parent is not None:
                G.add_edge(parent, node_id)

            if isinstance(node, Node):
                for i, child in enumerate(node.pointers):
                    add_edges(child, node_id, level + 1, pos_x + i)

        add_edges(self.root)

        # Set up positions for nodes based on levels
        for level in level_dict:
            num_nodes = len(level_dict[level])
            spacing = 2  # Adjust spacing between nodes
            start_x = -((num_nodes - 1) * spacing) / 2  # Center nodes at each level

            for i, node_id in enumerate(level_dict[level]):
                positions[node_id] = (start_x + i * spacing, -level)  # Invert Y-axis for top-down

        plt.figure(figsize=(12, 6))
        nx.draw(G, pos=positions, labels=node_labels, with_labels=True, node_color="lightblue", edge_color="gray",
                node_size=3000, font_size=10, arrows=True)
        plt.show()

def equalLeaf(leaf1 : Leaf, leaf2 : Leaf):
    if len(leaf1.leafsDataKey) != len(leaf2.leafsDataKey):
        return False
    
    for i in range(len(leaf1.leafsDataKey)):
        if leaf1.leafsDataKey[i].data != leaf2.leafsDataKey[i].data:
            return False
        
        if leaf1.leafsDataKey[i].key != leaf2.leafsDataKey[i].key:
            return False
        
    return True

# if __name__ == "__main__":
#     bTree = Bp_tree(order=3)

#     keys = [2, 21, 26, 18, 32, 8, 20, 43, 5, 11, 22, 29]
#     for i in range(len(keys)):
#         string = f"data{i}"
#         bTree.insert(keys[i], string)


#     bTree.visualize()

    