import pandas as pd
from  src.algorithms.sweep_line.ds import LineStatus,EventQueue
from src.algorithms.sweep_line import sorting_order, Segment


class SweepLine():
    '''
        Implementing This 
        https://people.inf.elte.hu/fekete/algoritmusok_msc/terinfo_geom/konyvek/Computational%20Geometry%20-%20Algorithms%20and%20Applications,%203rd%20Ed.pdf
        page 25~
    
    '''
    def __init__(self):
        self.line_status = LineStatus() 
        self.event_queue = EventQueue()
        self.upper_endpoint_segments = {}
        self.lower_endpoint_segments = {}
        self.interior_point_segments = {}
        self.intersections = {
            "x":[],
            "y":[],
            "segment":[]
        }

    def preprocess(self,edges):
        for index,edge in enumerate(edges):
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

            seg = Segment(upper_endpoint,lower_endpoint,index=index)
            self._append_event_point(self.upper_endpoint_segments,seg,upper_endpoint)
            self._append_event_point(self.lower_endpoint_segments,seg,lower_endpoint)
            
    def run_algo(self,is_debug=False):
        '''
            Please first run preprocessing.
            The answer will be at self.intersections
        '''
        while len(self.event_queue.queue)>0:
            event_point = self.event_queue.pop()
            self.handle_event_point(event_point)
            
            if is_debug:
                print(f"Handled Event point: {event_point}")
                sl_xml = self.line_status.convert_to_lxml(self.line_status.root)
                sl_xml.print()
                self.line_status.print()
                self.event_queue.print()
                print("\n",end="\n\n")
                self.line_status.check_sanity()

        data = []
        for x,(y,seg_index) in zip(self.intersections["x"],\
                            zip(self.intersections["y"],self.intersections["segment"])):
            data.append([x,y,seg_index])
        return pd.DataFrame(data,columns=['x',"y","segment"])
    
    def handle_event_point(self,event_point):
        lower_endpoint_segments = self._get_point_segments(self.lower_endpoint_segments,event_point)
        upper_endpoint_segments = self._get_point_segments(self.upper_endpoint_segments,event_point)
        interior_point_segments = self._get_point_segments(self.interior_point_segments,event_point)

        segment_involved = lower_endpoint_segments + upper_endpoint_segments + interior_point_segments

        # intercsetion
        if len(segment_involved) > 1:
            for seg in segment_involved:
                self.intersections["x"].append(event_point.x)
                self.intersections["y"].append(event_point.y)
                self.intersections["segment"].append(seg.index)
        
        # Delete C(p) and L(p)
        [self.line_status.delete_segment(segment) for segment in lower_endpoint_segments]
        [self.line_status.delete_segment(segment) for segment in interior_point_segments]

        # Cut the segemnt for a new upper endpoint (the intersection)
        for segment in interior_point_segments:
            segment.upper_point = event_point

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
        # if not segment_1.is_intersects(segment_2):
        #     return None
        intersec_point = segment_1.find_intersection_point(segment_2)

        if not intersec_point:
            return None
            
        if sorting_order(intersec_point,event_point) > 0:
            if not intersec_point in self.event_queue.queue:
                self.event_queue.append(intersec_point)
            if not (segment_1.is_endpoint(intersec_point)):# and segment_1.is_in_segment(intersec_point):
                    self._append_event_point(self.interior_point_segments,segment_1,intersec_point)
            if not(segment_2.is_endpoint(intersec_point)): #and segment_2.is_in_segment(intersec_point):
                    self._append_event_point(self.interior_point_segments,segment_2,intersec_point)    

    def _append_event_point(self,dict_point_segment,segment,event_point):
        if not str(event_point) in dict_point_segment:
            dict_point_segment[str(event_point)] = []
            
        dict_point_segment[str(event_point)].append(segment)
        dict_point_segment[str(event_point)] = list(set(dict_point_segment[str(event_point)])) # remove duplicates

    def _get_point_segments(self,dict_point_segment,event_point):
        if not str(event_point) in dict_point_segment:
            return []

        return dict_point_segment[str(event_point)]

   