import unittest
from lab2_bp_tree import *

class TestBPTree(unittest.TestCase):
    
    def setUp(self):
        pass
        #self.tree = Bp_tree(order=3)
    
    def test_insert_search_leaf(self):
        leaf = Leaf()
        leaf.insert(4, 4, "data4")
        leaf.insert(4, 2, "data2")
        leaf.insert(4, 6, "data6")

        self.assertEqual(leaf.search(4).data, "data4")
        self.assertEqual(leaf.search(2).data, "data2")
        self.assertEqual(leaf.search(6).data, "data6")
        self.assertIsNone(leaf.search(15))

    def test_split_leaf(self):
        bTree = Bp_tree(order=4)
        keys = [20, 15, 10, 40, 8]

        for i in range(len(keys)):
            string = f"data{i}"
            bTree.insert(keys[i], string)

        self.assertEqual(bTree.root.keys, [15])
        self.assertTrue(equalLeaf(
            bTree.root.pointers[0], Leaf([LeafDataKey(8, "data4"), LeafDataKey(10, "data2")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[1], Leaf([LeafDataKey(15, "data1"), LeafDataKey(20, "data0"), LeafDataKey(40, "data3")])
            ))

    def test_insert_node(self):
        bTree = Bp_tree(order=3)

        keys = [50, 100, 150, 200]
        for i in range(len(keys)):
            string = f"data{i}"
            bTree.insert(keys[i], string)

        self.assertEqual(bTree.root.keys, [100, 150])
        self.assertTrue(equalLeaf(
            bTree.root.pointers[0], Leaf([LeafDataKey(50, "data0")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[1], Leaf([LeafDataKey(100, "data1")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[2], Leaf([LeafDataKey(150, "data2"), LeafDataKey(200, "data3")])
            ))

    def test_split_node(self):
        bTree = Bp_tree(order=3)

        keys = [50, 100, 150, 200, 300]
        for i in range(len(keys)):
            string = f"data{i}"
            bTree.insert(keys[i], string)

        self.assertEqual(bTree.root.keys, [150])
        self.assertEqual(bTree.root.pointers[0].keys, [100])
        self.assertEqual(bTree.root.pointers[1].keys, [200])

        self.assertTrue(equalLeaf(
            bTree.root.pointers[0].pointers[0], Leaf([LeafDataKey(50, "data0")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[0].pointers[1], Leaf([LeafDataKey(100, "data1")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[1].pointers[0], Leaf([LeafDataKey(150, "data2")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[1].pointers[1], Leaf([LeafDataKey(200, "data3"), LeafDataKey(300, "data4")])
            ))

    def test_delete_leaf(self):
        bTree = Bp_tree(order=3)

        keys = [5, 15, 25, 35, 45, 55, 20, 30, 40]
        for i in range(len(keys)):
            string = f"data{i}"
            bTree.insert(keys[i], string)

        bTree.delete(40)

        self.assertEqual(bTree.root.keys, [25])
        self.assertEqual(bTree.root.pointers[0].keys, [15])
        self.assertEqual(bTree.root.pointers[1].keys, [35, 45])

        self.assertTrue(equalLeaf(
            bTree.root.pointers[0].pointers[0], Leaf([LeafDataKey(5, "data0")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[0].pointers[1], Leaf([LeafDataKey(15, "data1"), LeafDataKey(20, "data6")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[1].pointers[0], Leaf([LeafDataKey(25, "data2"), LeafDataKey(30, "data7")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[1].pointers[1], Leaf([LeafDataKey(35, "data3")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[1].pointers[2], Leaf([LeafDataKey(45, "data4"), LeafDataKey(55, "data5")])
            ))


    def test_delete_takeFromRight(self):
        bTree = Bp_tree(order=3)

        keys = [5, 15, 25, 35, 45, 55, 20, 30, 40]
        for i in range(len(keys)):
            string = f"data{i}"
            bTree.insert(keys[i], string)

        bTree.delete(40)
        bTree.delete(5)

        self.assertEqual(bTree.root.keys, [25])
        self.assertEqual(bTree.root.pointers[0].keys, [20])
        self.assertEqual(bTree.root.pointers[1].keys, [35, 45])

        self.assertTrue(equalLeaf(
            bTree.root.pointers[0].pointers[0], Leaf([LeafDataKey(15, "data1")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[0].pointers[1], Leaf([LeafDataKey(20, "data6")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[1].pointers[0], Leaf([LeafDataKey(25, "data2"), LeafDataKey(30, "data7")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[1].pointers[1], Leaf([LeafDataKey(35, "data3")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[1].pointers[2], Leaf([LeafDataKey(45, "data4"), LeafDataKey(55, "data5")])
            ))

    def test_delete_node(self):
        bTree = Bp_tree(order=3)

        keys = [5, 15, 25, 35, 45, 55, 20, 30, 40]
        for i in range(len(keys)):
            string = f"data{i}"
            bTree.insert(keys[i], string)

        bTree.delete(40)
        bTree.delete(5)
        bTree.delete(45)

        self.assertEqual(bTree.root.keys, [25])
        self.assertEqual(bTree.root.pointers[0].keys, [20])
        self.assertEqual(bTree.root.pointers[1].keys, [35, 55])

        self.assertTrue(equalLeaf(
            bTree.root.pointers[0].pointers[0], Leaf([LeafDataKey(15, "data1")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[0].pointers[1], Leaf([LeafDataKey(20, "data6")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[1].pointers[0], Leaf([LeafDataKey(25, "data2"), LeafDataKey(30, "data7")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[1].pointers[1], Leaf([LeafDataKey(35, "data3")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[1].pointers[2], Leaf([LeafDataKey(55, "data5")])
            ))

    def test_delete_node_takeFromLeft(self):
        bTree = Bp_tree(order=3)

        keys = [5, 15, 25, 35, 45, 55, 20, 30, 40]
        for i in range(len(keys)):
            string = f"data{i}"
            bTree.insert(keys[i], string)

        bTree.delete(40)
        bTree.delete(5)
        bTree.delete(45)
        bTree.delete(35)

        self.assertEqual(bTree.root.keys, [25])
        self.assertEqual(bTree.root.pointers[0].keys, [20])
        self.assertEqual(bTree.root.pointers[1].keys, [30, 55])

        self.assertTrue(equalLeaf(
            bTree.root.pointers[0].pointers[0], Leaf([LeafDataKey(15, "data1")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[0].pointers[1], Leaf([LeafDataKey(20, "data6")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[1].pointers[0], Leaf([LeafDataKey(25, "data2")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[1].pointers[1], Leaf([LeafDataKey(30, "data7")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[1].pointers[2], Leaf([LeafDataKey(55, "data5")])
            ))
        
    def test_delete_merge_leaf(self):
        bTree = Bp_tree(order=3)

        keys = [5, 15, 25, 35, 45, 55, 20, 30, 40]
        for i in range(len(keys)):
            string = f"data{i}"
            bTree.insert(keys[i], string)

        bTree.delete(40)
        bTree.delete(5)
        bTree.delete(45)
        bTree.delete(35)
        bTree.delete(25)


        self.assertEqual(bTree.root.keys, [30])
        self.assertEqual(bTree.root.pointers[0].keys, [20])
        self.assertEqual(bTree.root.pointers[1].keys, [55])

        self.assertTrue(equalLeaf(
            bTree.root.pointers[0].pointers[0], Leaf([LeafDataKey(15, "data1")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[0].pointers[1], Leaf([LeafDataKey(20, "data6")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[1].pointers[0], Leaf([LeafDataKey(30, "data7")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[1].pointers[1], Leaf([LeafDataKey(55, "data5")])
            ))


    def test_delete_merge_node(self):
        bTree = Bp_tree(order=3)

        keys = [5, 15, 25, 35, 45, 55, 20, 30, 40]
        for i in range(len(keys)):
            string = f"data{i}"
            bTree.insert(keys[i], string)

        bTree.delete(40)
        bTree.delete(5)
        bTree.delete(45)
        bTree.delete(35)
        bTree.delete(25)
        bTree.delete(55)


        self.assertEqual(bTree.root.keys, [20, 30])

        self.assertTrue(equalLeaf(
            bTree.root.pointers[0], Leaf([LeafDataKey(15, "data1")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[1], Leaf([LeafDataKey(20, "data6")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[2], Leaf([LeafDataKey(30, "data7")])
            ))

    def test_delete_leaf1(self):
        bTree = Bp_tree(order=3)

        keys = [2, 21, 26, 18, 32, 8, 20, 43, 5, 11, 22, 29]
        for i in range(len(keys)):
            string = f"data{i}"
            bTree.insert(keys[i], string)

        bTree.delete(22)

        self.assertEqual(bTree.root.keys, [21])
        self.assertEqual(bTree.root.pointers[0].keys, [8, 18])
        self.assertEqual(bTree.root.pointers[1].keys, [26, 32])

        self.assertTrue(equalLeaf(
            bTree.root.pointers[0].pointers[0], Leaf([LeafDataKey(2, "data0"), LeafDataKey(5, "data8")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[0].pointers[1], Leaf([LeafDataKey(8, "data5"), LeafDataKey(11, "data9")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[0].pointers[2], Leaf([LeafDataKey(18, "data3"), LeafDataKey(20, "data6")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[1].pointers[0], Leaf([LeafDataKey(21, "data1")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[1].pointers[1], Leaf([LeafDataKey(26, "data2"), LeafDataKey(29, "data11")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[1].pointers[2], Leaf([LeafDataKey(32, "data4"), LeafDataKey(43, "data7")])
            ))
    
    def test_delete_node1(self):
        bTree = Bp_tree(order=3)

        keys = [2, 21, 26, 18, 32, 8, 20, 43, 5, 11, 22, 29]
        for i in range(len(keys)):
            string = f"data{i}"
            bTree.insert(keys[i], string)

        bTree.delete(22)
        bTree.delete(32)

        self.assertEqual(bTree.root.keys, [21])
        self.assertEqual(bTree.root.pointers[0].keys, [8, 18])
        self.assertEqual(bTree.root.pointers[1].keys, [26, 43])

        self.assertTrue(equalLeaf(
            bTree.root.pointers[0].pointers[0], Leaf([LeafDataKey(2, "data0"), LeafDataKey(5, "data8")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[0].pointers[1], Leaf([LeafDataKey(8, "data5"), LeafDataKey(11, "data9")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[0].pointers[2], Leaf([LeafDataKey(18, "data3"), LeafDataKey(20, "data6")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[1].pointers[0], Leaf([LeafDataKey(21, "data1")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[1].pointers[1], Leaf([LeafDataKey(26, "data2"), LeafDataKey(29, "data11")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[1].pointers[2], Leaf([ LeafDataKey(43, "data7")])
            ))

    def test_delete_takeFromRight1(self):
        bTree = Bp_tree(order=3)

        keys = [2, 21, 26, 18, 32, 8, 20, 43, 5, 11, 22, 29]
        for i in range(len(keys)):
            string = f"data{i}"
            bTree.insert(keys[i], string)

        bTree.delete(22)
        bTree.delete(32)
        bTree.delete(21)

        self.assertEqual(bTree.root.keys, [26])
        self.assertEqual(bTree.root.pointers[0].keys, [8, 18])
        self.assertEqual(bTree.root.pointers[1].keys, [29, 43])

        self.assertTrue(equalLeaf(
            bTree.root.pointers[0].pointers[0], Leaf([LeafDataKey(2, "data0"), LeafDataKey(5, "data8")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[0].pointers[1], Leaf([LeafDataKey(8, "data5"), LeafDataKey(11, "data9")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[0].pointers[2], Leaf([LeafDataKey(18, "data3"), LeafDataKey(20, "data6")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[1].pointers[0], Leaf([LeafDataKey(26, "data2"),])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[1].pointers[1], Leaf([LeafDataKey(29, "data11")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[1].pointers[2], Leaf([LeafDataKey(43, "data7")])
            ))


    def test_delete_leaf2(self):
        bTree = Bp_tree(order=3)

        keys = [2, 21, 26, 18, 32, 8, 20, 43, 5, 11, 22, 29]
        for i in range(len(keys)):
            string = f"data{i}"
            bTree.insert(keys[i], string)

        bTree.delete(22)
        bTree.delete(32)
        bTree.delete(21)
        bTree.delete(11)

        self.assertEqual(bTree.root.keys, [26])
        self.assertEqual(bTree.root.pointers[0].keys, [8, 18])
        self.assertEqual(bTree.root.pointers[1].keys, [29, 43])

        self.assertTrue(equalLeaf(
            bTree.root.pointers[0].pointers[0], Leaf([LeafDataKey(2, "data0"), LeafDataKey(5, "data8")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[0].pointers[1], Leaf([LeafDataKey(8, "data5")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[0].pointers[2], Leaf([LeafDataKey(18, "data3"), LeafDataKey(20, "data6")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[1].pointers[0], Leaf([LeafDataKey(26, "data2"),])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[1].pointers[1], Leaf([LeafDataKey(29, "data11")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[1].pointers[2], Leaf([LeafDataKey(43, "data7")])
            ))
        
    def test_delete_midleleaf_takeFromRight(self):
        bTree = Bp_tree(order=3)

        keys = [2, 21, 26, 18, 32, 8, 20, 43, 5, 11, 22, 29]
        for i in range(len(keys)):
            string = f"data{i}"
            bTree.insert(keys[i], string)

        bTree.delete(22)
        bTree.delete(32)
        bTree.delete(21)
        bTree.delete(11)
        bTree.delete(8)

        self.assertEqual(bTree.root.keys, [26])
        self.assertEqual(bTree.root.pointers[0].keys, [18, 20])
        self.assertEqual(bTree.root.pointers[1].keys, [29, 43])

        self.assertTrue(equalLeaf(
            bTree.root.pointers[0].pointers[0], Leaf([LeafDataKey(2, "data0"), LeafDataKey(5, "data8")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[0].pointers[1], Leaf([LeafDataKey(18, "data3")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[0].pointers[2], Leaf([LeafDataKey(20, "data6")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[1].pointers[0], Leaf([LeafDataKey(26, "data2"),])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[1].pointers[1], Leaf([LeafDataKey(29, "data11")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[1].pointers[2], Leaf([LeafDataKey(43, "data7")])
            ))
        

    def test_delete_leaf_merge1(self):
        bTree = Bp_tree(order=3)

        keys = [2, 21, 26, 18, 32, 8, 20, 43, 5, 11, 22, 29]
        for i in range(len(keys)):
            string = f"data{i}"
            bTree.insert(keys[i], string)

        bTree.delete(22)
        bTree.delete(32)
        bTree.delete(21)
        bTree.delete(11)
        bTree.delete(8)
        bTree.delete(26)


        self.assertEqual(bTree.root.keys, [29])
        self.assertEqual(bTree.root.pointers[0].keys, [18, 20])
        self.assertEqual(bTree.root.pointers[1].keys, [43])

        self.assertTrue(equalLeaf(
            bTree.root.pointers[0].pointers[0], Leaf([LeafDataKey(2, "data0"), LeafDataKey(5, "data8")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[0].pointers[1], Leaf([LeafDataKey(18, "data3")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[0].pointers[2], Leaf([LeafDataKey(20, "data6")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[1].pointers[0], Leaf([LeafDataKey(29, "data11")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[1].pointers[1], Leaf([LeafDataKey(43, "data7")])
            ))

    def test_delete_node_takeFromLeft1(self):
        bTree = Bp_tree(order=3)

        keys = [2, 21, 26, 18, 32, 8, 20, 43, 5, 11, 22, 29]
        for i in range(len(keys)):
            string = f"data{i}"
            bTree.insert(keys[i], string)

        bTree.delete(22)
        bTree.delete(32)
        bTree.delete(21)
        bTree.delete(11)
        bTree.delete(8)
        bTree.delete(26)
        bTree.delete(43)



        self.assertEqual(bTree.root.keys, [20])
        self.assertEqual(bTree.root.pointers[0].keys, [18])
        self.assertEqual(bTree.root.pointers[1].keys, [29])

        self.assertTrue(equalLeaf(
            bTree.root.pointers[0].pointers[0], Leaf([LeafDataKey(2, "data0"), LeafDataKey(5, "data8")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[0].pointers[1], Leaf([LeafDataKey(18, "data3")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[1].pointers[0], Leaf([LeafDataKey(20, "data6")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[1].pointers[1], Leaf([LeafDataKey(29, "data11")])
            ))
        
    def test_delete_node_merge1(self):
        bTree = Bp_tree(order=3)

        keys = [2, 21, 26, 18, 32, 8, 20, 43, 5, 11, 22, 29]
        for i in range(len(keys)):
            string = f"data{i}"
            bTree.insert(keys[i], string)

        bTree.delete(22)
        bTree.delete(32)
        bTree.delete(21)
        bTree.delete(11)
        bTree.delete(8)
        bTree.delete(26)
        
        bTree.delete(43)

        bTree.delete(20)
        #bTree.visualize()
        

        self.assertEqual(bTree.root.keys, [18,29])

        self.assertTrue(equalLeaf(
            bTree.root.pointers[0], Leaf([LeafDataKey(2, "data0"), LeafDataKey(5, "data8")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[1], Leaf([LeafDataKey(18, "data3")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[2], Leaf([LeafDataKey(29, "data11")])
            ))
        
    def test_delete_merge2(self):
        bTree = Bp_tree(order=3)

        keys = [2, 21, 26, 18, 32, 8, 20, 43, 5, 11, 22, 29]
        for i in range(len(keys)):
            string = f"data{i}"
            bTree.insert(keys[i], string)

        bTree.delete(22)
        bTree.delete(32)
        bTree.delete(21)
        bTree.delete(11)
        bTree.delete(8)
        bTree.delete(26)
        
        bTree.delete(43)
        bTree.delete(18)
        bTree.delete(5)
        #bTree.visualize()
        

        self.assertEqual(bTree.root.keys, [20,29])

        self.assertTrue(equalLeaf(
            bTree.root.pointers[0], Leaf([LeafDataKey(2, "data0")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[1], Leaf([LeafDataKey(20, "data6")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[2], Leaf([LeafDataKey(29, "data11")])
            ))
        
    def test_delete_node_takeFromRight(self):
        bTree = Bp_tree(order=3)

        keys = [2, 21, 26, 18, 32, 8, 20, 43, 5, 11, 22, 29]
        for i in range(len(keys)):
            string = f"data{i}"
            bTree.insert(keys[i], string)

        bTree.delete(18)
        bTree.delete(20)
        bTree.delete(11)
        bTree.delete(8)
        bTree.delete(5)

        #bTree.visualize()
        

  
        self.assertEqual(bTree.root.keys, [26])
        self.assertEqual(bTree.root.pointers[0].keys, [21])
        self.assertEqual(bTree.root.pointers[1].keys, [32])

        self.assertTrue(equalLeaf(
            bTree.root.pointers[0].pointers[0], Leaf([LeafDataKey(2, "data0")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[0].pointers[1], Leaf([LeafDataKey(21, "data1"), LeafDataKey(22, "data10")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[1].pointers[0], Leaf([LeafDataKey(26, "data2"), LeafDataKey(29, "data11")])
            ))
        self.assertTrue(equalLeaf(
            bTree.root.pointers[1].pointers[1], Leaf([LeafDataKey(32, "data4"), LeafDataKey(43, "data7")])
            ))
        
    def test_search_btree(self):
        bTree = Bp_tree(order=3)

        keys = [2, 21, 26, 18, 32, 8, 20, 43, 5, 11, 22, 29]
        for i in range(len(keys)):
            string = f"data{i}"
            bTree.insert(keys[i], string)

        leaf = bTree.search(2)
        self.assertEqual(2, leaf.key)
        self.assertEqual("data0", leaf.data)

    def test_delete_fail(self):
        bTree = Bp_tree(order=3)

        keys = [2, 21, 26, 18, 32, 8, 20, 43, 5, 11, 22, 29]
        for i in range(len(keys)):
            string = f"data{i}"
            bTree.insert(keys[i], string)

        response = bTree.delete(1)
        self.assertFalse(response)





if __name__ == "__main__":
    unittest.main()
