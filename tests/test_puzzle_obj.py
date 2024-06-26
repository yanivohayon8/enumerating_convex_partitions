import unittest
import sys
sys.path.append("./")

from src.puzzle_creators.utils.puzzle_obj import Puzzle
import pandas as pd
import matplotlib.pyplot as plt

class TestPuzzleObj(unittest.TestCase):

    def test_loading_for_ploting(self):
        puzzle = Puzzle(None)

        df = pd.read_csv("games/chris old puzzles/christian-spasov-JhT5z93iSOY-unsplash_0.csv")
        df.columns = ["id","x","y"]
        puzzle.load_polygons(df)

        ax = plt.subplot()

        puzzle.plot(ax)

        plt.show()

if __name__ == "__main__":
    unittest.main()