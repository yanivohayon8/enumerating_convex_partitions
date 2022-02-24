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
        myTree = AVL_Tree()
        root = None
        nums = [1,2,3,4,5,6]
        
        for num in nums:
            root = myTree.insert(root, num)

        xml = myTree.convert_to_lxml(root)
        myTree.print_as_xml(xml)

if __name__ == "__main__":
    unittest.main()
    pass
    