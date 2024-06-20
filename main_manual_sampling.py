import argparse
from PIL import Image
import os
from src.data_structures.shapes import Polygon
from src.data_structures import Point
from shapely.geometry import MultiPoint
from datetime import datetime
from src.seed_points.board import Board
from src.puzzle_creators.single_scanner.creator import Creator
import matplotlib.pyplot as plt
import pandas as pd
import shutil


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sampling_src_file",default="")
    parser.add_argument("--puzzles_dst_folder",default="data/puzzles/new_puzzles")
    parser.add_argument("--num_puzzles",default=10,type=int)

    args = parser.parse_args()

    
    
        
    try:
        dst_file = args.sampling_src_file
        
        
        board = Board()
        board.load_sampled_points(dst_file)

        puzzles_dst_folder = args.puzzles_dst_folder

        creator = Creator(board,puzzles_dst_folder)
        dirs_to_create = [puzzles_dst_folder,puzzles_dst_folder+"/results"]

        for _dir in dirs_to_create:
            if not os.path.exists(_dir):
                os.makedirs(_dir)

        creator.sample_puzzle_space(probability_skip_snapshot=0.8, num_puzzles=int(args.num_puzzles))

        if args.sampling_src_file=="":
            os.remove(dst_file)

        plt.close("all")
    except Exception as err:
        raise err
    finally:
        plt.close("all")


