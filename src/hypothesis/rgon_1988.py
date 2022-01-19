from ..hypothesis import HypothesisAlgo
import numpy as np
from ..data_structure import Polygon,Point,Edge,Graph


''' Maybe transfer'''


def get_stared_shape_polygon(kernel_point,subspace_points):
    polygon = Polygon()
    polygon.add_vertex(kernel_point)
    points = {}
    pos_angles = []
    pos_angle_points = []
    neg_angles = []
    neg_angle_points = []
    for point in subspace_points: 
        angle = np.degrees(np.arctan((point.y- kernel_point.y)/abs(kernel_point.x-point.x)))

        if angle >0:
            pos_angles.append(angle)
            pos_angle_points.append(point.get_as_tuple())
        else:
            neg_angles.append(-angle)
            neg_angle_points.append(point.get_as_tuple())

    pos_angle_points = [polygon.add_vertex(Point(point[0],point[1])) for _,point in sorted(zip(pos_angles,pos_angle_points),reverse=True)]
    neg_angle_points = [polygon.add_vertex(Point(point[0],point[1])) for _,point in sorted(zip(neg_angles,neg_angle_points))]
    
    return polygon

def get_points_horizontal_ahead(src_point,space_points,direction="left"):
    '''
        Returns the points that if the source point look at that direction - left/right
        it return the list of point that ahead of it
    '''
    filter_condition = lambda item: item.x>=src_point.x and item!=src_point    
    if direction == "right":
        filter_condition = lambda item: item.x<=src_point.x and item!=src_point    
    
    return list(filter(filter_condition,space_points))



def get_visualization_graph(kernel_point,stared_polygon):
    '''
        This method implement the "Visibility" procedure in the rgon paper

    '''
    copy_polygon = stared_polygon.make_copy()
    copy_polygon.reverse_direction() # This is under the assumption it came from came stared polygon function above
    copy_polygon.remove_vertex(kernel_point)
    points_queues = [[]] * len(copy_polygon.vertcies)
    grph = Graph()

    for index in range(len(copy_polygon.vertcies[:-1])):
        grph,points_queues = get_visualization_graph_proceed(index,index+1,stared_polygon,points_queues,grph)
    
    return grph
    
    
def get_visualization_graph_proceed(i_index,j_index,stared_polygon,points_queues,grph):
    '''
        This method implement the proceed method in  "Visibility" procedure in the rgon paper
    '''
    
    def turn(_i,_j,_k):
        i_to_j  = _j -_i 
        i_to_k = _k - _i
        determinant = i_to_j.x*i_to_k.y - i_to_k.x*i_to_j.y
        return np.sign(determinant)


    while len(points_queues[i_index])>0:
        k_index = points_queues[i_index][0]
        _i = stared_polygon.vertcies[i_index]
        _j = stared_polygon.vertcies[j_index]
        _k = stared_polygon.vertcies[k_index]

        if turn(_i,_j,_k) > 0:
            grph,points_queues = get_visualization_graph_proceed(k_index,j_index,
                                                        stared_polygon,points_queues,grph)
            points_queues[i_index].pop(0)
        else:
            break

    grph.insert_edge(Edge(stared_polygon.vertcies[i_index],stared_polygon.vertcies[j_index]))
    points_queues[j_index] =  points_queues[j_index] + [i_index]

    return grph,points_queues
    #verticies = stared_polygon.

    
