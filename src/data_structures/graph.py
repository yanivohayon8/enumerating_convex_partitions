from src.data_structures import Point,remove_prefix_
from src.data_structures.lines import Line
from src.data_structures.shapes import Polygon

class Edge(object):
    def __init__(self,*args):
        if len(args)==2: 
            self.src_point = args[0]
            self.dst_point = args[1]
        if len(args) == 1: 
            vals = args[0].split(">>") 
            # tuple_0 =  eval(vals[0])
            # tuple_1 = eval(vals[1])

            point0_str = remove_prefix_(vals[0])
            tuple_0 =  eval(point0_str)
            point1_str = remove_prefix_(vals[1])
            tuple_1 = eval(point1_str)
            self.src_point = Point(tuple_0[0],tuple_0[1])
            self.dst_point = Point(tuple_1[0],tuple_1[1])

        if self.src_point == self.dst_point:
            raise ValueError(f"Tried to create edge with the same src_point and dst_point value ({str(self.src_point)})")

    def plot(self,ax,**kwargs):
        ax.plot([self.src_point.x,self.dst_point.x], [self.src_point.y,self.dst_point.y],**kwargs)

    def plot_directed(self,ax,**kwargs):
        dx = self.dst_point.x - self.src_point.x
        dy = self.dst_point.y - self.src_point.y
        ax.arrow(self.src_point.x,self.src_point.y,dx,dy,head_width=3,**kwargs)

    def __str__(self):
        return str(self.src_point) + ">>" + str(self.dst_point)

    def __eq__(self,edge):
        if isinstance(edge,Edge):
            return self.src_point == edge.src_point and self.dst_point == edge.dst_point
        if isinstance(edge,tuple):
            return self.src_point == edge[0] and self.dst_point == edge[1]

    def __repr__(self) -> str:
        return str(self)

    def __hash__(self):
        return hash((self.src_point,self.dst_point))

    def is_endpoint(self,point):
        return point == self.src_point or point == self.dst_point
    
    def find_intersection_point(self,edge):

        if not self.is_intersects(edge):
            return None

        self_line = Line(self.src_point,self.dst_point)
        other_line = Line(edge.src_point,edge.dst_point)
        inter_point = self_line.find_intersection(other_line)
        
        return inter_point

    def is_intersects(self,edge):
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

        return doIntersect(self.src_point,self.dst_point,edge.src_point,edge.dst_point)



class Graph(object):
    def __init__(self):
        self.edges = set()
        self.vertecies = set()
    
    def insert_vertex(self,vertex):
        self.vertecies.add(vertex)

    def insert_edge(self,edge):
        self.insert_vertex(edge.src_point)
        self.insert_vertex(edge.dst_point)
        self.edges.add(edge)

    def plot_undirected(self,ax):
        for e in self.edges:
            e.plot(ax)
        # Point.scatter_points(ax,self.vertecies)

    def plot_directed(self,ax,**kwargs):
        for e in self.edges:
            e.plot_directed(ax,**kwargs)
        # Point.scatter_points(ax,self.vertecies)

    def get_input_edges(self,dst_vertex):
        return [edge for edge in self.edges if edge.dst_point == dst_vertex]

    def get_output_edges(self,src_vertex):
        return [edge for edge in self.edges if edge.src_point == src_vertex]

    def get_edges(self):
        return self.edges

    def get_verticies(self):
        return self.vertecies

    def union(self,other):

        if isinstance(other,Polygon):
            verts = list(other.exterior.coords)
            for i in range(len(verts)-1):
                self.insert_edge(Edge(Point(verts[i]),Point(verts[i+1])))

        if isinstance(other,Graph):
            self.vertecies = self.vertecies.union(other.vertecies)
            self.edges = self.edges.union(other.edges)

    def get_copy(self):
        grph = Graph()
        grph.union(self)
        return grph

    def remove_edge(self,edge):
        self.edges.remove(edge)

        for vert in [edge.src_point,edge.dst_point]:
            vert_edges = self.get_input_edges(vert) + self.get_output_edges(vert)
            if len(vert_edges) == 0:
                self.vertecies.remove(vert)
            