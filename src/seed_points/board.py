from src.data_structures import Point, plot_polygons, poly_as_matplotlib, scatter_points
from src.data_structures.shapes import Polygon


import pandas as pd


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
        scatter_points(ax,self.interior_points,color="blue")
        scatter_points(ax,self.frame_anchor_points,color="red")
        frame_mat_polygon = poly_as_matplotlib(self.frame_polygon,edgecolor="black",facecolor='white',lw=2)
        plot_polygons(ax,[frame_mat_polygon])

    def potential_points(self,kernel_point,space):
        return list(filter(lambda point: point.x>=kernel_point.x and point!=kernel_point,space ))