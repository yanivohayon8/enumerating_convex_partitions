from src.data_structures import Point, plot_polygons, poly_as_matplotlib, scatter_points
from src.data_structures.shapes import Polygon
from shapely.geometry import LineString


import pandas as pd

def collinear_(x1, y1, x2, y2, x3, y3,threshold=1e-3):
    """ Calculation the area of  
        triangle. We have skipped 
        multiplication with 0.5 to
        avoid floating point computations """
    a = x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)
    a = abs(a)
 
    if a < threshold:
        return True
    
    return False

def collinear_shapely_(p1,p2,p3,threshold=1e-3):
    # Create a LineString from the first two points
    line = LineString([p1, p2])
    # Check if the third point is on the line
    return line.distance(Point(p3)) < threshold


class Board():

    def __init__(self,interior_points=None,convex_hull_points=None,file_path=None) -> None:
        self.interior_points = []
        self.frame_anchor_points = [] #frame anchor points
        self.frame_polygon = None 
        self.space_points = []

        if file_path:
            self.load_sampled_points(file_path)
        else:
            self.interior_points =  sorted(interior_points,key=lambda p: p.x) if interior_points is not None else []
            self.frame_anchor_points = sorted(convex_hull_points,key=lambda p: p.x) if convex_hull_points is not None else []
            self.frame_polygon = Polygon(Polygon(convex_hull_points).convex_hull) if  len(convex_hull_points) > 2 else None
            self.space_points = sorted(self.interior_points + self.frame_anchor_points, key=lambda p: p.x)

        ''' Validity check '''
        # frame_anchor_points_cycle = self.frame_anchor_points + [self.frame_anchor_points[0]]

        # for i,ch_point_i in enumerate(self.frame_anchor_points):
        #     for ch_point_j in frame_anchor_points_cycle[i+1:]:

        #         for int_point in self.interior_points:
        #             collinear_simple = collinear_(ch_point_i.x,ch_point_i.y,ch_point_j.x,ch_point_j.y,int_point.x,int_point.y)
        #             collinear_shapely = collinear_shapely_(ch_point_i,ch_point_j,int_point)

        #             if collinear_simple or collinear_shapely:
        #                 raise ValueError(f"The points {ch_point_i},{ch_point_j},{int_point} collinear")

        


    def load_sampled_points(self,file_path):
        frame_points = []
        role_points = {
            "interior": self.interior_points,
            "frame_anchor":self.frame_anchor_points,
            "frame": frame_points
        }
        df = pd.read_csv(file_path,index_col=False)

        for row in df.to_numpy():

            if row[0] < 0 or row[1] < 0:
                raise ValueError(f"All points coordinates must not be negative. Recieved as input ({row[0]},{row[1]})")

            point = Point(row[0],row[1])
            role_points[row[2]].append(point)

        self.frame_polygon = Polygon(frame_points)
        self.interior_points = sorted(self.interior_points,key=lambda p: p.x)
        self.frame_anchor_points = sorted(self.frame_anchor_points,key=lambda p: p.x)
        self.space_points = sorted(self.interior_points + self.frame_anchor_points,key=lambda p: p.x)

    def plot(self,ax):
        scatter_points(ax,self.interior_points,color="blue",s=60)
        scatter_points(ax,self.frame_anchor_points,color="red",s=60)
        frame_mat_polygon = poly_as_matplotlib(self.frame_polygon,edgecolor="black",facecolor='white',lw=2)
        plot_polygons(ax,[frame_mat_polygon])

    def potential_points(self,kernel_point,space):
        return list(filter(lambda point: point.x>=kernel_point.x and point!=kernel_point,space ))