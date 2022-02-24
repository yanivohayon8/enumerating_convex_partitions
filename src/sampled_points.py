import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from .data_structures import Point

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