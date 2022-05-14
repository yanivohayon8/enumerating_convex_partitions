from cmath import log
import sys
import os

# from src.puzzle_creators import Direction

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import unittest
# from src.puzzle_creators.skeleton import PuzzleCreator
# from src.puzzle_creators.power_group.primary import PowerGroupCreator
from src.puzzle_creators.single_scanner.creator import Creator
from src.puzzle_creators.single_scanner.puzzle_obj import Board

import matplotlib.pyplot as plt
import logging
from src import setup_logger
from glob import glob as glob_glob
from ntpath import split as ntpath_split





class TestSingleScanCreator(unittest.TestCase):
    files_path = 'data/starting_points/'
   

    def _run(self,example_name,output_dir):
        dirs = ["results","visibility-graph-before-filter","visibility-graph-filtered",
                "last_decision_junction","last_creation","snapshots","failure"]
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            [os.makedirs(output_dir+ f"/{_dir}") for _dir in dirs]
        
        [[os.remove(file.path) for file in os.scandir(os.path.join(output_dir+f"/{_dir}"))] for _dir in dirs]

        # setup_logger.set_debug_lastrun_dir(output_dir)
        # log_handler = setup_logger.get_file_handler(os.path.join(output_dir,"run.log"),mode="w")
        # logger = logging.getLogger("logger.test_puzzle_creator")
        # logger.addHandler(log_handler)
        # logger.debug("Starting....")


        board = Board()
        board.load_sampled_points(self.files_path + example_name +".csv")

        creator = Creator(board,output_dir)
        # fig, ax = plt.subplots()

        try:
            # start_time = time.time()
            creator.create_puzzles()
            
        except Exception as err:
            pass
            # logger.exception(err)
            # logger.error(err)
            raise err
        finally:
            plt.close("all")

    def _validate_results(self,result_path):
        # gather traces
        results_paths = glob_glob(result_path+"/*.csv")
        results_traces = [ntpath_split(path)[1].split(".")[0] for path in results_paths]
        puzzles_traces = []

        for trace_str in results_traces:
            trace_str = trace_str.replace("s_","")
            recursive_calls = trace_str.split("_")
            trace = []
            for recursive_call in recursive_calls:
                curr,total = recursive_call.split("-")
                curr = eval(curr)
                total = eval(total)
                trace.append((curr,total))
            puzzles_traces.append(trace)
        
        # analayz consistency
        


    def _output_dir(self,example_name):
        current_working_dir = os.getcwd()
        return os.path.join(current_working_dir,"data","results",example_name)
        

    def test_simple_square(self):
        example_name = "simple_square"
        output_dir = self._output_dir(example_name)
        self._run(example_name,output_dir)
        
    def test_empty_triangle(self):
        example_name = "triangle_intpoint_0_01"
        output_dir = self._output_dir(example_name)
        self._run(example_name,output_dir)

    def test_simple_square_crossing_cuts(self):
        example_name = "simple_square_crossing_cuts"
        output_dir = self._output_dir(example_name)
        self._run(example_name,output_dir)
    
    def test_triangle_intpoint_1_01(self):
        example_name = "triangle_intpoint_1_01"
        output_dir = self._output_dir(example_name)
        self._run(example_name,output_dir)
    
    def test_square_int_2_anchor_4_01(self):
        example_name = "square_int_2_anchor_4_01"
        output_dir = self._output_dir(example_name)
        self._run(example_name,output_dir)

    def test_square_int_2_anchor_8_01(self):
        example_name = "square_int_2_anchor_8_01"
        output_dir = self._output_dir(example_name)
        self._run(example_name,output_dir)
        # self._validate_results(output_dir+"/results")
        # C:\Users\yaniv\Desktop\MSCBenGurion\iCVL\rgons\data\debug_powergroup_creator\square_int_2_anchor_8_01\results

    def test_square_int_4_anchor_4_01(self):
        example_name = "square_int_4_anchor_4_01"
        output_dir = self._output_dir(example_name)
        self._run(example_name,output_dir)
    
    def test_square_int_5_anchor_4_01(self):
        example_name = "square_int_5_anchor_4_01"
        output_dir = self._output_dir(example_name)
        self._run(example_name,output_dir)
        