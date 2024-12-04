from src.rgon_1988 import internals as Rgon1988Internals
from src.data_structures import Point
from src.data_structures.shapes import Polygon
from src.data_structures.graph import Graph,Edge
import re

'''
    Deprecated module
'''

# old - to delete
def mirror_y_axis(mirrored,direction):
    return mirrored
    # if direction.value == 1:
    #     return mirrored

    # if isinstance(mirrored,Point):
    #     return Point(-mirrored.x,mirrored.y)
    # if isinstance(mirrored,Polygon):
    #     coords = list(mirrored.exterior.coords)
    #     coords = [(-coor[0],coor[1]) for coor in coords]
    #     return Polygon(coords)
    # if isinstance(mirrored,Graph):
    #     grph_mirr = Graph()
        
    #     for edge in list(mirrored.get_edges()):
    #         edge_mirr = mirror_y_axis(edge,direction)
    #         grph_mirr.insert_edge(edge_mirr)

    #     return grph_mirr
    # if isinstance(mirrored,Edge):
    #     src_point = mirror_y_axis(mirrored.src_point,direction) 
    #     dst_point = mirror_y_axis(mirrored.dst_point,direction) 

    #     return Edge(src_point,dst_point)

def get_stared_shape_polygon(kernel_point,subspace_points,direction):
    kernel_point_mirr = mirror_y_axis(kernel_point,direction)
    subspace_points_mirr = [mirror_y_axis(point,direction) for point in subspace_points]
    stared_polygon = Rgon1988Internals.get_stared_shape_polygon(kernel_point_mirr,subspace_points_mirr)
    stared_polygon = mirror_y_axis(stared_polygon,direction)
    return stared_polygon

def get_visualization_graph(kernel_point,stared_polygon,direction):
    kernel_point_mirr = mirror_y_axis(kernel_point,direction)
    stared_polygon = mirror_y_axis(stared_polygon,direction)
    visual_graph = Rgon1988Internals.get_visualization_graph(kernel_point_mirr,stared_polygon)
    return mirror_y_axis(visual_graph,direction)

def get_convex_chain_connectivity(visual_graph,direction):
    visual_graph_mirr = mirror_y_axis(visual_graph,direction)
    connectivity = Rgon1988Internals.get_convex_chain_connectivity(visual_graph_mirr)

    if direction.value == 1:
        return connectivity

    connectivity_mirr = {}
    for edge_key in connectivity.keys():
        edge_key_mirr = re.sub("-","",edge_key) # This could be prolematic - str is ()--()
        connectivity_mirr[edge_key_mirr] = [mirror_y_axis(e,direction) for e in connectivity[edge_key]]
    
    return connectivity_mirr
