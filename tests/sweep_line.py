import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import src.data_structure as ds
import matplotlib.pyplot as plt
import pandas as pd


def simple_example():
    # load the examples
    df = pd.read_csv('data/algo_test/sweep_line/001.csv',index_col=False)
    segments = []
    df_list = df.values.tolist()

    for seg_row in df_list:
        start_point = ds.Point(seg_row[0],seg_row[1])
        end_point = ds.Point(seg_row[2],seg_row[3])
        segments.append(ds.Edge(start_point,end_point)) 

    fig,axs = plt.subplots()

    for segment in segments:
        segment.plot(axs)

    plt.show()


if __name__ == "__main__":
    simple_example()