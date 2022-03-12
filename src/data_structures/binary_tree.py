from src.data_types import XmlWrapper

class TreeNode(object):
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.height = 1


# AVL tree class which supports insertion,
# deletion operations
class AVL_Tree(object):
 
    def insert(self,root, key):
         
        # Step 1 - Perform normal BST
        if not root:
            return TreeNode(key)
        elif key <= root.val:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)
 
        # Step 2 - Update the height of the
        # ancestor node
        root.height = 1 + max(self.getHeight(root.left),
                          self.getHeight(root.right))
 
        # Step 3 - Get the balance factor
        balance = self.getBalance(root)
 
        # Step 4 - If the node is unbalanced,
        # then try out the 4 cases
        # Case 1 - Left Left
        # if balance > 1 and key < root.left.val:
        if balance > 1 and key <= root.left.val:
            return self.rightRotate(root)
 
        # Case 2 - Right Right
        # if balance < -1 and key > root.right.val:
        if balance < -1 and key >= root.right.val:
            return self.leftRotate(root)
 
        # Case 3 - Left Right
        # if balance > 1 and key > root.left.val:
        if balance > 1 and key >= root.left.val:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)
 
        # Case 4 - Right Left
        # if balance < -1 and key < root.right.val:
        if balance < -1 and key <= root.right.val:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)
 
        return root
 
    # Recursive function to delete a node with
    # given key from subtree with given root.
    # It returns root of the modified subtree.
    def delete(self, root, key):
 
        # Step 1 - Perform standard BST delete
        if not root:
            return root
 
        elif key < root.val:
            root.left = self.delete(root.left, key)
 
        elif key > root.val:
            root.right = self.delete(root.right, key)
 
        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp
 
            elif root.right is None:
                temp = root.left
                root = None
                return temp
 
            temp = self.getMinValueNode(root.right)
            root.val = temp.val
            root.right = self.delete(root.right,
                                      temp.val)
 
        # If the tree has only one node,
        # simply return it
        if root is None:
            return root
 
        # Step 2 - Update the height of the
        # ancestor node
        root.height = 1 + max(self.getHeight(root.left),
                            self.getHeight(root.right))
 
        # Step 3 - Get the balance factor
        balance = self.getBalance(root)
 
        # Step 4 - If the node is unbalanced,
        # then try out the 4 cases
        # Case 1 - Left Left
        if balance > 1 and self.getBalance(root.left) >= 0:
            return self.rightRotate(root)
 
        # Case 2 - Right Right
        if balance < -1 and self.getBalance(root.right) <= 0:
            return self.leftRotate(root)
 
        # Case 3 - Left Right
        if balance > 1 and self.getBalance(root.left) < 0:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)
 
        # Case 4 - Right Left
        if balance < -1 and self.getBalance(root.right) > 0:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)
 
        return root
 
    def leftRotate(self, z):
 
        y = z.right
        T2 = y.left
 
        # Perform rotation
        y.left = z
        z.right = T2
 
        # Update heights
        z.height = 1 + max(self.getHeight(z.left),
                         self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left),
                         self.getHeight(y.right))
 
        # Return the new root
        return y
 
    def rightRotate(self, z):
 
        y = z.left
        T3 = y.right
 
        # Perform rotation
        y.right = z
        z.left = T3
 
        # Update heights
        z.height = 1 + max(self.getHeight(z.left),
                          self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left),
                          self.getHeight(y.right))
 
        # Return the new root
        return y
 
    def getHeight(self, root):
        if not root:
            return 0
 
        return root.height
 
    def getBalance(self, root):
        if not root:
            return 0
 
        return self.getHeight(root.left) - self.getHeight(root.right)
 
    def getMinValueNode(self, root):
        if root is None or root.left is None:
            return root
 
        return self.getMinValueNode(root.left)
 
    def preOrder(self, root):
 
        if not root:
            return
 
        print("{0} ".format(root.val), end="")
        self.preOrder(root.left)
        self.preOrder(root.right)
    
    def convert_to_lxml(self,root,prefix="_",att="node"):
        # The Tree is empty
        if root is None:
            return XmlWrapper(prefix=prefix)
        else:
            return self._convert_to_lxml(root,prefix=prefix,att=att)

    def _convert_to_lxml(self,root,prefix="_",att="node"):
        if root is not None:
            element_root = XmlWrapper(prefix=prefix)
            element_root.set_att(att,str(root.val))
            element_left = self.convert_to_lxml(root.left,prefix="left")

            if element_left is not None:
                element_root.add_child(element_left)

            element_right = self.convert_to_lxml(root.right,prefix="right")

            if element_right is not None:
                element_root.add_child(element_right)
            
            return element_root
        return None
    
    def in_order(self,root):
        if root is not None:
            return self.in_order(root.left) + [root.val] + self.in_order(root.right)
        return []
            
