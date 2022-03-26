from shapely.geometry import Point
from src.data_structures.lines import Line


class Edge(object):
    def __init__(self,*args):
        if len(args)==2: # (src_point,dst_point)dsf
            self.src_point = args[0]#.src_point
            self.dst_point = args[1]#.dst_point
        if len(args) == 1: # ("(x_src,y_src)->(x_dst,y_dst)")
            tuple_0 =  eval(args[0].split("->")[0])
            tuple_1 = eval(args[0].split("->")[1])
            self.src_point = Point(tuple_0[0],tuple_0[1])
            self.dst_point = Point(tuple_1[0],tuple_1[1])

        if self.src_point == self.dst_point:
            raise ValueError(f"Tried to create edge with the same src_point and dst_point value ({str(self.src_point)})")
    
    def plot(self,ax):
        ax.plot([self.src_point.x,self.dst_point.x], [self.src_point.y,self.dst_point.y],"o-")

    def plot_directed(self,ax,**kwargs):
        dx = self.dst_point.x - self.src_point.x
        dy = self.dst_point.y - self.src_point.y
        ax.arrow(self.src_point.x,self.src_point.y,dx,dy,head_width=0.2,**kwargs)

    def __str__(self):
        return str(self.src_point) + "->" + str(self.dst_point)

    def __eq__(self,edge):
        return self.src_point == edge.src_point and self.dst_point == edge.dst_point
    
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

    def union(self,graph):
        self.vertecies = self.vertecies.union(graph.vertecies)
        self.edges = self.edges.union(graph.edges)
        # for vert in graph.vertecies:
        #     self.insert_vertex(vert)
        # for edge in graph.edges:
        #     self.insert_edge(edge)

    def get_copy(self):
        grph = Graph()
        grph.union(self)
        return grph

    def remove_edge(self,edge):
        pass
            