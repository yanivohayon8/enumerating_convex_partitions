import pandas as pd
import glob
import os


def df_raw_data(files_path):
    # csvs = glob.iglob(files_path+"/**/*.csv",recursive=True)
    directory = glob.glob(files_path+"/*")
    
    # convention of file path: data/puzzles\\frame-4-frame_anchor-4-int-1-395
    n_internal_points = []
    n_frame_points = []
    n_frame_anchor = []
    n_puzzles = []
    for sample_dir in directory:
        name = sample_dir.split("\\")[-1]
        vals = name.split("-")
        n_internal_points.append(eval(vals[-2]))
        n_frame_anchor.append(eval(vals[-4]))
        # n_frame_points.append(eval(vals[-6]))
        n_puzzles.append(len(glob.glob(f"{sample_dir}/**/*.csv",recursive=True)))
    
    return pd.DataFrame(data={
        "n_convex_hull":n_frame_anchor,
        "n_interior":n_internal_points,
        "n_puzzles":n_puzzles
    })



def save_sample_poly_hist(csvs,output_path):
    df_sample = pd.DataFrame()
    for csv in csvs:
        df_puzzle = pd.read_csv(csv)
        df_polygons = df_puzzle.groupby("id").size().reset_index(name="polygon_type")
        df_sample = pd.concat([df_sample,df_polygons],axis=0)
    
    df_poly_hist = pd.DataFrame()
    df_poly_hist["Count"] = df_sample.polygon_type.value_counts()
    df_poly_hist["Percentage"] = df_sample.polygon_type.value_counts(normalize=True).mul(100).round(2)
    
    df_poly_hist.to_csv(output_path)
        


