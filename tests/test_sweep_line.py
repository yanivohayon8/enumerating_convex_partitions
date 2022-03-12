from genericpath import exists
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import src.data_structures as ds
import matplotlib.pyplot as plt
import pandas as pd
# from  algorithms.sweep_line.sweep_line import SweepLine
from src.algorithms.sweep_line.sweep_line import SweepLine
import unittest
from src.data_types import XmlWrapper
from src.data_structures.lines import Segment 

class TestSweepLine(unittest.TestCase):

    def _run_example(self,file_path,expected_intersections,is_plot=False):
        '''load the examples'''
         # load the examples
        df = pd.read_csv(file_path,index_col=False)
        segments = []
        df_list = df.values.tolist()

        for seg_row in df_list:
            start_point = ds.Point(seg_row[0],seg_row[1])
            end_point = ds.Point(seg_row[2],seg_row[3])
            segments.append(ds.Edge(start_point,end_point)) 

        if is_plot:
            fig,axs = plt.subplots()

            for segment in segments:
                segment.plot(axs)
            plt.show()

        sweep_line = SweepLine()
        sweep_line.preprocess(segments)
        print("Starting point:")
        sweep_line.line_status.print()
        sweep_line.event_queue.print()
        sweep_line.run_algo(is_debug=True)
        
        # None = I skipped it for now 
        if expected_intersections is not None:
            self.assertEqual(len(sweep_line.intersections),len(expected_intersections))

            for exist,expected in zip(sweep_line.intersections,expected_intersections):
                self.assertEqual(exist["point"],expected["point"])
                self.assertEqual(exist["segments"],expected["segments"])

    def test_simple_example(self):
        # The expected results 
        seg_1 = Segment(ds.Point(5,10),ds.Point(5.5,2.5))
        seg_2 = Segment(ds.Point(6,6),ds.Point(5,2))
        inter_point = seg_1.find_intersection_point(seg_2)
        expected_intersections = [{
            "point": inter_point,
            "segments":[seg_2,seg_1]
        }]

        self._run_example('data/algo_test/sweep_line/002.csv',expected_intersections)

    def test_example_001(self):
        self._run_example('data/algo_test/sweep_line/001.csv',None)

    def test_inter_003_example(self):
        self._run_example('data/algo_test/sweep_line/003.csv',None,is_plot=True)
    
    def test_inter_004_example(self):
        self._run_example('data/algo_test/sweep_line/004.csv',None,is_plot=True)

    def test_vertical_005_example(self):
        self._run_example('data/algo_test/sweep_line/005.csv',None)


if __name__ == "__main__":
    unittest.main()
    # TestSweepLine.test_line_status_insert()
    pass
    