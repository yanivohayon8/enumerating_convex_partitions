import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def load_sampling_csv(path):
    df = pd.read_csv(path,index_col=False)
    df_points_interior = df.loc[df["role"]=="interior"]
    df_points_border = df.loc[df["role"]=="border"]
    return df_points_interior,df_points_border


def df_to_array(df):
    return [tuple(row) for row in df.to_numpy()]

def plot_sampled_point(x_interior_points, y_interior_points,
                        border_width, border_height,border_start_point=(1,1)):
    shifted_x = [p+1 for p in x_interior_points]
    shifted_y = [p+1 for p in y_interior_points]

    fig, ax = plt.subplots()                        
    ax.scatter(shifted_x, shifted_y)    
    #plt.scatter(x_border_points,y_border_points,c="black")

    border_frame = patches.Rectangle(border_start_point, border_height, border_width, linewidth=1,
                        edgecolor='r', facecolor="none")
    ax.add_patch(border_frame)

    plt.show()

#def plot_line()
# plt.plot(interior_points[0], interior_points[1], 'bo-')
