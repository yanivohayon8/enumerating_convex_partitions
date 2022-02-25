import bisect
from functools import cmp_to_key, reduce
# from typing_extensions import Self


# import binarytree
from src.hypothesis.rgon_1988 import turn
from src.data_structures.binary_tree  import Node
from src.data_structures import binary_tree  as binary_tree
# from src.data_structures.binary_tree import AVL_Tree


class SweepLine():
    
    def __init__(self):
        self.line_status = LineStatus() # None
        self.event_queue = []
        self.upper_endpoint_segments = {}
        self.lower_endpoint_segments = {}
        self.interior_point_segments = {}
        self.intersection = []

    def preprocess(self,edges):
        
        for edge in edges:
            self.upper_endpoint_segments[str(edge.src_point)] = []
            self.upper_endpoint_segments[str(edge.dst_point)] = []
            self.lower_endpoint_segments[str(edge.src_point)] = []
            self.lower_endpoint_segments[str(edge.dst_point)] = []
            self.interior_point_segments[str(edge.src_point)] = []
            self.interior_point_segments[str(edge.dst_point)] = []
            self.event_queue.append(edge.src_point)            
            self.event_queue.append(edge.dst_point) 

        for edge in edges:
            '''
                Initialize the lower and upper endpoints DB
                if the dst point is above the src point
                it will be the upper endpoint
            '''
            upper_endpoint = edge.src_point
            lower_endpoint = edge.dst_point
            
            if sorting_order(edge.src_point,edge.dst_point) > 0:
                tmp = upper_endpoint
                upper_endpoint = lower_endpoint
                lower_endpoint=tmp

            seg = Segment(upper_endpoint,lower_endpoint)
            self.upper_endpoint_segments[str(upper_endpoint)].append(seg)
            self.lower_endpoint_segments[str(lower_endpoint)].append(seg)

        # remove duplicates and sort
        self.event_queue = list(set(self.event_queue)) 
        self.event_queue = sorted(self.event_queue,key=cmp_to_key(sorting_order))
            
    def run_algo(self):
        while len(self.event_queue)>0:
            event_point = self.event_queue.pop(0)
            self.handle_event_point(event_point)
    
    def handle_event_point(self,event_point):
        lower_endpoint_segments = self.lower_endpoint_segments[str(event_point)]
        upper_endpoint_segments = self.upper_endpoint_segments[str(event_point)]
        interior_point_segments = self.interior_point_segments[str(event_point)]

        segment_involved = lower_endpoint_segments + upper_endpoint_segments + interior_point_segments

        # intercsetion
        if len(segment_involved) > 1:
            self.intersection.append(
                {
                    "point":event_point,
                    "segments": segment_involved
                }
            )
        
        # Delete C(p) and L(p)
        # [self.line_status.remove(segment) for segment in lower_endpoint_segments]
        # [self.line_status.remove(segment) for segment in interior_point_segments]

        # insert U(p) and C(p) (flip their position)
        [self.insert_to_status(segment) for segment in upper_endpoint_segments]
        [self.insert_to_status(segment) for segment in interior_point_segments]

        if len(interior_point_segments + upper_endpoint_segments)==0:
            pass

    def insert_to_status(self,segment):
        '''
            This is the procedure
            1. Insert to the status the new node
            2. Find parent with only one child and add to him a child with its value (In the planning it should be the left)
            3. Update all the internal nodes values
        '''

        '''Step 1'''
        self.line_status.insert_segment(segment)

        '''Step 2'''
        parents_single_child = self.line_status.find_parent_with_single_child(self.line_status.root)

        if len(parents_single_child) >= 2:
                raise("By the planningn of the algorith, This should not happen")
        
        if len(parents_single_child)  == 1:
            # Adding the missing son
            if not parents_single_child[0].left:
                parents_single_child[0].left = binary_tree.TreeNode(parents_single_child[0].val)
            else:
                parents_single_child[0].right = binary_tree.TreeNode(parents_single_child[0].val)

        '''Step 3'''
        self.line_status.update_internal_nodes_val(self.line_status.root)

    def remove_from_status(self,segment):
        self.remove_from_status_rec(self.line_status,segment)
        
    def remove_from_status_rec(self,root,segment):
        if root is None: 
            return
        
        if root.value.lower_point == segment.lower_point:
            if root.right.value == root.value:
                pass

            if root.left.value == root.value:
                pass
            return
        
        is_seg_left_to_root = (-1) * turn(root.value.upper_point,root.value.lower_point,segment.lower_point)

        if is_seg_left_to_root < 0:
            self.remove_from_status_rec(root.right,segment)
        
        if is_seg_left_to_root > 0:
            self.remove_from_status_rec(root.left,segment)
        


def is_segments_intersects(segment1,segment2):
    '''
        segment1 - data structure of Edge
        segment2 - data structure of Edge
    '''
    # Given three collinear points p, q, r, the function checks if
    # point q lies on line segment 'pr'
    def onSegment(p, q, r):
        if ( (q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and
            (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y))):
            return True
        return False
    
    def orientation(p, q, r):
        # to find the orientation of an ordered triplet (p,q,r)
        # function returns the following values:
        # 0 : Collinear points
        # 1 : Clockwise points
        # 2 : Counterclockwise
        
        # See https://www.geeksforgeeks.org/orientation-3-ordered-points/amp/
        # for details of below formula.
        
        val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y))
        if (val > 0):
            
            # Clockwise orientation
            return 1
        elif (val < 0):
            
            # Counterclockwise orientation
            return 2
        else:
            
            # Collinear orientation
            return 0
    
    # The main function that returns true if
    # the line segment 'p1q1' and 'p2q2' intersect.
    def doIntersect(p1,q1,p2,q2):
        
        # Find the 4 orientations required for
        # the general and special cases
        o1 = orientation(p1, q1, p2)
        o2 = orientation(p1, q1, q2)
        o3 = orientation(p2, q2, p1)
        o4 = orientation(p2, q2, q1)
    
        # General case
        if ((o1 != o2) and (o3 != o4)):
            return True
    
        # Special Cases
    
        # p1 , q1 and p2 are collinear and p2 lies on segment p1q1
        if ((o1 == 0) and onSegment(p1, p2, q1)):
            return True
    
        # p1 , q1 and q2 are collinear and q2 lies on segment p1q1
        if ((o2 == 0) and onSegment(p1, q2, q1)):
            return True
    
        # p2 , q2 and p1 are collinear and p1 lies on segment p2q2
        if ((o3 == 0) and onSegment(p2, p1, q2)):
            return True
    
        # p2 , q2 and q1 are collinear and q1 lies on segment p2q2
        if ((o4 == 0) and onSegment(p2, q1, q2)):
            return True
    
        # If none of the cases
        return False

    return doIntersect(segment1.src_point,segment1.dst_point,segment2.src_point,segment2.dst_point)

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


class Segment(object):

    def __init__(self,upper_point,lower_point):
        self.upper_point = upper_point
        self.lower_point = lower_point

    def __eq__(self,segment):
        return self.upper_point == segment.upper_point and self.lower_point == segment.lower_point

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

    def insert_segment(self, key):
        self.root = self.insert(self.root, key)


    def is_leaf(self,node):
        if node is not None:
            return node.left==None and node.right == None
        return False

    def find_parent_with_single_child(self,root):
        if root is not None:
            if (not root.right and root.left is not None) or (not root.left and root.right is not None):
                return [root]
            
            left = self.find_parent_with_single_child(root.left)
            right = self.find_parent_with_single_child(root.right)

            return left+right
        return []

    def update_internal_nodes_val(self,root):
        if root is not None and  not self.is_leaf(root):
            root.val = self.get_internal_node_val(root.left)
            self.update_internal_nodes_val(root.left)
            self.update_internal_nodes_val(root.right)

    def get_internal_node_val(self,root):
        if root is not None:
            if self.is_leaf(root):
                return root.val
            return self.get_internal_node_val(root.right)

    # def print(self):
    #     xml = self.convert_to_lxml(self.root)
    #     super().print_as_xml(xml)