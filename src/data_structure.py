

class Point():
    def __init__(self,x,y): #*args):
        self.x = x 
        self.y = y
        # if len(args) == 2:
        #     self.x = args[0]
        #     self.y = args[1]
        # if len(args) == 1:
        #     tuple_ = eval(args[0])
        #     self.x = args[tuple_[0]]
        #     self.y = args[tuple_[1]]

    def get_as_tuple(self):
        return (self.x,self.y)

    @staticmethod
    def scatter_points(ax,points):
        xs = [point.x for point in points]
        ys = [point.y for point in points]

        ax.scatter(xs,ys)

    def __sub__(self,p):
        if isinstance(p, Point):
            return Point(self.x-p.x,self.y-p.y)

    def __str__(self):
        return "(" + str(self.x) +","+str(self.y)+")"

class Edge():
    def __init__(self,*args):
        if len(args)==2: # (src_point,dst_point)dsf
            self.src_point = args[0]#.src_point
            self.dst_point = args[1]#.dst_point
        if len(args) == 1: # ("(x_src,y_src)->(x_dst,y_dst)")
            tuple_0 =  eval(args[0].split("->")[0])
            tuple_1 = eval(args[0].split("->")[1])
            self.src_point = Point(tuple_0[0],tuple_0[1])
            self.dst_point = Point(tuple_1[0],tuple_1[1])
    
    def plot(self,ax):
        ax.plot([self.src_point.x,self.dst_point.x], [self.src_point.y,self.dst_point.y],"o-")

    def plot_directed(self,ax):
        dx = self.dst_point.x - self.src_point.x
        dy = self.dst_point.y - self.src_point.y
        ax.arrow(self.src_point.x,self.src_point.y,dx,dy,head_width=0.2)

    def __str__(self):
        return str(self.src_point) + "->" + str(self.dst_point)

class Graph():
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
        Point.scatter_points(ax,self.vertecies)

    def plot_directed(self,ax):
        for e in self.edges:
            e.plot_directed(ax)
        # Point.scatter_points(ax,self.vertecies)

    def get_input_edges(self,dst_vertex):
        return [edge for edge in self.edges if edge.dst_point == dst_vertex]

    def get_output_edges(self,src_vertex):
        return [edge for edge in self.edges if edge.src_point == src_vertex]


class Polygon():
    def __init__(self,*args):
        if len(args) == 1:
            self.vertcies = args[0]
        else:
            self.vertcies = []

    def add_vertex(self,point):
        self.vertcies.append(point)

    def plot(self,ax,color="blue"):
        verts = self.vertcies + [self.vertcies[0]]
        xs = [p.x for p in verts]
        ys = [p.y for p in verts]
        ax.plot( xs,ys,color=color )
        ax.scatter(xs,ys,color=color)

    def remove_vertex(self,point):
        self.vertcies = list(filter(lambda p: not (p.x==point.x and p.y==point.y),self.vertcies))

    def make_copy(self):
        return Polygon(self.vertcies)
    
    def reverse_direction(self):
        self.vertcies.reverse()