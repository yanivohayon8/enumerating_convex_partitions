import unittest
import sys
sys.path.append("..")

from src.data_structures import Point
from src.data_structures.shapes import Polygon
import matplotlib.pyplot as plt
from src.seed_points.board import Board
from shapely.geometry import MultiPoint
from src.seed_points import sampler


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
        # board = Board(file_path="data/thesis qualatative results/manual_sampling/CH-5-INT-2-14-28-21 to 4-2 to 3-3 v2.csv")
        #board = Board(file_path="data/thesis qualatative results/manual_sampling/CH-5-INT-2-14-28-21 to 4-2 to 3-3.csv")
        # board = Board(file_path="data/thesis qualatative results/stam manual3 pertubed/CH-5-INT-2-19-41-56.csv")
        # board = Board(file_path="data/thesis quantative results/2024-06-26 12-01-36 on-circle/CH-6-INT-1-12-01-36.csv")
        # board = Board(file_path="data/thesis qualatative results/input sensitivity/CH-5-INT-1-13-32-33 V2.csv")
        # board = Board(file_path="data/thesis qualatative results/input sensitivity/4-1/CH-4-INT-1-13-28-21.csv")
        board = Board(file_path="data/thesis qualatative results/input sensitivity/3-1/CH-3-INT-0-12-01-11.csv")
        ax = plt.subplot()

        y_min = 120
        y_max = 650
        x_min = 370
        x_max = 1180

        board.plot(ax)
        # ax.set_xlim([x_min,x_max])
        # ax.set_ylim([y_min,y_max])
        ax.set_aspect("equal")

        plt.show()

        print()

    def test_plot_boards_pertubated_as_grid(self):
        board6_0 = Board(file_path="data/thesis qualatative results/manual_sampling/CH-5-INT-2-14-28-21 to 6-0.csv")
        board5_1 = Board(file_path="data/thesis qualatative results/manual_sampling/CH-5-INT-2-14-28-21 to 5-1.csv")
        board4_2 = Board(file_path="data/thesis qualatative results/manual_sampling/CH-5-INT-2-14-28-21 to 5-1 to 4-2.csv")
        board3_3 = Board(file_path="data/thesis qualatative results/manual_sampling/CH-5-INT-2-14-28-21 to 4-2 to 3-3 v2.csv")

        fig, axs = plt.subplots(2,2)
        
        y_min = 120
        y_max = 650
        x_min = 370
        x_max = 1180

        for ax in axs.flatten():
            ax.set_xlim([x_min,x_max])
            ax.set_ylim([y_min,y_max])
            ax.set_aspect("equal")
        
        board6_0.plot(axs[0,0])
        board5_1.plot(axs[0,1])
        board4_2.plot(axs[1,0])
        board3_3.plot(axs[1,1])
        
        
        
        plt.show()
         

if __name__ == "__main__":
    unittest.main()