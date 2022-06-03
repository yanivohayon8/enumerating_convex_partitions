import sys
import os

# from src.puzzle_creators import Direction

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import unittest
import glob

from src.puzzle_creators import statistics 


class TestStatistics(unittest.TestCase):

    def test_sample_poly_hist(self,example_name):
        # example_name = "convex_hull-3-int-2-2299"
        current_working_dir = os.getcwd()
        example_path = os.path.join(current_working_dir,"data","puzzles",example_name)
        csvs = glob.glob(f"{example_path}/results/*.csv")
        statistics.save_sample_poly_hist(csvs,f"{example_path}/polygon_type_hist.csv")
    
    def test_save_all_puzzles_poly_hist(self):
        current_working_dir = os.getcwd()
        examples_path = os.path.join(current_working_dir,"data","puzzles")
        examples = [ex.split("\\")[-1] for ex in glob.glob(f"{examples_path}/convex_hull*")]
        [self.test_sample_poly_hist(ex) for ex in examples]

