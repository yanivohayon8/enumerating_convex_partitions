from src.hypothesis import rgon_1988 as Rgon1988
from src.data_structures import Point
from src.data_structures.shapes import Polygon
# from src.puzzle_creators import Direction
from src.data_structures.graph import Graph,Edge
import re


# direction = Direction.left

def mirror_y_axis(mirrored,direction):
    if direction.value == 1:
        return mirrored

    if isinstance(mirrored,Point):
        return Point(-mirrored.x,mirrored.y)
    if isinstance(mirrored,Polygon):
        coords = list(mirrored.exterior.coords)
        coords = [(-coor[0],coor[1]) for coor in coords]
        return Polygon(coords)
    if isinstance(mirrored,Graph):
        grph_mirr = Graph()
        # for vert in list(mirrored.get_verticies()):
        #     vert_mirr = mirror_y_axis(vert)
        #     grph_mirr.insert_vertex(vert_mirr)

        for edge in list(mirrored.get_edges()):
            edge_mirr = mirror_y_axis(edge,direction)
            grph_mirr.insert_edge(edge_mirr)

        return grph_mirr
    if isinstance(mirrored,Edge):
        src_point = mirror_y_axis(mirrored.src_point,direction) #Point(-mirrored.src_point.x,mirrored.src_point.y)
        dst_point = mirror_y_axis(mirrored.dst_point,direction) #Point(-mirrored.dst_point.x,mirrored.dst_point.y)

        return Edge(src_point,dst_point)

def get_stared_shape_polygon(kernel_point,subspace_points,direction):
    kernel_point_mirr = mirror_y_axis(kernel_point,direction)
    subspace_points_mirr = [mirror_y_axis(point,direction) for point in subspace_points]
    stared_polygon = Rgon1988.get_stared_shape_polygon(kernel_point_mirr,subspace_points_mirr)
    stared_polygon = mirror_y_axis(stared_polygon,direction)
    return stared_polygon

def get_visualization_graph(kernel_point,stared_polygon,direction):
    kernel_point_mirr = mirror_y_axis(kernel_point,direction)
    stared_polygon = mirror_y_axis(stared_polygon,direction)
    visual_graph = Rgon1988.get_visualization_graph(kernel_point_mirr,stared_polygon)
    return mirror_y_axis(visual_graph,direction)

def get_convex_chain_connectivity(visual_graph,direction):
    visual_graph_mirr = mirror_y_axis(visual_graph,direction)
    connectivity = Rgon1988.get_convex_chain_connectivity(visual_graph_mirr)

    if direction.value == 1:
        return connectivity

    connectivity_mirr = {}
    for edge_key in connectivity.keys():
        edge_key_mirr = re.sub("-","",edge_key) # This could be prolematic - str is ()--()
        connectivity_mirr[edge_key_mirr] = [mirror_y_axis(e,direction) for e in connectivity[edge_key]]
    
    return connectivity_mirr

def get_edges_max_chain_length_new(kernel_point,visual_graph,continuity_edges):
    return Rgon1988.get_edges_max_chain_length_new(kernel_point,visual_graph,continuity_edges)

# def calc_angle_around_point(center_point,peripheral_point,epsilon = 0.00001):
#     return Rgon1988.calc_angle_around_point(center_point,peripheral_point,epsilon=epsilon)
def sort_points_clockwise(center_point,subspace_points):
    return Rgon1988.sort_points_clockwise(center_point,subspace_points)