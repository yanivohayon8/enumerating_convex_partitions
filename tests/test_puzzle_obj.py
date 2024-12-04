import unittest
import sys
sys.path.append("./")

from src.puzzle_creators.utils.puzzle_obj import Puzzle
import pandas as pd
import matplotlib.pyplot as plt
from src.seed_points.board import Board

class TestPuzzleObj(unittest.TestCase):

    def test_loading_for_ploting(self):
        
        board = Board(file_path="data/paper/panelC/2024-12-03 07-55-29+865589/CH-7-INT-3-07-55-29.csv",skip_validity=True)
        puzzle = Puzzle(board)

        df = pd.read_csv("data/paper/panelC/2024-12-03 07-55-29+865589/1-297_s_24-29_n_1-3_.csv")
        df.columns = ["id","x","y"]
        puzzle.load_polygons(df)

        ax = plt.subplot()

        puzzle.plot_shades(ax)

        plt.show()
    
    def test_shades_plotting(self):
        board = Board(file_path="data/thesis qualatative results/manual_sampling/CH-5-INT-2-14-28-21 to 6-0.csv")
        puzzle = Puzzle(board)

        df = pd.read_csv("data/thesis qualatative results/CH-5-INT-2-14-28-21 to 6-0/12-27_.csv")
        df.columns = ["id","x","y"]
        puzzle.load_polygons(df)

        ax = plt.subplot()

        puzzle.plot_shades(ax)

        plt.show()

if __name__ == "__main__":
    unittest.main()