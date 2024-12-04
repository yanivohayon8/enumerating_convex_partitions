from shapely.geometry import Point as ShapelyPoint

from matplotlib.patches import Polygon as MatplotlibPolygon
from matplotlib.collections import PatchCollection
from typing import List
import numpy as np

class Point(ShapelyPoint):
    def __sub__(self,other):
        return Point(self.x-other.x,self.y-other.y)


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
    p = PatchCollection(polygons,match_original=True,alpha=0.4)
    ax.add_collection(p)

def poly_as_matplotlib(polygon,**kwargs) -> MatplotlibPolygon:
    points_np = [point_to_np(Point(vert)) for vert in list(polygon.exterior.coords)]
    return MatplotlibPolygon(points_np,True,**kwargs)