from ..hypothesis import HypothesisAlgo
from ..hypothesis import rgon_1988  as Rgon1988

class FirstHypo(HypothesisAlgo):
    """
        This class implements my first idea.
        Scanning from left to right and then the opposite.
        Each scan random polygon from each point...
    """
    def __init__(self,interior_points,border_points):
        super().__init__(interior_points,border_points)


    def get_visible_view_points(src_point,space_points):
        # you will need to filter here the subspace points 
        # according the view of the current point: 
        # it could be blocked by edges (and by direction)
        return space_points

    def run_algo(self):
        pass
        ''' space_points = self.interior_points + self.border_points
        for interior_point in self.interior_points:

            points_ahead = self.get_points_horizontal_ahead(interior_point,space_points)            
            subspace = self.get_visible_view_points(interior_point,points_ahead)
            stared_polygon = self.get_stared_shape_polygon(interior_point,subspace)'''