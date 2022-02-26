import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import src.data_structures as ds
import matplotlib.pyplot as plt
import pandas as pd
from  src.algorithms.sweep_line import SweepLine
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

        sweep_line.run_algo()

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

        # Creating the desired result: 
        #   i 
        # i   k
        xml_root.set_att("node",str(upper_endpoint_segments_1[0]))
        xml_child1_left = XmlWrapper(prefix="left")
        xml_child1_left.set_att("node",str(upper_endpoint_segments_1[0]))
        xml_child1_right = XmlWrapper(prefix="right")
        xml_child1_right.set_att("node",str(upper_endpoint_segments_0[0]))
        xml_root.add_child(xml_child1_left)
        xml_root.add_child(xml_child1_right)
        xml_root.print()

        is_equal = xml_root.element == sl_xml.element

        #self.assertTrue(is_equal)

        sweep_line.line_status.delete_segment(upper_endpoint_segments_1[0])
        # sweep_line.line_status.delete_segment(upper_endpoint_segments_0[0])
        sl_xml = sweep_line.line_status.convert_to_lxml(sweep_line.line_status.root)
        sl_xml.print()


        


        


if __name__ == "__main__":
    unittest.main()
    # TestSweepLine.test_line_status_insert()
    pass
    