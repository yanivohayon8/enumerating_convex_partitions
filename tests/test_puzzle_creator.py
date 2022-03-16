import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import unittest
from src.puzzle_creators import PuzzleCreator
from src.puzzle_creators.random import RandomCreator
import matplotlib.pyplot as plt
from src.data_structures import Polygon

class TestParentCreator(unittest.TestCase):

    files_path = 'data/starting_points/'
        
    def test_data_loading(self):
        creator = PuzzleCreator()
        creator.load_sampled_points(self.files_path + "TBN_01.csv")

        fig, ax = plt.subplots()
        creator.plot_scratch(ax)
        
        plt.show()


        pass
        

class TestRandomCreator(unittest.TestCase):

    files_path = 'data/starting_points/'
        
    def test_example_01(self):
        creator = RandomCreator()
        creator.load_sampled_points(self.files_path + "TBN_01.csv")
        fig, ax = plt.subplots()

        creator.create()
        creator.plot_puzzle(fig,ax)

        plt.show()
        pass


if __name__ == "__main__":
    unittest.main()
    # TestSweepLine.test_line_status_insert()
    pass
    