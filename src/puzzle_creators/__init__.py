from turtle import color
import pandas as pd
from src.data_structures import Point,Polygon
import matplotlib.pyplot as plt
import numpy as np


class PuzzleCreator():
    def __init__(self):
        self.interior_points = []
        self.border_points = []
        self.frame_points = []
    
    def load_sampled_points(self,file_path):
        role_points = {
            "interior":self.interior_points,
            "border":self.border_points,
            "frame":self.frame_points
        }
        df = pd.read_csv(file_path,index_col=False)

        for row in df.to_numpy():
            point = Point(row[0],row[1])
            role_points[row[2]].append(point)
        
    def plot_scratch(self,ax):
        '''
            Plot the border, frame, interior lines prior to the puzzle creation
        '''
        x_interior_points = [point.x for point in self.interior_points]
        y_interior_points = [point.y for point in self.interior_points]
        x_border_points = [point.x for point in self.border_points]
        y_border_points = [point.y for point in self.border_points]
        
        ax.scatter(x_interior_points,y_interior_points,color="blue")
        ax.scatter(x_border_points,y_border_points,color="red")

        '''
            use later for other implemntation methods:
            https://matplotlib.org/stable/gallery/shapes_and_collections/patch_collection.html#sphx-glr-gallery-shapes-and-collections-patch-collection-py
        '''
        
        frame_polygon = Polygon(self.frame_points)
        mat_polygon = frame_polygon.get_as_matplotlib()
        Polygon.plot_polygons(ax,[mat_polygon])

        # poly = [[1,1], [2,1], [2,2], [1,2], [0.5,1.5]]
        # frame = [[p.x,p.y] for p in self.frame_points]
        # ax.plot(*np.column_stack(frame+[frame[0]]))

