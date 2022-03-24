from src.data_structures import binary_tree  as binary_tree
from functools import cmp_to_key
from src.algorithms.sweep_line import sorting_order
from functools import reduce


class LineStatus(binary_tree.AVL_Tree):

    def __init__(self):
        super().__init__()
        self.root = None

    def insert_segment(self, segment):
        self.root = self.insert(self.root, segment)

        # Insert missing child
        parent_single_child = self._find_parent_with_single_child(self.root)

        if parent_single_child is not None and self.root.height !=1:
            if parent_single_child.right is None:
                parent_single_child.right = binary_tree.TreeNode(parent_single_child.val)
            elif parent_single_child.left is None:
                parent_single_child.left = binary_tree.TreeNode(parent_single_child.val)
                # parent_single_child = self.insert(parent_single_child,parent_single_child.val)

        # Update internal node value: each internal node is the right most child of its left subtree
        self._update_internal_nodes_val(self.root)

    def delete_segment(self,segment):
        right_neighbor = self.get_right_neighbor(segment)
        if right_neighbor is not None:
            new_val = right_neighbor
            self._delete_leaf(self.root,right_neighbor)
            self._replace_leaf_val(self.root,segment,new_val)
            self.root = self.delete(self.root,segment) 
            self._update_internal_nodes_val(self.root)
        else:
            # This code is not checked yet
            # the segment leaf value is the most right leaf
            left_neighbor = self.get_left_neighbor(segment)
            if left_neighbor is not None:
                self._delete_leaf(self.root,left_neighbor)
                self.root = self.delete(self.root,segment)
                self._update_internal_nodes_val(self.root)
            elif self.root is not None:
                # if it is a single node tree - delete the tree
                # if self.root.height > 1:
                    # self._delete_leaf(self.root,self.root.val)
                self._delete_leaf(self.root,self.root.val)
                self.root = self.delete(self.root,segment)
        try:
            self.check_sanity()
        except Exception as err:
            raise err

    def get_segment_on_line(self):
        return self._get_leafs(self.root)#super().in_order(self.root)

    def _is_leaf(self,node):
        if node is not None:
            return node.left==None and node.right == None
        return False

    def _is_have_single_child(self,node):
        return (not node.right and node.left is not None) or (not node.left and node.right is not None)

    def _find_parent_with_single_child(self,root):
        if root is not None:
            if self._is_have_single_child(root) and not self._is_leaf(root):
                return root
            
            left = self._find_parent_with_single_child(root.left)
            right = self._find_parent_with_single_child(root.right)

            # expecting only single node to answer the demand
            if left is not None and not right:
                return left
            if right is not None and not left:
                return right

        return None

    def _get_leafs(self,root):
        if root is not None:
            if  self._is_leaf(root):
                return [root.val]
            return  self._get_leafs(root.left) + self._get_leafs(root.right)
        return []

    def _update_internal_nodes_val(self,root):
        if root is not None and  not self._is_leaf(root):
            root.val = self._get_internal_node_expected_val(root.left)
            self._update_internal_nodes_val(root.left)
            self._update_internal_nodes_val(root.right)

    def _get_internal_node_expected_val(self,root):
        '''
            root - root.left when inserting as input
        '''
        if root is not None:
            if self._is_leaf(root):
                return root.val
            return self._get_internal_node_expected_val(root.right)
        return None

    def _delete_leaf(self,root,segment):
        if root is not None and not self._is_leaf(root):
            if root.left.val == segment and self._is_leaf(root.left):
                root.left = None
            elif root.right.val == segment and self._is_leaf(root.right):
                root.right = None
            else:
                self._delete_leaf(root.left,segment)
                self._delete_leaf(root.right,segment)
    
    def get_right_neighbor(self,point_or_seg):
        leafs = self.get_segment_on_line()
        # neighbor_right = None
        # for seg in leafs:
        #     if seg > point_or_seg:
        #         neighbor_right = seg
        #         break
        
        for seg in leafs:
            # does point_or_seg is left to seg? 
            # choose the previous
            if point_or_seg < seg:
                return seg

        return None#neighbor_right
    
    def get_left_neighbor(self,point_or_seg):
        leafs = self.get_segment_on_line()
        # neighbor_left = None

        # for seg in list(reversed(leafs)):
        #     if seg < point_or_seg:
        #         neighbor_left = seg
        #         break

        for seg in list(reversed(leafs)):
            # does point_or_seg is right to seg? 
            # choose the previous
            if point_or_seg > seg:
                return seg

        return None #neighbor_left

    def _replace_leaf_val(self,root,old_val,new_val):
        if root is not None:
            if root.val == old_val and self._is_leaf(root):
                root.val = new_val
            else:
                self._replace_leaf_val(root.left,old_val,new_val)
                self._replace_leaf_val(root.right,old_val,new_val)

    def print(self):
        print("Line Status:", end="\t")
        segments = self.get_segment_on_line()
        [print(seg, end=";") for seg in segments]
        print()

    def check_sanity(self):
        '''
            Makes sure several things:
            1. Each internal node is equal to its most right leaf in the left subtree
            2. The tree is binary, full, balanced search tree
            3. The leaves represent the segments on the line.
                Make sure the order of them is correct based on the sorting_order fucntion
                and that there is no duplicates
        '''
        self._check_sanity_internal(self.root)
        
        leafs = self.get_segment_on_line()
        # is_leafs_ok = all(leafs[i] < leafs[i + 1] for i in range(len(leafs)-1))

        # if not is_leafs_ok:
        #     raise("Check for duplicates and well ordering of the segment on the line status")

        if not all(leaf is not None for leaf in leafs):
            raise ValueError("On the line segment - segment cannot have None value")

        for i in range(len(leafs)-1):
            if not leafs[i] < leafs[i + 1]:
                raise ValueError("On the line status segment " + str(leafs[i]) +" should be left to " + str(leafs[i + 1]))

    
    def _check_sanity_internal(self,root):
        if not root:
            return None

        if self._is_leaf(root):
            return None

        if self._is_have_single_child(root):
            raise ValueError(f"Node {str(root)} have a single child")
        
        if root.val is None:
            raise ValueError(f"Value of internal node cannot be None")

        expected_val = self._get_internal_node_expected_val(root.left)

        # Internal node cann't have None value
        if not expected_val:
            raise ValueError(f"Expected internal node value can't be None")

        if expected_val != root.val:
            raise ValueError(f"Expected value of node {str(root)} is {str(expected_val)}, whereas it is {str(root.val)}")
        
        # return self._check_sanity_internal(root.left) and self._check_sanity_internal(root.right)
        self._check_sanity_internal(root.left)
        self._check_sanity_internal(root.right)

    def toString(self):
        leafs = self.get_segment_on_line()
        return reduce(lambda acc,x: acc + x + ";" ,["",""] + list(map(lambda x: str(x),leafs)))


class EventQueue():

    def __init__(self):
        self.queue = []

    def append(self,point):
        self.queue.append(point)
        self.queue = list(set(self.queue)) 
        self.queue = sorted(self.queue,key=cmp_to_key(sorting_order))

    def pop(self):
        return self.queue.pop(0)
    
    def print(self):
        print("Event Queue: ",end="\t")
        [print(event, end=";") for event in self.queue]
        print()
    
    def toString(self):
        return reduce(lambda acc,x: acc + x + ";" ,["",""] + list(map(lambda x: str(x),self.queue)))