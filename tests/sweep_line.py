import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import src.data_structure as ds
import matplotlib.pyplot as plt
import pandas as pd
from  src.algorithms.sweep_line import SweepLine
import unittest

class TestSweepLine(unittest.TestCase):
    def test_simple_example(self):
        # load the examples
        df = pd.read_csv('data/algo_test/sweep_line/001.csv',index_col=False)
        segments = []
        df_list = df.values.tolist()

        for seg_row in df_list:
            start_point = ds.Point(seg_row[0],seg_row[1])
            end_point = ds.Point(seg_row[2],seg_row[3])
            segments.append(ds.Edge(start_point,end_point)) 

        # fig,axs = plt.subplots()

        # for segment in segments:
        #     segment.plot(axs)
        # plt.show()

        sweep_line = SweepLine(segments)
        sweep_line.preprocess()

        event_queue = list(map(lambda p: p.get_as_tuple(),sweep_line.event_queue))
        # upper_event = list(map(lambda s: str(s),sweep_line.upper_endpoint_segments))
        # lower_event = list(map(lambda p: p.get_as_tuple(),sweep_line.lower_endpoint_segments))
        # interior_events = list(map(lambda p: p.get_as_tuple(),sweep_line.interior_point_segments))

        expect_event_queue = [(1,6),(7,6),(3,5),(4,4),(3,2),(5,1.5),(2,1)] 
        # expect_upper_event = [(1,6),(7,6),(3,5),(4,4)]
        # expect_lower_event = [(3,2),(5,1.5),(2,1)]
        # expect_interior_event = []

        self.assertEqual(event_queue,expect_event_queue)
        # self.assertEquals(upper_event,expect_upper_event)
        # self.assertEquals(lower_event,expect_lower_event)
        # self.assertEquals(interior_events,expect_interior_event)

        sweep_line.run_algo()

        sweep_line.print_line_status()

        pass




if __name__ == "__main__":
    unittest.main()
    pass
    