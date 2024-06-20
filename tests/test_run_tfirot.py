import sys
import os

from src.seed_points.board import Board

# from src.puzzle_creators import Direction

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import pandas as pd
import matplotlib.pyplot as plt
import unittest
import glob

from src.puzzle_creators.single_scanner.puzzle_obj import Puzzle

class TestRePAIRJune2022(unittest.TestCase):

    files_path = "data/puzzles"
    samples_files_path = "data/sampled_points"

    def test_save_plot_naive_puzzles(self):

        example_name = "sample_range-10000-convex_hull-9-int-16-6893" #"convex_hull-7-int-2-6545"
        # puzzle_name = "1-133_1-47_s_n_1-3_s_"
        fig,ax = plt.subplots(1,1)
        board = Board()
        board.load_sampled_points(self.samples_files_path + "/" + example_name + ".csv")
        temp_puzzle = Puzzle(board)
        puzzles_names = list(map(lambda pz: pz.split("\\")[1].split(".")[0],glob.glob(f"{self.files_path}/{example_name}/results/*.csv")))

        for puzzle_name in puzzles_names:
            df_puzzle = pd.read_csv(f"{self.files_path}/{example_name}/results/{puzzle_name}.csv")
            temp_puzzle.load_polygons(df_puzzle)
            ax.cla()
            temp_puzzle.plot_naive(ax,is_annotate=False)
            # ax.suptitle(puzzle_name)
            fig.savefig(f"{self.files_path}/{example_name}/naive_plot/{puzzle_name}.png")
        
