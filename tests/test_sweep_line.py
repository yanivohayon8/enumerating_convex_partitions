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

class TestSweepLine(unittest.TestCase):
    def test_simple_example(self):
        # load the examples
        df = pd.read_csv('data/algo_test/sweep_line/002.csv',index_col=False)
        segments = []
        df_list = df.values.tolist()

        for seg_row in df_list:
            start_point = ds.Point(seg_row[0],seg_row[1])
            end_point = ds.Point(seg_row[2],seg_row[3])
            segments.append(ds.Edge(start_point,end_point)) 

        fig,axs = plt.subplots()

        # for segment in segments:
        #     segment.plot(axs)
        # plt.show()

        sweep_line = SweepLine()
        sweep_line.preprocess(segments)

        # event_queue = list(map(lambda p: p.get_as_tuple(),sweep_line.event_queue))
        # upper_event = list(map(lambda s: str(s),sweep_line.upper_endpoint_segments))
        # lower_event = list(map(lambda p: p.get_as_tuple(),sweep_line.lower_endpoint_segments))
        # interior_events = list(map(lambda p: p.get_as_tuple(),sweep_line.interior_point_segments))

        # expect_event_queue = [(1,6),(7,6),(3,5),(4,4),(3,2),(5,1.5),(2,1)] 
        # expect_upper_event = [(1,6),(7,6),(3,5),(4,4)]
        # expect_lower_event = [(3,2),(5,1.5),(2,1)]
        # expect_interior_event = []

        # self.assertEqual(event_queue,expect_event_queue)
        # self.assertEquals(upper_event,expect_upper_event)
        # self.assertEquals(lower_event,expect_lower_event)
        # self.assertEquals(interior_events,expect_interior_event)

        print("Starting point:")
        sweep_line.line_status.print()
        sweep_line.event_queue.print()

        for event_point in sweep_line.run_algo():
            print(f"Handled Event point: {event_point}")
            sl_xml = sweep_line.line_status.convert_to_lxml(sweep_line.line_status.root)
            sl_xml.print()
            sweep_line.line_status.print()
            sweep_line.event_queue.print()
            print("\n",end="\n\n")
           

        pass

    def test_line_status_insert_delete(self):
        df = pd.read_csv('data/algo_test/sweep_line/002.csv',index_col=False)
        segments = []
        df_list = df.values.tolist()
        xml_root = XmlWrapper()

        for seg_row in df_list:
            start_point = ds.Point(seg_row[0],seg_row[1])
            end_point = ds.Point(seg_row[2],seg_row[3])
            segments.append(ds.Edge(start_point,end_point)) 
        
        sweep_line = SweepLine()
        sweep_line.preprocess(segments)
        event_queue = sweep_line.event_queue

        upper_endpoint_segments_0 = sweep_line.upper_endpoint_segments[str(event_queue[0])] 
        sweep_line.insert_to_status(upper_endpoint_segments_0[0])

        upper_endpoint_segments_1 = sweep_line.upper_endpoint_segments[str(event_queue[1])] 
        sweep_line.insert_to_status(upper_endpoint_segments_1[0])


        sl_xml = sweep_line.line_status.convert_to_lxml(sweep_line.line_status.root)
        sl_xml.print()

        segment_on_line = sweep_line.line_status.get_segment_on_line()

        is_equal = xml_root.element == sl_xml.element

        sweep_line.line_status.delete_segment(upper_endpoint_segments_1[0])
        sl_xml = sweep_line.line_status.convert_to_lxml(sweep_line.line_status.root)
        sl_xml.print()


    def test_line_status_simple_numbers(self):
        first_tree = SweepLine()
        second_tree = SweepLine()
        first_tree_vals = [4,10,5,6]
        second_tree_vals = [4,10,6,5]
        
        for num in first_tree_vals:
            first_tree.line_status.insert_segment(num)
        
        for num in second_tree_vals:
            second_tree.line_status.insert_segment(num)

        xml1 = first_tree.line_status.convert_to_lxml(first_tree.line_status.root)
        xml1.print()

        xml2 = second_tree.line_status.convert_to_lxml(second_tree.line_status.root)
        xml2.print()
        


        


if __name__ == "__main__":
    unittest.main()
    # TestSweepLine.test_line_status_insert()
    pass
    