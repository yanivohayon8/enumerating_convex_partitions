import numpy as np
import src.sampled_points as sampled_points

def ala_va_bala():
    df_points_interior,df_points_border = sampled_points.load_sampling_csv("data/starting_points/sampling_001.csv")
    
    interior_points = sampled_points.df_to_array(df_points_interior[["x","y"]])
    border_points = sampled_points.df_to_array(df_points_border[["x","y"]])

    x_interior_points = [point[0] for point in interior_points]
    y_interior_points = [point[1] for point in interior_points]
    x_border_points = [point[0] for point in border_points]
    y_border_points = [point[1] for point in border_points]

    sampled_points.plot_sampled_point(x_interior_points,y_interior_points,6,12)


if __name__ == "__main__":
    ala_va_bala()
    pass