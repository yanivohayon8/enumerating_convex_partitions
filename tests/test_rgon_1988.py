import unittest

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import pandas as pd
from src.hypothesis import internals as Rgon1988Internals
import matplotlib.pyplot as plt
from  src.consts import PLOT_COLORS
import matplotlib.patches as patches
from src.data_structures import Point



def load_sampling_csv(path):
    df = pd.read_csv(path,index_col=False)
    df_points_interior = df.loc[df["role"]=="interior"]
    df_points_border = df.loc[df["role"]=="border"]
    return df_points_interior,df_points_border


def get_border_dim(df_border):
    return (df_border["x"]).max(),(df_border["y"]).max()

def df_to_array(df):
    return [Point(row[0],row[1]) for row in df.to_numpy()]

def plot_sampled_point(fig,ax,x_interior_points, y_interior_points,
                        x_border_length, y_border_length):
                        #border_width, border_height,border_start_point=(1,1)):
    '''
        This method need to be removed or be splitted to multiple methods
        some like scatter points in Point class
    '''
    ax.scatter(x_interior_points, y_interior_points)    

    # This is hard coded
    border_frame = patches.Rectangle((0,0), x_border_length, y_border_length, linewidth=1,
                        edgecolor='r', facecolor="none")

    ax.add_patch(border_frame)


class TestRgonInternal(unittest.TestCase):

    def test_load_csv_and_scatter(self):
        df_points_interior,df_points_border = load_sampling_csv("data/starting_points/old/sampling_002.csv")
        
        interior_points = df_to_array(df_points_interior[["x","y"]])
        border_points = df_to_array(df_points_border[["x","y"]])
        x_border_length, y_border_length = get_border_dim(df_points_border)
        x_interior_points = [point.x for point in interior_points]
        y_interior_points = [point.y for point in interior_points]

        fig, ax = plt.subplots()
        plot_sampled_point(fig,ax,x_interior_points,y_interior_points,x_border_length,y_border_length)
        plt.show()

    def test_draw_stared_shaped_polygon(self):
        df_points_interior,df_points_border = load_sampling_csv("data/starting_points/old/sampling_002.csv")
        
        x_border_length, y_border_length = get_border_dim(df_points_border)

        interior_points = df_to_array(df_points_interior[["x","y"]])
        border_points = df_to_array(df_points_border[["x","y"]])
        x_interior_points = [point.x for point in interior_points]
        y_interior_points = [point.y for point in interior_points]


        space_points = interior_points +  border_points
        interior_point = interior_points[0]
        points_ahead = Rgon1988Internals.get_points_horizontal_ahead(interior_point,space_points)            
        stared_polygon = Rgon1988Internals.get_stared_shape_polygon(interior_point,points_ahead)

        fig, ax = plt.subplots()
        
        # stared_polygon.plot(ax)
        plt.plot(*stared_polygon.exterior.xy)
        plot_sampled_point(fig,ax,x_interior_points,y_interior_points,x_border_length,y_border_length)
        plt.show()

    def test_draw_visualization_graph(self):
        df_points_interior,df_points_border = load_sampling_csv("data/starting_points/old/sampling_002.csv")
        
        x_border_length, y_border_length = get_border_dim(df_points_border)

        interior_points = df_to_array(df_points_interior[["x","y"]])
        border_points = df_to_array(df_points_border[["x","y"]])
        x_interior_points = [point.x for point in interior_points]
        y_interior_points = [point.y for point in interior_points]

        space_points =interior_points + border_points #interior_points 
        interior_point = interior_points[0]
        points_ahead = Rgon1988Internals.get_points_horizontal_ahead(interior_point,space_points)            
        stared_polygon = Rgon1988Internals.get_stared_shape_polygon(interior_point,points_ahead)

        fig, axs = plt.subplots(1,3)
        # stared_polygon.plot(axs[0])
        axs[0].plot(*stared_polygon.exterior.xy)
        plot_sampled_point(fig,axs[0],x_interior_points,y_interior_points,x_border_length,y_border_length)

        graph = Rgon1988Internals.get_visualization_graph(interior_point,stared_polygon)
        graph.plot_undirected(axs[1])
        graph.plot_directed(axs[2])

        fig_, axs_ = plt.subplots()
        plot_sampled_point(fig_,axs_,x_interior_points,y_interior_points,x_border_length,y_border_length)

        graph = Rgon1988Internals.get_visualization_graph(interior_point,stared_polygon)
        # nx.draw(graph)
        graph.plot_directed(axs_)
        # plot_graph(graph)

        plt.show()


if __name__ == "__main__":
    unittest.main()