import lxml.etree as etree

class Node(object):

    def __init__(self,value,right=None,left=None):
        self.value = value
        self.right = right
        self.left = left


def get_leafs(root):
    if root.right is None and root.left is None:
        return [root.value]
    return 



# def get_height(self):
#     if self is None:
#         return 0
#     return 1 + max(self.get_height(self.right),self.get_height(self.left))


# def in_order_scan(self,root):
#     if not root is None:
#         return root.in_order_scan(root.left) + [root.value] + root.in_order_scan(root.right)
#     return []

def print_pre_order(root):
    nodes = pre_order_rec(root,0)
    level = -1
    for node in nodes:
        if node["level"] !=level:
            level=node["level"]
            print()
            print("Nodes at level {0}: ".format(level) , end=" ")
        print(str(node["value"]), end=",")

    print()

def pre_order_rec(root,level):
    if not root is None:
        level_up=level+1
        return [{"value":root.value,"level":level}]  + pre_order_rec(root.left,level_up) +  pre_order_rec(root.right,level_up)
    return []



class TreeNode(object):
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.height = 1


# AVL tree class which supports insertion,
# deletion operations
class AVL_Tree(object):
 
    def insert(self, root, key):
         
        # Step 1 - Perform normal BST
        if not root:
            return TreeNode(key)
        elif key < root.val:
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
        if balance > 1 and key < root.left.val:
            return self.rightRotate(root)
 
        # Case 2 - Right Right
        if balance < -1 and key > root.right.val:
            return self.leftRotate(root)
 
        # Case 3 - Left Right
        if balance > 1 and key > root.left.val:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)
 
        # Case 4 - Right Left
        if balance < -1 and key < root.right.val:
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


    # def convert_to_lxml(self,root):
    #     if root is not None:
    #         element_root = etree.Element("root")
    #         element_root.text = str(root.val)
    
    def convert_to_lxml(self,root,prefix="_"):
        if root is not None:
            element_root = etree.Element(f"{prefix}_{str(root.val)}")
            element_left = self.convert_to_lxml(root.left,prefix="left")

            if element_left is not None:
                element_root.append(element_left)

            element_right = self.convert_to_lxml(root.right,prefix="right")

            if element_right is not None:
                element_root.append(element_right)
            
            return element_root
        return None
    
    def print_as_xml(self,xml):
        '''
            xml : the output from the convert_to_lxml method
        '''
        etree.indent(xml,space="\t")
        # print(etree.tostring(xml, pretty_print=True))
        print(etree.tostring(xml).decode("UTF-8"))

