from shapely.geometry import Polygon as ShapelyPolygon
from functools import reduce

class Polygon(ShapelyPolygon):
    def __str__(self) -> str:
        xs,ys = self.exterior.coords.xy
        verticies = [(x,y) for x,y in zip(xs,ys)]
        return reduce(lambda acc,vert_str: acc + vert_str+";",\
                list(map(lambda x: str(x),verticies)),"")
    







# from src.data_structures.graph import Graph,Edge
# from matplotlib.patches import Polygon as MatplotlibPolygon
# from matplotlib.collections import PatchCollection
# from typing import List
# from functools import reduce

# class Polygon(object):
#     def __init__(self,*args):
#         if len(args) == 1:
#             self.vertcies = args[0]
#         else:
#             self.vertcies = []

#     def add_vertex(self,point):
#         if not point in self.vertcies:
#             self.vertcies.append(point)

#     def plot(self,ax,color="blue"):
#         verts = self.vertcies + [self.vertcies[0]]
#         xs = [p.x for p in verts]
#         ys = [p.y for p in verts]
#         ax.plot( xs,ys,color=color )
#         ax.scatter(xs,ys,color=color)

#     @staticmethod
#     def plot_polygons(ax,polygons:List[MatplotlibPolygon]):
#         '''
#             https://matplotlib.org/stable/gallery/shapes_and_collections/patch_collection.html#sphx-glr-gallery-shapes-and-collections-patch-collection-py
#         '''
#         # colors = 100 * np.random.rand(len(polygons))
#         p = PatchCollection(polygons,match_original=True,alpha=0.4) # alpha=0.4 ,edgecolor=[0.5,0.5,0.5]
#         # p.set_array(colors)
#         ax.add_collection(p)

#     def get_as_matplotlib(self,**kwargs) -> MatplotlibPolygon:
#         points_np = [vert.get_as_np() for vert in self.vertcies]
#         return MatplotlibPolygon(points_np,True,**kwargs)#  working: edgecolor=[0,0,0],color=None,lw=100)  ,color=[0.5,0.5,0.5],alpha=None)

#     def remove_vertex(self,point):
#         self.vertcies = list(filter(lambda p: not (p.x==point.x and p.y==point.y),self.vertcies))

#     def make_copy(self):
#         return Polygon(self.vertcies)
    
#     def reverse_direction(self):
#         self.vertcies.reverse()

#     def get_graph(self):
#         grph = Graph()
#         for i,vert in enumerate(self.vertcies):
#             # grph.insert_vertex(vert)
#             next_vert = self.vertcies[(i+1)%len(self.vertcies)]
#             grph.insert_edge(Edge(vert,next_vert))
#         return grph

#     def __str__(self) -> str:
#         return reduce(lambda acc,vert_str: acc + vert_str+";",list(map(lambda x: str(x),self.vertcies)),"")
# #

#     # def is_contain(self,other_polygon):
#     #     if other