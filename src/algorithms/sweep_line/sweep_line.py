from  src.algorithms.sweep_line.ds import LineStatus,EventQueue, sorting_order,Segment
from functools import cmp_to_key
# from src.data_structures.lines import Segment as GeneralSegment


class SweepLine():
    
    def __init__(self):
        self.line_status = LineStatus() # None
        self.event_queue = EventQueue()
        self.upper_endpoint_segments = {}
        self.lower_endpoint_segments = {}
        self.interior_point_segments = {}
        self.intersections = []

    def preprocess(self,edges):
        for edge in edges:
            '''
                Initialize the lower and upper endpoints DB
                if the dst point is above the src point
                it will be the upper endpoint
            '''
            upper_endpoint = edge.src_point
            lower_endpoint = edge.dst_point
            self.event_queue.append(upper_endpoint)
            self.event_queue.append(lower_endpoint)
            
            if sorting_order(edge.src_point,edge.dst_point) > 0:
                tmp = upper_endpoint
                upper_endpoint = lower_endpoint
                lower_endpoint=tmp

            seg = Segment(upper_endpoint,lower_endpoint)
            self._append_event_point(self.upper_endpoint_segments,seg,upper_endpoint)
            self._append_event_point(self.lower_endpoint_segments,seg,lower_endpoint)
            
    def run_algo(self):
        '''
            Please first run preprocessing.
            The answer will be at self.intersections
        '''
        while len(self.event_queue.queue)>0:
            event_point = self.event_queue.pop()
            self.handle_event_point(event_point)
            yield event_point
    
    def handle_event_point(self,event_point):
        lower_endpoint_segments = self._get_point_segments(self.lower_endpoint_segments,event_point)
        upper_endpoint_segments = self._get_point_segments(self.upper_endpoint_segments,event_point)
        interior_point_segments = self._get_point_segments(self.interior_point_segments,event_point)

        segment_involved = lower_endpoint_segments + upper_endpoint_segments + interior_point_segments

        # intercsetion
        if len(segment_involved) > 1:
            self.intersections.append(
                {
                    "point":event_point,
                    "segments": [seg.get_parent() for seg in segment_involved]
                }
            )
        
        # Delete C(p) and L(p)
        [self.line_status.delete_segment(segment) for segment in lower_endpoint_segments]
        [self.line_status.delete_segment(segment) for segment in reversed(interior_point_segments)]

        # Cut the segemnt for a new upper endpoint (the intersection)
        for segment in interior_point_segments:
            segment.upper_point = event_point
            # self._append_event_point(upper_endpoint_segments,segment,event_point)

        # interior_point_segments.clear()

        # insert U(p) and C(p) (flip their position)
        [self.line_status.insert_segment(segment) for segment in upper_endpoint_segments]
        [self.line_status.insert_segment(segment) for segment in interior_point_segments] # for debug: self.line_status.convert_to_lxml(self.line_status.root).print()

        left_segment = self.line_status.get_left_neighbor(event_point)
        right_segment = self.line_status.get_right_neighbor(event_point)
        
        '''if segments ends at the event point maybe the neighbors of the surronding segments are intersects'''
        if len(interior_point_segments + upper_endpoint_segments)==0:

            if left_segment is not None and right_segment is not None:
                self.find_new_event(left_segment,right_segment,event_point)
        else:
            for seg in upper_endpoint_segments+interior_point_segments:
                if left_segment is not None:
                    self.find_new_event(seg,left_segment,event_point)
                if right_segment is not None:
                    self.find_new_event(seg,right_segment,event_point)
    
    def find_new_event(self,segment_1,segment_2,event_point):
        if not segment_1.is_intersects(segment_2):
            return None
        intersec_point = segment_1.find_intersection_point(segment_2)

        if sorting_order(intersec_point,event_point) > 0:
            if not intersec_point in self.event_queue.queue:
                self.event_queue.append(intersec_point)
            if not self.is_point_endpoint(self.upper_endpoint_segments,intersec_point,segment_1) and \
                not self.is_point_endpoint(self.lower_endpoint_segments,intersec_point,segment_1):
                if segment_1.is_point_in_segment(intersec_point):
                    self._append_event_point(self.interior_point_segments,segment_1,intersec_point)
            if not self.is_point_endpoint(self.upper_endpoint_segments,intersec_point,segment_2) and \
                not self.is_point_endpoint(self.lower_endpoint_segments,intersec_point,segment_2):
                if segment_2.is_point_in_segment(intersec_point):
                    self._append_event_point(self.interior_point_segments,segment_2,intersec_point)    

    def _append_event_point(self,dict_point_segment,segment,event_point):
        if not str(event_point) in dict_point_segment:
            dict_point_segment[str(event_point)] = []

        dict_point_segment[str(event_point)].append(segment)

    def _get_point_segments(self,dict_point_segment,event_point):
        if not str(event_point) in dict_point_segment:
            return []
        # lst = dict_point_segment[str(event_point)]
        # return sorted(lst,key=cmp_to_key(sorting_order)) # lst
        return dict_point_segment[str(event_point)]

    def is_point_endpoint(self,dict_upper_lower,point,segment):
        if point in dict_upper_lower:
            return segment in dict_upper_lower[str(point)]
        return False

   