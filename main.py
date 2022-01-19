import src.sampled_points as sampled_points
from src.hypothesis import rgon_1988 as Rgon1988
import matplotlib.pyplot as plt

def load_csv_and_scatter():
    df_points_interior,df_points_border = sampled_points.load_sampling_csv("data/starting_points/sampling_001.csv")
    
    interior_points = sampled_points.df_to_array(df_points_interior[["x","y"]])
    border_points = sampled_points.df_to_array(df_points_border[["x","y"]])
    x_border_length, y_border_length = sampled_points.get_border_dim(df_points_border)
    x_interior_points = [point.x for point in interior_points]
    y_interior_points = [point.y for point in interior_points]

    fig, ax = plt.subplots()
    sampled_points.plot_sampled_point(fig,ax,x_interior_points,y_interior_points,x_border_length,y_border_length)
    plt.show()


def draw_stared_shaped_polygon():
    df_points_interior,df_points_border = sampled_points.load_sampling_csv("data/starting_points/sampling_002.csv")
    
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
    
    stared_polygon.plot(fig,ax)
    sampled_points.plot_sampled_point(fig,ax,x_interior_points,y_interior_points,x_border_length,y_border_length)
    plt.show()

def draw_visualization_graph():
    df_points_interior,df_points_border = sampled_points.load_sampling_csv("data/starting_points/sampling_002.csv")
    
    x_border_length, y_border_length = sampled_points.get_border_dim(df_points_border)

    interior_points = sampled_points.df_to_array(df_points_interior[["x","y"]])
    border_points = sampled_points.df_to_array(df_points_border[["x","y"]])
    x_interior_points = [point.x for point in interior_points]
    y_interior_points = [point.y for point in interior_points]

    space_points = interior_points 
    interior_point = interior_points[0]
    points_ahead = Rgon1988.get_points_horizontal_ahead(interior_point,space_points)            
    stared_polygon = Rgon1988.get_stared_shape_polygon(interior_point,points_ahead)

    fig, axs = plt.subplots(1,3)
    stared_polygon.plot(fig,axs[0])
    sampled_points.plot_sampled_point(fig,axs[0],x_interior_points,y_interior_points,x_border_length,y_border_length)

    graph = Rgon1988.get_visualization_graph(interior_point,stared_polygon)
    graph.plot_undirected(axs[1])
    graph.plot_directed(axs[2])

    plt.show()

    # pass



if __name__ == "__main__":
    #load_csv_and_scatter()
    #draw_stared_shaped_polygon()
    draw_visualization_graph()
    pass