from turtle import color
from src.data_structure import Polygon
from src.hypothesis import rgon_1988 as Rgon1988
from src.hypothesis.first_hypo import FirstHypo
import matplotlib.pyplot as plt
import src.sampled_points as sampled_points
from  src.consts import PLOT_COLORS



def test():
    df_points_interior,df_points_border = sampled_points.load_sampling_csv("data/starting_points/sampling_002.csv")
    # x_border_length, y_border_length = sampled_points.get_border_dim(df_points_border)
    interior_points = sampled_points.df_to_array(df_points_interior[["x","y"]])
    border_points = sampled_points.df_to_array(df_points_border[["x","y"]])
    fig, axs = plt.subplots(1,2)
    
    border_polygon = Rgon1988.get_stared_shape_polygon(border_points[0],border_points[1:])
    border_polygon.plot(axs[0],color="black")

    hypo = FirstHypo(interior_points,border_points)
    polygons = hypo.run_algo()
    for i,pol in enumerate(polygons):
        pol.plot(axs[0],color=PLOT_COLORS[i%len(PLOT_COLORS)])
    
    hypo.graph.plot_directed(axs[1])
    
    plt.show()
    



if __name__ == "__main__":
    test()
    pass