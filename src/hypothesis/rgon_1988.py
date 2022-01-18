from ..hypothesis import HypothesisAlgo
import numpy as np
from ..data_structure import Polygon
#import math


class Rgon1988(HypothesisAlgo):
    def __init__(self,interior_points,border_points):
        super().__init__(interior_points,border_points)

    def get_stared_shape_polygon(self,kernel_point,subspace_points):
        polygon = Polygon()
        polygon.add_vertex(kernel_point)
        points = {}
        pos_angles = []
        pos_angle_points = []
        neg_angles = []
        neg_angle_points = []
        for point in subspace_points: 
            angle = np.degrees(np.arctan((point[1]- kernel_point[1])/abs(kernel_point[0]-point[0])))

            if angle >0:
                pos_angles.append(angle)
                pos_angle_points.append(point)
            else:
                neg_angles.append(-angle)
                neg_angle_points.append(point)

        pos_angle_points = [polygon.add_vertex(point) for _,point in sorted(zip(pos_angles,pos_angle_points),reverse=True)]
        neg_angle_points = [polygon.add_vertex(point) for _,point in sorted(zip(neg_angles,neg_angle_points))]
        
        return polygon

    def get_points_horizontal_ahead(self,src_point,space_points,direction="left"):
        '''
            Returns the points that if the source point look at that direction - left/right
            it return the list of point that ahead of it
        '''
        filter_condition = lambda item: item[0]>=src_point[0] and item!=src_point    
        if direction == "right":
            filter_condition = lambda item: item[0]<=src_point[0] and item!=src_point    
        
        return list(filter(filter_condition,space_points))

    def get_visible_view_points(self,src_point,space_points):
        # you will need to filter here the subspace points 
        # according the view of the current point: 
        # it could be blocked by edges (and by direction)
        return space_points

    def get_visualization_graph():
        pass

    def run_algo(self):
        space_points = self.interior_points + self.border_points
        for interior_point in self.interior_points:

            points_ahead = self.get_points_horizontal_ahead(interior_point,space_points)            
            subspace = self.get_visible_view_points(interior_point,points_ahead)
            stared_polygon = self.get_stared_shape_polygon(interior_point,subspace)
    
