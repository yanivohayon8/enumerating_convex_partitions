import bisect
from functools import cmp_to_key, reduce
import binarytree


class SweepLine():
    
    def __init__(self,segments):
        self.line_status = []
        self.event_queue = []
        self.upper_endpoint_segments = {}
        self.lower_endpoint_segments = {}
        self.interior_point_segments = {}
        self.segments = segments
        self.intersection = []

    def preprocess(self):
        
        for seg in self.segments:
            self.upper_endpoint_segments[str(seg.src_point)] = []
            self.upper_endpoint_segments[str(seg.dst_point)] = []
            self.lower_endpoint_segments[str(seg.src_point)] = []
            self.lower_endpoint_segments[str(seg.dst_point)] = []
            self.interior_point_segments[str(seg.src_point)] = []
            self.interior_point_segments[str(seg.dst_point)] = []
            self.event_queue.append(seg.src_point)            
            self.event_queue.append(seg.dst_point) 

        for seg in self.segments:
            '''
                Initialize the lower and upper endpoints DB
                if the dst point is above the src point
                it will be the upper endpoint
            '''
            upper_endpoint = seg.src_point
            lower_endpoint = seg.dst_point
            
            if sorting_order(seg.src_point,seg.dst_point) > 0:
                tmp = upper_endpoint
                upper_endpoint = lower_endpoint
                lower_endpoint=tmp

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
        [self.line_status.remove(segment) for segment in lower_endpoint_segments]
        [self.line_status.remove(segment) for segment in interior_point_segments]

        # insert U(p) and C(p) (flip their position)
        # [bisect.insort_left(self.line_status,segment) for segment in upper_endpoint_segments]
        # [bisect.insort_left(self.line_status,segment)for segment in interior_point_segments]
        # [self.line_status.append(segment) for segment in upper_endpoint_segments]
        # [self.line_status.append(segment) for segment in interior_point_segments]

        # self.line_status = sorted(self.line_status,key=cmp_to_key(sorting_order))

        if len(interior_point_segments + upper_endpoint_segments)==0:
            pass




        
        
    # def remove_from_status(self,segment):
    #     if self.line_status is not None:
    #         segment_index = self.line_status.values.index(segment)
    #         del self.line_status[segment_index]


    # def insert_to_status(self,segment):
    #     if self.line_status is None:
    #         self.line_status = binarytree.Node(segment)

    def print_line_status(self):
        tree = binarytree.build(self.line_status)
        tree.pprint(index=True)
        pass

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