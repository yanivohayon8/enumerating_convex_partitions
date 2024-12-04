import unittest
import sys
sys.path.append("..")

from src.data_structures import Point
from src.data_structures.shapes import Polygon
import matplotlib.pyplot as plt
from src.seed_points.board import Board
from shapely.geometry import MultiPoint
from src.seed_points import sampler
from glob import glob

class TestBoard(unittest.TestCase):

    def test_toy(self):

        interior_points = [Point(30,50)]
        convex_hull = [Point(0,0),Point(100,0),Point(100,100),Point(0,100)]

        board = Board(interior_points,convex_hull)

        _,ax = plt.subplots()
        board.plot(ax)
        plt.show()

    def test_toy_sampler(self):
        interior_points,convex_hull_points,_ = sampler.sample_AABB(10,1000,1000)

        board = Board(interior_points,convex_hull_points)

        _,ax = plt.subplots()
        board.plot(ax)
        plt.show()
    
    def test_plot_board(self):
        files_seed = glob("data/paper/panelA/*/CH-*")
        board = Board(file_path=files_seed[0])
        ax = plt.subplot()

        y_min = 120
        y_max = 650
        x_min = 370
        x_max = 1180

        board.plot(ax)
        ax.set_aspect("equal")

        plt.show()

        print()
         

if __name__ == "__main__":
    unittest.main()