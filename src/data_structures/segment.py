from src.hypothesis.rgon_1988 import turn
from src.data_structures import Point

'''

MAYBE THIS MODULE BELONGS UNDER SWEEP LINE PACKAGE 
'''


class Line(object):
    def __init__(self,*args):
        self.point_1 = None
        self.point_2 = None
        if len(args) == 1: 
            if isinstance(args[0],Segment):
                self.point_1 = args[0].upper_point
                self.point_2 = args[0].lower_point

    def find_intersection(self,other_line):
        '''
            https://stackoverflow.com/questions/20677795/how-do-i-compute-the-intersection-point-of-two-lines
        '''
        line1 = [[self.point_1.x,self.point_1.y],[self.point_2.x,self.point_2.y]]
        line2 = [[other_line.point_1.x,other_line.point_1.y],[other_line.point_2.x,other_line.point_2.y]]

        xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
        ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:
            raise Exception('lines do not intersect')   

        d = (det(*line1), det(*line2))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        return Point(x, y)


class Segment(object):
    def __init__(self,upper_point,lower_point):
        self.upper_point = upper_point
        self.lower_point = lower_point

    def __eq__(self,segment):
        return self.upper_point == segment.upper_point and self.lower_point == segment.lower_point

    def __ne__(self,segment):
        return self.upper_point != segment.upper_point or self.lower_point != segment.lower_point

    def __lt__(self,other):
        if isinstance(other,Segment):
            return turn(self.upper_point,self.lower_point,other.upper_point) > 0
        
        if isinstance(other,Point):
            return turn(self.lower_point,self.upper_point,other) > 0
        
        
    def __le__(self,other):
        if isinstance(other,Segment):
            is_other_left_to = turn(self.upper_point,self.lower_point,other.upper_point)  >= 0
            return is_other_left_to

        if isinstance(other,Point):
            is_other_left_to = turn(self.lower_point,self.upper_point,other)  >= 0
            return is_other_left_to

    def __gt__(self,other):
        if isinstance(other,Segment):
            return turn(self.upper_point,self.lower_point,other.upper_point)  < 0   
        
        if isinstance(other,Point):
            return turn(self.lower_point,self.upper_point,other)  < 0   

    def __ge__(self,other):
        if isinstance(other,Segment):
            return turn(self.upper_point,self.lower_point,other.upper_point)  <= 0   
        
        if isinstance(other,Point):
            return turn(self.lower_point,self.upper_point,other)  <= 0  

    def __hash__(self):
        return str(self)

    def __str__(self):
        return "{0}--{1}".format(self.upper_point,self.lower_point)


    def find_intersection_point(self,other_segment):
        self_line = Line(self)
        other_line = Line(other_segment)
        inter_point = self_line.find_intersection(other_line)

        if not (self.lower_point.x < inter_point.x <  self.upper_point.x or\
            self.upper_point.x < inter_point.x <  self.lower_point.x):
            return None
            
        if not (other_segment.lower_point.x < inter_point.x <  other_segment.upper_point.x or\
                other_segment.upper_point.x < inter_point.x <  other_segment.lower_point.x):
            return None
        
        return inter_point
            
    
    def is_point_in_segment(self,point):
        x_condition =  self.upper_point.x < point.x < self.lower_point.x or self.lower_point.x < point.x < self.upper_point.x
        y_condition = self.upper_point.y < point.y < self.lower_point.y or self.lower_point.y < point.y < self.upper_point.y
        return x_condition and y_condition

    def is_intersects(self,segment):
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

        return doIntersect(self.upper_point,self.lower_point,segment.upper_point,segment.lower_point)



