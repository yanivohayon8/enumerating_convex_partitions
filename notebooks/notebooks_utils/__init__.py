import numpy as np
import pandas as pd

def n_interior_points(example_name):
    ex = example_name.split("\\")[-1]
    values = ex.split("-")
    return eval(values[-2])

def n_convex_hull(example_name):
    ex = example_name.split("\\")[-1]
    values = ex.split("-")
    return eval(values[1])


def vertecies_degree(df_puzzle_polygons):
    df_puzzle_polygons = df_puzzle_polygons.drop("Unnamed: 0",axis=1)
    df_puzzle_polygons.columns = ["src_x","src_y","polygon_id"]
    #print(df_puzzle_polygons.head())
    ids = df_puzzle_polygons.polygon_id.unique()
    xs = []
    ys = []

    for _id in ids:
        df_curr_polygon = df_puzzle_polygons.loc[df_puzzle_polygons["polygon_id"]==_id]
        xs = xs + np.roll(df_curr_polygon["src_x"].values.tolist(),-1).tolist()
        ys = ys + np.roll(df_curr_polygon["src_y"].values.tolist(),-1).tolist()

    df_puzzle_polygons["dst_x"] = xs
    df_puzzle_polygons["dst_y"] = ys
    # print(df_puzzle_polygons.head())
    dst = df_puzzle_polygons.groupby(["dst_x","dst_y"],as_index=False).size()[["dst_x","dst_y"]].values.tolist()
    src = df_puzzle_polygons.groupby(["src_x","src_y"],as_index=False).size()[["src_x","src_y"]].values.tolist()
    assert(dst==src)
    adjecency_mat = np.zeros((len(src),len(src)))

    for index,row in df_puzzle_polygons.iterrows():
        src_point = row[["src_x","src_y"]].values.tolist()
        dst_point = row[["dst_x","dst_y"]].values.tolist()
        adjecency_mat[src.index(src_point),src.index(dst_point)] = 1 
        adjecency_mat[src.index(dst_point),src.index(src_point)] = 1 

    return pd.DataFrame({
            "x": df_puzzle_polygons.groupby(["src_x","src_y"],as_index=False).size().src_x.values.tolist(),
            "y": df_puzzle_polygons.groupby(["src_x","src_y"],as_index=False).size().src_y.values.tolist(),
            "degree": [adjecency_mat[:,point_index].sum() for point_index in range(len(src))]
        })