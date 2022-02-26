import bisect
from functools import cmp_to_key, reduce
from tkinter.tix import Tree
# from typing_extensions import Self

from sweep_line.ds import Segment,LineStatus
# import binarytree

from src.data_structures import binary_tree 


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
        [self.remove_from_status(segment) for segment in lower_endpoint_segments]
        [self.remove_from_status(segment) for segment in interior_point_segments]

        

        # insert U(p) and C(p) (flip their position)
        [self.insert_to_status(segment) for segment in upper_endpoint_segments]
        [self.insert_to_status(segment) for segment in interior_point_segments]

        # self.line_status.is_valid()

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
                raise("By the planning of the algorithm, This should not happen")
        
        if len(parents_single_child)  == 1:
            # Adding the missing son
            if not parents_single_child[0].left:
                parents_single_child[0].left = binary_tree.TreeNode(parents_single_child[0].val)
            else:
                parents_single_child[0].right = binary_tree.TreeNode(parents_single_child[0].val)

        '''Step 3'''
        self.line_status.update_internal_nodes_val(self.line_status.root)

    def remove_from_status(self,segment):
        '''
            1. Remove the value from the leaf
            2. If internal node contains this value then delete also. 
                else, delete the leaf next to him also
        '''
        self.line_status.delete_segment(segment)
        self.line_status.delete_segment(segment)




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

