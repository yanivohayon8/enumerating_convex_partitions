import sys
import os
import unittest

# from src.puzzle_creators import Direction

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from src.seed_points import sampler
from src.data_structures.shapes import Polygon
from src.data_structures import Point
from shapely.geometry import MultiPoint

from random import randint


class TestDeprecatedTests(unittest.TestCase):

    files_dir = "data/sampled_points/"

    def test_square_interior(self):
        frame_tuples = [(0,0),(0,100),(100,100),(100,0)]
        frame_polygon_points = [Point(p) for p in frame_tuples]
        frame_polygon = Polygon(frame_tuples)


        for n_int_points in range(9,10,1):
            for t in range(1):
                sampled_points = sampler.sample_int_(n_int_points,frame_polygon)
                frame_points = frame_polygon.exterior.coords
                rnd_int = randint(1,1000)
                file_name = self.files_dir+f"frame-{len(frame_points)-1}-frame_anchor-{len(frame_points)-1}-int-{n_int_points}-{rnd_int}.csv"
                sampler.arange_df_(file_name,sampled_points,frame_polygon_points,frame_polygon_points)

    def test_convex_hull(self):
        frame_tuples = [(0,0),(0,100),(100,100),(100,0)]
        frame_polygon_points = [Point(p) for p in frame_tuples]
        frame_polygon = Polygon(frame_tuples)
        x_min, y_min, x_max, y_max = frame_polygon.bounds

        for n_int_points in range(5,6,1):
            for t in range(20):
                sampled_points = MultiPoint(sampler.sample_float_(n_int_points,x_min, y_min, x_max, y_max))                
                # convex_hull = 
                convex_hull = sampled_points.convex_hull
                interior_points = [point for point in sampled_points if not convex_hull.touches(point)]
                convex_hull_points = MultiPoint(list(Polygon(sampled_points.convex_hull).exterior.coords)[:-1])
                rnd_int = randint(1,10000)
                file_name = self.files_dir+f"convex_hull-{len(convex_hull_points)}-int-{len(interior_points)}-{rnd_int}.csv"
                sampler.arange_df_(file_name,interior_points,convex_hull_points,convex_hull_points)

    def test_for_repair_june(self):
        '''
            Sampling at frame of 1000x1000 so ofir will cut pictures from the futured puzzled
        '''
        frame_sampling_size = 10000
        #frame_tuples = [(0,0),(0,frame_sampling_size),(frame_sampling_size,frame_sampling_size),(frame_sampling_size,0)]
        frame_tuples = [(0,0),(0,2953),(2248,2953),(2248,0)] # because ofir asked these dimensions
        frame_polygon_points = [Point(p) for p in frame_tuples]
        frame_polygon = Polygon(frame_tuples)
        x_min, y_min, x_max, y_max = frame_polygon.bounds

        for n_int_points in range(15,20,1):
            for t in range(1):
                sampled_points = MultiPoint(sampler.sample_float_(n_int_points,x_min, y_min, x_max, y_max))                
                # convex_hull = 
                convex_hull = sampled_points.convex_hull
                interior_points = [point for point in sampled_points if not convex_hull.touches(point)]
                convex_hull_points = MultiPoint(list(Polygon(sampled_points.convex_hull).exterior.coords)[:-1])
                rnd_int = randint(1,10000)
                file_name = self.files_dir+f"sample_range-{frame_sampling_size}-convex_hull-{len(convex_hull_points)}-int-{len(interior_points)}-{rnd_int}.csv"
                sampler.arange_df_(file_name,interior_points,convex_hull_points,convex_hull_points)


class TestSampler(unittest.TestCase):

    def test_toy_AABB_without_saving(self):
        df,_ = sampler.sample_AABB(5,1000,1000)

        assert _ is None

        print(df)

    def test_toy_AABB_saving(self):
        df,out_path = sampler.sample_AABB(10,1000,1000,output_dir="data/tmp")

        assert isinstance(out_path,str)
        assert os.path.exists(out_path)

        print(df)

        os.remove(out_path)