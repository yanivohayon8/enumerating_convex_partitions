import numpy as np
from matplotlib.patches import Polygon as MatplotlibPolygon
from matplotlib.collections import PatchCollection
from typing import List
from functools import reduce

class Point(object):
    def __init__(self,x,y): #*args):
        self.x = float(round(x,2))
        self.y = float(round(y,2))
        # if len(args) == 2:
        #     self.x = args[0]
        #     self.y = args[1]
        # if len(args) == 1:
        #     tuple_ = eval(args[0])
        #     self.x = args[tuple_[0]]
        #     self.y = args[tuple_[1]]

    def get_as_tuple(self):
        return (self.x,self.y)

    def get_as_np(self):
        return np.asarray([self.x,self.y])

    def __eq__(self,p):
        return self.x==p.x and self.y==p.y
    
    def __ne__(self,p):
        return not (self.x == p.x and self.y==p.y)
    
    def __hash__(self):
        return hash(self.get_as_tuple())

    @staticmethod
    def scatter_points(ax,points,color="blue"):
        xs = [point.x for point in points]
        ys = [point.y for point in points]

        ax.scatter(xs,ys,color=color)

    def __sub__(self,p):
        if isinstance(p, Point):
            return Point(self.x-p.x,self.y-p.y)

    def __str__(self):
        return "({0},{1})".format(self.x,self.y) #"(" + str(self.x) +","+str(self.y)+")"




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

    def plot_directed(self,ax):
        dx = self.dst_point.x - self.src_point.x
        dy = self.dst_point.y - self.src_point.y
        ax.arrow(self.src_point.x,self.src_point.y,dx,dy,head_width=0.2)

    def __str__(self):
        return str(self.src_point) + "->" + str(self.dst_point)

    def __eq__(self,edge):
        return self.src_point == edge.src_point and self.dst_point == edge.dst_point
    
    def __hash__(self):
        return hash((self.src_point,self.dst_point))

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
        Point.scatter_points(ax,self.vertecies)

    def plot_directed(self,ax):
        for e in self.edges:
            e.plot_directed(ax)
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
            


class Polygon(object):
    def __init__(self,*args):
        if len(args) == 1:
            self.vertcies = args[0]
        else:
            self.vertcies = []

    def add_vertex(self,point):
        if not point in self.vertcies:
            self.vertcies.append(point)

    def plot(self,ax,color="blue"):
        verts = self.vertcies + [self.vertcies[0]]
        xs = [p.x for p in verts]
        ys = [p.y for p in verts]
        ax.plot( xs,ys,color=color )
        ax.scatter(xs,ys,color=color)

    @staticmethod
    def plot_polygons(ax,polygons:List[MatplotlibPolygon]):
        '''
            https://matplotlib.org/stable/gallery/shapes_and_collections/patch_collection.html#sphx-glr-gallery-shapes-and-collections-patch-collection-py
        '''
        # colors = 100 * np.random.rand(len(polygons))
        p = PatchCollection(polygons,match_original=True,alpha=0.4) # alpha=0.4 ,edgecolor=[0.5,0.5,0.5]
        # p.set_array(colors)
        ax.add_collection(p)

    def get_as_matplotlib(self,**kwargs) -> MatplotlibPolygon:
        points_np = [vert.get_as_np() for vert in self.vertcies]
        return MatplotlibPolygon(points_np,True,**kwargs)#  working: edgecolor=[0,0,0],color=None,lw=100)  ,color=[0.5,0.5,0.5],alpha=None)

    def remove_vertex(self,point):
        self.vertcies = list(filter(lambda p: not (p.x==point.x and p.y==point.y),self.vertcies))

    def make_copy(self):
        return Polygon(self.vertcies)
    
    def reverse_direction(self):
        self.vertcies.reverse()

    def get_graph(self):
        grph = Graph()
        for i,vert in enumerate(self.vertcies):
            # grph.insert_vertex(vert)
            next_vert = self.vertcies[(i+1)%len(self.vertcies)]
            grph.insert_edge(Edge(vert,next_vert))
        return grph

    def __str__(self) -> str:
        return reduce(lambda acc,vert_str: acc + vert_str+";",list(map(lambda x: str(x),self.vertcies)),"")
