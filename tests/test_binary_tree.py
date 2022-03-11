import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))


from src.data_structures.binary_tree import AVL_Tree

import unittest

class TestBinaryTree(unittest.TestCase):
    def test_simple_example(self):
        # Driver program to test above function
        myTree = AVL_Tree()
        root = None
        nums = [9, 5, 10, 0, 6, 11, -1, 1, 2]
        
        for num in nums:
            root = myTree.insert(root, num)
        
        # Preorder Traversal
        print("Preorder Traversal after insertion -")
        myTree.preOrder(root)
        print()
        
        # Delete
        key = 10
        root = myTree.delete(root, key)
        
        # Preorder Traversal
        print("Preorder Traversal after deletion -")
        myTree.preOrder(root)
        print()
        
        # This code is contributed by Ajitesh Pathak

    def test_print_simple(self):
        first_tree = AVL_Tree()
        second_tree = AVL_Tree()
        root1 = None
        root2 = None
        first_tree_vals = [4,10,5,6]
        second_tree_vals = [4,10,6,5]
        
        for num in first_tree_vals:
            root1 = first_tree.insert(root1, num)
        
        for num in second_tree_vals:
            root2 = second_tree.insert(root2, num)

        xml1 = first_tree.convert_to_lxml(root1)
        xml1.print()

        xml2 = second_tree.convert_to_lxml(root2)
        xml2.print()

if __name__ == "__main__":
    unittest.main()
    pass
    