from src.data_structures import Point

class Line(object):
    def __init__(self,*args):
        self.point_1 = None
        self.point_2 = None
        if len(args) == 1: 
            if isinstance(args[0],Segment):
                self.point_1 = args[0].upper_point
                self.point_2 = args[0].lower_point
        if len(args) == 2:
            self.point_1 = args[0]
            self.point_2 = args[1]

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
            raise ZeroDivisionError('lines do not intersect')   

        d = (det(*line1), det(*line2))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        return Point(x, y)


class Segment(object):
    def __init__(self,upper_point,lower_point):
        self.upper_point = upper_point
        self.lower_point = lower_point

    def __str__(self):
        return "{0}--{1}".format(self.upper_point,self.lower_point)
    
    def __eq__(self,segment):
        return self.upper_point == segment.upper_point and self.lower_point == segment.lower_point

    def __ne__(self,segment):
        return self.upper_point != segment.upper_point or self.lower_point != segment.lower_point


    def find_intersection_point(self,other_segment):

        if not self.is_intersects(other_segment):
            return None

        self_line = Line(self)
        other_line = Line(other_segment)
        inter_point = self_line.find_intersection(other_line)
        
        return inter_point
            
    
    def is_endpoint(self,point):
        return point == self.upper_point or point == self.lower_point

    def is_in_segment(self,point):

        def isBetween(a, b, c):
            crossproduct = (c.y - a.y) * (b.x - a.x) - (c.x - a.x) * (b.y - a.y)

            # compare versus epsilon for floating point values, or != 0 if using integers
            epsilon = 0.001 # This is dangerous. is due to the fact rounding point coordinates to 2
            if abs(crossproduct) > epsilon:
                return False

            dotproduct = (c.x - a.x) * (b.x - a.x) + (c.y - a.y)*(b.y - a.y)
            if dotproduct < 0:
                return False

            squaredlengthba = (b.x - a.x)*(b.x - a.x) + (b.y - a.y)*(b.y - a.y)
            if dotproduct > squaredlengthba:
                return False

            return True
    
        return isBetween(self.lower_point,self.upper_point,point)

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



