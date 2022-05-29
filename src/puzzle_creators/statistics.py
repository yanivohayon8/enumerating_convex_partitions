import pandas as pd
import glob


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