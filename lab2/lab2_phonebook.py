from lab2_bp_tree import Bp_tree, Node
from lab2_hash import hash_name


class Phonebook:

    def __init__(self, order =3 ):
        self.tree = Bp_tree(order)

    def insert(self, name : str, phone : str):
        person_hash = hash_name(name)

        return self.tree.insert(person_hash, [name, phone])

    def search(self, name : str):
        person_hash = hash_name(name)
        
        return self.tree.search(person_hash)
    
    def delete(self, name : str):
        person_hash = hash_name(name)
        
        return self.tree.delete(person_hash)
    
    def search_greater_than(self, name: str):
        person_hash = hash_name(name)
        results = []
        
        # починаємо з кореня
        node = self.tree.root

        # йдемо до першого листка, який може містити значення > person_hash
        while isinstance(node, Node):
            node = node.pointers[0]

        # обходимо листки
        while node:
            for leaf_data in node.leafsDataKey:
                length = leaf_data.key % 100
                if length > len(name):
                    results.append(leaf_data.data)
            node = node.nextLeaf

        return results


    def search_less_than(self, name: str):
        results = []
        
        # починаємо з кореня
        node = self.tree.root

        # йдемо до першого листка, який містить можливі значення < person_hash
        while isinstance(node, Node):
            node = node.pointers[0]

        # Проходимо по всіх листках
        while node:
            for leaf_data in node.leafsDataKey:
                length = leaf_data.key % 100
                if length < len(name) :
                    results.append(leaf_data.data)
            node = node.nextLeaf

        return results


