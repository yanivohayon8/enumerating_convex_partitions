import sys
import os

# from src.puzzle_creators import Direction

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import unittest
from src.puzzle_creators import sampler
from src.data_structures.shapes import Polygon
from src.data_structures import Point

class TestSampler(unittest.TestCase):

    files_dir = "data/sampled_points/"

    def test_square(self):
        frame_tuples = [(0,0),(0,100),(100,100),(100,0)]
        frame_polygon_points = [Point(p) for p in frame_tuples]
        frame_polygon = Polygon(frame_tuples)
        n_int_points = 4
        sampled_points = sampler.sample_internal(n_int_points,frame_polygon)
        frame_points = frame_polygon.exterior.coords
        sampler.write_sampling(self.files_dir+f"frame-{len(frame_points)}-frame_anchor-{len(frame_points)}-int-{n_int_points}.csv",
                                sampled_points,frame_polygon_points,frame_polygon_points)