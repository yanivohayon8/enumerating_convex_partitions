from genericpath import exists
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from src.data_structures.graph import Edge
import matplotlib.pyplot as plt
import pandas as pd
# from  algorithms.sweep_line.sweep_line import SweepLine
from src.algorithms.sweep_line.sweep_line import SweepLine
import unittest
from src.data_structures.lines import Segment 
from shapely.geometry import Point

class TestSweepLine(unittest.TestCase):

    files_path = 'data/algo_test/sweep_line/'

    def _run_example(self,file_path,file_path_ans,is_plot=False):
        '''load the examples'''
         # load the examples
        df = pd.read_csv(file_path) #pd.read_csv(file_path,index_col=False)
        segments = []
        df_list = df.values.tolist()

        for seg_row in df_list:
            start_point = Point(seg_row[0],seg_row[1])
            end_point = Point(seg_row[2],seg_row[3])
            segments.append(Edge(start_point,end_point)) 

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
        df_res = sweep_line.run_algo(is_debug=True)
        
        df_ans = pd.read_csv(file_path_ans)
        df_res = df_res.sort_values(by=df_res.columns.tolist()).reset_index(drop=True)
        df_ans = df_res.sort_values(by=df_ans.columns.tolist()).reset_index(drop=True)
        self.assertTrue(df_res.equals(df_ans))

        
    def test_example_002(self):
        self._run_example(self.files_path + '002.csv',self.files_path + '002_ans.csv')

    def test_example_001(self):
        self._run_example(self.files_path + '001.csv',self.files_path + '001_ans.csv')

    def test_inter_003_example(self):
        self._run_example(self.files_path + '003.csv',self.files_path + '003_ans.csv')
    
    def test_inter_004_example(self):
        self._run_example(self.files_path + '004.csv',self.files_path + '004_ans.csv')

    def test_vertical_005_example(self):
        self._run_example(self.files_path + '005.csv',self.files_path + '005_ans.csv')

    # sweep line assumes this scenario does not exist
    # def test_segment_in_segment_006_example(self):
    #     self._run_example(self.files_path + '006.csv',self.files_path + '006_ans.csv')


if __name__ == "__main__":
    unittest.main()
    # TestSweepLine.test_line_status_insert()
    pass
    