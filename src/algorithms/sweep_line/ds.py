from src.data_structures import binary_tree  as binary_tree
from functools import cmp_to_key

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
        self.root = self.delete(self.root,segment)

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

    def get_neighbors(self,event_point):
        leafs = self.get_segment_on_line()
        neighbor_right,neighbor_left = None,None

        for seg in leafs:
            if seg < event_point:
                neighbor_right = seg
                break
        
        for seg in list(reversed(leafs)):
            if seg > event_point:
                neighbor_left = seg
                break

        return neighbor_left,neighbor_right

    def print(self):
        print("Line Status:", end="\t")
        segments = self.get_segment_on_line()
        [print(seg, end=";") for seg in segments]
        print()


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



def sorting_order(point1,point2):
    '''
        Sorting mechanism for the event points
        if one have higher y-coordinated it will be sorted first.
        if the y-coordinates are equal, then the one with smaller x-coordinate will be count first
    '''
    if point1.y == point2.y:
        return point1.x-point2.x
    else:
        return point2.y-point1.y 