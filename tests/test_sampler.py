import sys
import os
import unittest
import matplotlib.pyplot as plt

# from src.puzzle_creators import Direction

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from src.seed_points import sampler
from src.data_structures.shapes import Polygon
from src.data_structures import Point
from shapely.geometry import MultiPoint

from random import randint


class TestSampler(unittest.TestCase):

    def test_toy_AABB(self):
        interior_points,convex_hull_points,_ = sampler.sample_AABB(5,1000,1000)

        assert _ is None

        print("num interior points",len(interior_points))
        print("num CH points",len(convex_hull_points))

    def test_toy_AABB_saving(self):
        interior_points,convex_hull_points,out_path = sampler.sample_AABB(10,1000,1000,output_dir="data/tmp")

        assert isinstance(out_path,str)
        assert os.path.exists(out_path)

        print("num interior points",len(interior_points))
        print("num CH points",len(convex_hull_points))

        os.remove(out_path)
    
    def test_toy_image(self):
        interior_points,convex_hull_points, _ = sampler.sample_image(5,"data/images/neom-Oj8w6hWC0dU-unsplash.jpg")

        assert _ is None

        print("num interior points",len(interior_points))
        print("num CH points",len(convex_hull_points))


    def test_toy_image_saving(self):
        interior_points,convex_hull_points,out_path = sampler.sample_image(10,"data/images/neom-Oj8w6hWC0dU-unsplash.jpg",output_dir="data/tmp")

        assert isinstance(out_path,str)
        assert os.path.exists(out_path)

        print("num interior points",len(interior_points))
        print("num CH points",len(convex_hull_points))

        os.remove(out_path)

    def test_toy_manual(self):
        interior_points,convex_hull_points, _ = sampler.sampler_manual()

        assert _ is None


        print("num interior points",len(interior_points))
        print("num CH points",len(convex_hull_points))
    
    def test_toy_manual_saving(self):
        interior_points,convex_hull_points, out_path = sampler.sampler_manual(output_dir="data/thesis quantative results/manual_sampling")

        assert isinstance(out_path,str)


        print("num interior points",len(interior_points))
        print("num CH points",len(convex_hull_points))

    
    def test_on_circle(self):
        interior_points,convex_hull_points, out_path = sampler.sample_points_on_circle(5,2,1000)

        print("num interior points",len(interior_points))
        print("num CH points",len(convex_hull_points))

        int_xs = [point.x for point in interior_points]
        int_ys = [point.y for point in interior_points]
        plt.scatter(int_xs,int_ys,color="blue")

        ch_xs = [point.x for point in convex_hull_points]
        ch_ys = [point.y for point in convex_hull_points]
        plt.scatter(ch_xs,ch_ys,color="red")

        plt.show()

    def test_on_circle_only_ch(self):
        interior_points,convex_hull_points, out_path = sampler.sample_points_on_circle(5,0,1000)

        print("num interior points",len(interior_points))
        print("num CH points",len(convex_hull_points))

        int_xs = [point.x for point in interior_points]
        int_ys = [point.y for point in interior_points]
        plt.scatter(int_xs,int_ys,color="blue")

        ch_xs = [point.x for point in convex_hull_points]
        ch_ys = [point.y for point in convex_hull_points]
        plt.scatter(ch_xs,ch_ys,color="red")

        plt.show()
        
