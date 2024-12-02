from shapely.geometry import Point as ShapelyPoint

from matplotlib.patches import Polygon as MatplotlibPolygon
from matplotlib.collections import PatchCollection
from typing import List
import numpy as np

class Point(ShapelyPoint):

    def __hash__(self) -> int:
        # return super().__hash__()
        return hash((self.x,self.y))

    def __sub__(self,other):
        return Point(self.x-other.x,self.y-other.y)
    
    # Changing str might be dangerous
    def __str__(self):
        return "({0},{1})".format(self.x,self.y) 

    def __repr__(self) -> str:
        return str(self)

def scatter_points(ax,points,**kwargs):
    xs = [point.x for point in points]
    ys = [point.y for point in points]

    ax.scatter(xs,ys,**kwargs)

def point_to_np(point):
    return np.asarray([point.x,point.y])


def remove_prefix_(point_str:str):
    # To adjust shapely 2.0
    paranthesis_index = point_str.index("(")
    no_prefix = point_str[paranthesis_index:]
    no_prefix = no_prefix.replace(" ",",")
    
    return no_prefix


'''Polygon '''

def plot_polygons(ax,polygons:List[MatplotlibPolygon]):
    '''
        https://matplotlib.org/stable/gallery/shapes_and_collections/patch_collection.html#sphx-glr-gallery-shapes-and-collections-patch-collection-py
    '''
    # colors = 100 * np.random.rand(len(polygons))
    p = PatchCollection(polygons,match_original=True,alpha=0.4) # alpha=0.4 ,edgecolor=[0.5,0.5,0.5]
    # p.set_array(colors)
    ax.add_collection(p)

def poly_as_matplotlib(polygon,**kwargs) -> MatplotlibPolygon:
    points_np = [point_to_np(Point(vert)) for vert in list(polygon.exterior.coords)]
    return MatplotlibPolygon(points_np,True,**kwargs)#  working: edgecolor=[0,0,0],color=None,lw=100)  ,color=[0.5,0.5,0.5],alpha=None)









'''Old: '''
# import networkx as nx

# # maybe need to inherent from shapley point and ovveride __sub__ operator
# def substract_points(point_from,point_to):
#     '''
#         This function takes 2 Points(shapely) and return point_to - point_from
#         This method was made because of the wrong result tested when making directly point_to-point_from (sub operator)
#     '''
#     _from = list(point_from.xy)
#     _to = list(point_to.xy)

#     return Point(_to[0][0]-_from[0][0],_to[1][0]-_from[1][0])


# def plot_graph(graph,**kwargs):
#     nx.draw(graph,**kwargs)
'''More old:'''
# import numpy as np


# class Point(object):
#     def __init__(self,x,y): #*args):
#         self.x = float(round(x,2))
#         self.y = float(round(y,2))
#         # if len(args) == 2:
#         #     self.x = args[0]
#         #     self.y = args[1]
#         # if len(args) == 1:
#         #     tuple_ = eval(args[0])
#         #     self.x = args[tuple_[0]]
#         #     self.y = args[tuple_[1]]

#     def get_as_tuple(self):
#         return (self.x,self.y)

#     def get_as_np(self):
#         return np.asarray([self.x,self.y])

#     def __eq__(self,p):
#         return self.x==p.x and self.y==p.y
    
#     def __ne__(self,p):
#         return not (self.x == p.x and self.y==p.y)
    
#     def __hash__(self):
#         return hash(self.get_as_tuple())

#     @staticmethod
#     def scatter_points(ax,points,color="blue"):
#         xs = [point.x for point in points]
#         ys = [point.y for point in points]

#         ax.scatter(xs,ys,color=color)

#     def __sub__(self,p):
#         if isinstance(p, Point):
#             return Point(self.x-p.x,self.y-p.y)

#     def __str__(self):
#         return "({0},{1})".format(self.x,self.y) #"(" + str(self.x) +","+str(self.y)+")"




