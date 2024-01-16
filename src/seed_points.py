import pandas as pd
from shapely.geometry import MultiPoint
from src.data_structures.shapes import Polygon
from src.data_structures import Point
import random


class SeedPointsParent():
    
    def __init__(self,save_file_path=None) -> None:
        self.save_file_path = save_file_path

    def _sample_points(self,**_ignored)->MultiPoint:
        raise NotImplementedError("Implement me in child class")

    def _sort_points_role(self,sampled_points:MultiPoint):
        convex_hull = sampled_points.convex_hull
        interior_points = [point for point in sampled_points if not convex_hull.touches(point)]
        convex_hull_points = MultiPoint(list(Polygon(sampled_points.convex_hull).exterior.coords)[:-1])

        return interior_points,convex_hull_points
    
    def _wrap_output(self,internal_points,convex_hull_points)->pd.DataFrame:
        ''''
            internal_points - list or shapely MultiPoint
            convex_hull_points - list
        '''
        xs = []
        ys = []
        roles = []
        for p in internal_points:
            xs.append(p.x)
            ys.append(p.y)
            roles.append("interior")

        for p in convex_hull_points:
            xs.append(p.x)
            ys.append(p.y)
            roles.append("convex_hull")
        
        df = pd.DataFrame(data={
            "x": xs,
            "y":ys,
            "role":roles
        })
        
        return df
    
    def run(self,**kwargs):
        sampled_points = self._sample_points(**kwargs)
        
        interior_points,convex_hull_points = self._sort_points_role(sampled_points)
        df = self._wrap_output(interior_points,convex_hull_points)

        if not self.save_file_path is None:
            pass # save to file the df

        return df
    
class InputRangeGenerator(SeedPointsParent):

    def _sample_points(self,n_points,x_max, y_max,x_min=0, y_min=0, **_ignored)->MultiPoint:
        sampled_points_tmp = []
    
        for _ in range(n_points):
            x = random.uniform(x_min,x_max)
            y = random.uniform(y_min,y_max)
            sampled_points_tmp.append(Point((x,y)))

        return MultiPoint(sampled_points_tmp)
    

class ImageRangeGenerator(SeedPointsParent):

    def _sample_points(self, **_ignored)->MultiPoint:
        pass


