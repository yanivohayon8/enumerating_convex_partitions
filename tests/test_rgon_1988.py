import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import src.sampled_points as sampled_points
from src.hypothesis import rgon_1988 as Rgon1988
import matplotlib.pyplot as plt
from  src.consts import PLOT_COLORS

import networkx as nx

# from src.data_structures import plot_graph

def load_csv_and_scatter():
    df_points_interior,df_points_border = sampled_points.load_sampling_csv("data/starting_points/old/sampling_002.csv")
    
    interior_points = sampled_points.df_to_array(df_points_interior[["x","y"]])
    border_points = sampled_points.df_to_array(df_points_border[["x","y"]])
    x_border_length, y_border_length = sampled_points.get_border_dim(df_points_border)
    x_interior_points = [point.x for point in interior_points]
    y_interior_points = [point.y for point in interior_points]

    fig, ax = plt.subplots()
    sampled_points.plot_sampled_point(fig,ax,x_interior_points,y_interior_points,x_border_length,y_border_length)
    plt.show()

def draw_stared_shaped_polygon():
    df_points_interior,df_points_border = sampled_points.load_sampling_csv("data/starting_points/old/sampling_002.csv")
    
    x_border_length, y_border_length = sampled_points.get_border_dim(df_points_border)

    interior_points = sampled_points.df_to_array(df_points_interior[["x","y"]])
    border_points = sampled_points.df_to_array(df_points_border[["x","y"]])
    x_interior_points = [point.x for point in interior_points]
    y_interior_points = [point.y for point in interior_points]


    space_points = interior_points +  border_points
    interior_point = interior_points[0]
    points_ahead = Rgon1988.get_points_horizontal_ahead(interior_point,space_points)            
    stared_polygon = Rgon1988.get_stared_shape_polygon(interior_point,points_ahead)

    fig, ax = plt.subplots()
    
    # stared_polygon.plot(ax)
    plt.plot(*stared_polygon.exterior.xy)
    sampled_points.plot_sampled_point(fig,ax,x_interior_points,y_interior_points,x_border_length,y_border_length)
    plt.show()

def draw_visualization_graph():
    df_points_interior,df_points_border = sampled_points.load_sampling_csv("data/starting_points/old/sampling_002.csv")
    
    x_border_length, y_border_length = sampled_points.get_border_dim(df_points_border)

    interior_points = sampled_points.df_to_array(df_points_interior[["x","y"]])
    border_points = sampled_points.df_to_array(df_points_border[["x","y"]])
    x_interior_points = [point.x for point in interior_points]
    y_interior_points = [point.y for point in interior_points]

    space_points =interior_points + border_points #interior_points 
    interior_point = interior_points[0]
    points_ahead = Rgon1988.get_points_horizontal_ahead(interior_point,space_points)            
    stared_polygon = Rgon1988.get_stared_shape_polygon(interior_point,points_ahead)

    fig, axs = plt.subplots(1,3)
    # stared_polygon.plot(axs[0])
    axs[0].plot(*stared_polygon.exterior.xy)
    sampled_points.plot_sampled_point(fig,axs[0],x_interior_points,y_interior_points,x_border_length,y_border_length)

    graph = Rgon1988.get_visualization_graph(interior_point,stared_polygon)
    graph.plot_undirected(axs[1])
    graph.plot_directed(axs[2])

    # fig, axs = plt.subplots()
    # sampled_points.plot_sampled_point(fig,axs,x_interior_points,y_interior_points,x_border_length,y_border_length)

    # graph = Rgon1988.get_visualization_graph(interior_point,stared_polygon)
    # # nx.draw(graph)
    # graph.plot_directed(axs[])
    # # plot_graph(graph)

    plt.show()
    pass

def draw_convex_chain():
    df_points_interior,df_points_border = sampled_points.load_sampling_csv("data/starting_points/old/sampling_002.csv")
    x_border_length, y_border_length = sampled_points.get_border_dim(df_points_border)
    interior_points = sampled_points.df_to_array(df_points_interior[["x","y"]])
    border_points = sampled_points.df_to_array(df_points_border[["x","y"]])
    x_interior_points = [point.x for point in interior_points]
    y_interior_points = [point.y for point in interior_points]

    space_points = interior_points 
    kernel_point = interior_points[0]
    points_ahead = Rgon1988.get_points_horizontal_ahead(kernel_point,space_points)            
    stared_polygon = Rgon1988.get_stared_shape_polygon(kernel_point,points_ahead)

    fig, axs = plt.subplots(1,4,sharex=True,sharey=True)

    graph = Rgon1988.get_visualization_graph(kernel_point,stared_polygon)

    continuity_edges = Rgon1988.get_convex_chain_connectivity(graph)

    for rel in continuity_edges:
        for e in continuity_edges[rel]:
            print(rel + ":\t"+ str(e))

    edges_max_chain_length = Rgon1988.get_edges_max_chain_length(graph,continuity_edges)
    for e in edges_max_chain_length.keys():
        print(str(e) +" : " + str(edges_max_chain_length[e]))



    num_shapes = 3
    triangles = [Rgon1988.create_rgon(kernel_point,3,edges_max_chain_length,continuity_edges) for i in range(num_shapes)]
    poly4s = [Rgon1988.create_rgon(kernel_point,4,edges_max_chain_length,continuity_edges) for i in range(num_shapes)]
    
    stared_polygon.plot(axs[0])
    [triangles[i].plot(axs[1],color=PLOT_COLORS[i]) for i in range(len(triangles))]
    [poly4s[i].plot(axs[2],color=PLOT_COLORS[i]) for i in range(len(poly4s))]
    graph.plot_directed(axs[3])

    plt.show()


if __name__ == "__main__":
    # load_csv_and_scatter()
    # draw_stared_shaped_polygon()
    draw_visualization_graph()
    # draw_convex_chain()
    pass