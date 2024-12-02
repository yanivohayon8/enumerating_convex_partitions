import unittest

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import pandas as pd
from src.rgon_1988 import internals as Rgon1988Internals
import matplotlib.pyplot as plt
from  src.consts import PLOT_COLORS
import matplotlib.patches as patches
from src.data_structures import Point
from src.data_structures.shapes import Polygon
from src.data_structures.graph import Graph,Edge
from src.puzzle_creators.utils import surface


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


class TestRgonInternalOLD(unittest.TestCase):

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


class TestInternals(unittest.TestCase):

    def test_star_shaped_polygon_1(self):
        kernel = Point(474.0,320.0)

        _, axs = plt.subplots(1,2)
        axs[0].scatter([kernel.x],[kernel.y],color="green",marker="o")
        axs[1].scatter([kernel.x],[kernel.y],color="green",marker="o")

        candidates1 = [Point(1107.0,314.0),Point(593.0,707.0),Point(1410.0,661.0)] 
        star_polygon1 = Rgon1988Internals.get_stared_shape_polygon(kernel,candidates1)
        xs,ys = star_polygon1.exterior.coords.xy
        axs[0].plot(xs,ys,color="red")

        candidates2 = [Point(593.0,707.0),Point(1107.0,314.0),Point(1410.0,661.0)] 
        star_polygon2 = Rgon1988Internals.get_stared_shape_polygon(kernel,candidates2)
        xs,ys = star_polygon2.exterior.coords.xy
        axs[1].plot(xs,ys,color="red")

        plt.show()

        assert star_polygon1 == star_polygon2

    def test_visualization_graph_1(self):
        kernel = Point(474.0,320.0)
        star_shaped_polygon = Polygon([Point(474.0,320.0),Point(593.0,707.0),Point(1410.0,661.0),Point(1107.0,314.0)])

        visibility_graph = Rgon1988Internals.get_visualization_graph(kernel,star_shaped_polygon)

        ax = plt.subplot()
        star_xs,star_ys = star_shaped_polygon.exterior.coords.xy
        ax.plot(star_xs,star_ys,"r--")
        ax.scatter(star_xs,star_ys,color="blue")
        visibility_graph.plot_directed(ax,linewidth=3)

        plt.show()

        assert len(visibility_graph.get_edges())==3

    def test_convex_chain_connectivity(self):
        visibility_graph = Graph()
        e1 = Edge(Point(1107.0,314.0),Point(593.0,707.0))
        visibility_graph.insert_edge(e1)
        e2 = Edge(Point(1107.0,314.0),Point(1410.0,661.0))
        visibility_graph.insert_edge(e2)
        e3 = Edge(Point(1410.0,661.0),Point(593.0,707.0))
        visibility_graph.insert_edge(e3)

        continuity_edges = Rgon1988Internals.get_convex_chain_connectivity(visibility_graph)
        print(continuity_edges)

        ax = plt.subplot()
        visibility_graph.plot_directed(ax,linewidth=1.5)
        plt.show()

        assert len(continuity_edges[str(e1)])==0
        assert continuity_edges[str(e2)]==[e3]
        assert len(continuity_edges[str(e3)])==0


class TestSurface(unittest.TestCase):
    
    def test_compute_visibility_graph(self):
        kernel = Point(467.0,477.0)
        candidates = [Point(961.0,167.0),Point(600.0,213.0),Point(779.0,693.0),Point(1049.0,661.0),Point(1154.0,322.0)]
        star_shaped_polygon = Rgon1988Internals.get_stared_shape_polygon(kernel,candidates)
        visibility_graph = Rgon1988Internals.get_visualization_graph(kernel,star_shaped_polygon)

        ax = plt.subplot()
        star_xs,star_ys = star_shaped_polygon.exterior.coords.xy
        ax.plot(star_xs,star_ys,"r--")
        ax.scatter(star_xs,star_ys,color="blue")
        visibility_graph.plot_directed(ax,linewidth=3)

        plt.show()

        assert len(visibility_graph.get_edges())==10 # = 5 choose 2

    def test_traverses(self):
        continuity_edges = {
            'POINT (1107 314)>>POINT (593 707)': [],
            'POINT (1107 314)>>POINT (1410 661)': [Edge(Point(1410,661),Point(593,707))],
              'POINT (1410 661)>>POINT (593 707)': []
        }

        edges = [Edge(Point(1107.0,314.0),Point(593.0,707.0)),
                 Edge(Point(1107.0,314.0),Point(1410.0,661.0)),
                    Edge(Point(1410.0,661.0),Point(593.0,707.0))]

        for edge in edges:
            traverses = surface._get_traverse(edge,continuity_edges)

            print(f"for edge {edge} the traverses are the following")
            [print(f"\t{trav}") for trav in traverses]




        



if __name__ == "__main__":
    unittest.main()