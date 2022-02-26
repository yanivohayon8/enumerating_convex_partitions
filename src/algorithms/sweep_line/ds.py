from src.data_structures import binary_tree  as binary_tree
from src.hypothesis.rgon_1988 import turn


class Segment(object):
    def __init__(self,upper_point,lower_point):
        self.upper_point = upper_point
        self.lower_point = lower_point

    def __eq__(self,segment):
        return self.upper_point == segment.upper_point and self.lower_point == segment.lower_point

    def __ne__(self,segment):
        return self.upper_point != segment.upper_point or self.lower_point != segment.lower_point

    # def __lt__(self,other):
    #     is_seg_left_to_root = (-1) * turn(self.upper_point,self.lower_point,other.upper_point) # > 0
    #     return is_seg_left_to_root

    def __le__(self,other):
        is_other_left_to = turn(self.upper_point,self.lower_point,other.upper_point)  >= 0
        return is_other_left_to

    def __gt__(self,other):
        return turn(self.upper_point,self.lower_point,other.upper_point)  < 0

    def __hash__(self):
        return str(self)

    def __str__(self):
        return "{0}--{1}".format(self.upper_point,self.lower_point)

class LineStatus(binary_tree.AVL_Tree):

    def __init__(self):
        super().__init__()
        self.root = None

    def insert_segment(self, segment):
        self.root = self.insert(self.root, segment)

    def delete_segment(self,segment):
        self.root = self.delete(self.root,segment)


    def is_leaf(self,node):
        if node is not None:
            return node.left==None and node.right == None
        return False

    def is_have_single_child(self,node):
        return (not node.right and node.left is not None) or (not node.left and node.right is not None)

    def find_parent_with_single_child(self,root):
        if root is not None:
            if self.is_have_single_child(root) and not self.is_leaf(root):
                return [root]
            
            left = self.find_parent_with_single_child(root.left)
            right = self.find_parent_with_single_child(root.right)

            return left+right
        return []

    def update_internal_nodes_val(self,root):
        if root is not None and  not self.is_leaf(root):
            root.val = self.get_internal_node_expected_val(root.left)
            self.update_internal_nodes_val(root.left)
            self.update_internal_nodes_val(root.right)

    def get_internal_node_expected_val(self,root):
        '''
            root - root.left when inserting as input
        '''
        if root is not None:
            if self.is_leaf(root):
                return root.val
            return self.get_internal_node_expected_val(root.right)
        return None


    def is_valid(self):
        try:
            # Check wheter the internal nodes are ok
            self.is_valid_internal_nodes(self.root)

            # # check wheter the leafs are ok 
            # leafs = self.get_leafs(self.root)

            # for index in range(len(leafs) - 1):
            #     pass 
            #     # problem if the segment flipped due to intersection - it will be count as error

        except Exception as err:
            raise(err)

    def is_valid_internal_nodes(self,root):
        '''
            Verify the right internal nodes values and that they don't have single child
        '''
        if root is not None:
            if not self.is_leaf(root):

                # Verify the internal node have the right value
                match_leaf_val = self.get_internal_node_expected_val(root.left)
                if root.val != match_leaf_val:
                    raise(f"Internal Node : {root.val} expected value is {match_leaf_val} beacuse its match leaf")

                # Verify the internal node have 2 childs
                if self.is_have_single_child(root):
                    raise(f"Internal Node : {root.val} have only single child")
                
                self.is_valid_internal_nodes(root.left)
                self.is_valid_internal_nodes(root.right)


    def get_leafs(self,root):
        if root is not None:

            if  self.is_leaf(root):
                return [root]

            return  self.get_leafs(root.left) + self.get_leafs(root.right)