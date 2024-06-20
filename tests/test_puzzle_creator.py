import sys
import os

# from src.puzzle_creators import Direction

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import pandas as pd

import unittest
# from src.puzzle_creators.skeleton import PuzzleCreator
# from src.puzzle_creators.power_group.primary import PowerGroupCreator
from src.puzzle_creators.utils.creator import Creator
from src.puzzle_creators.utils.adjasments import transform_peleg_output
from src.seed_points.board import Board

import matplotlib.pyplot as plt
from glob import glob as glob_glob
from ntpath import split as ntpath_split
from src.puzzles_statistics import df_raw_data
import numpy as np



class TestSingleScanCreator(unittest.TestCase):
    files_path = 'data/starting_points/'
   

    def _run(self,example_name,output_dir):
        dirs = ["results","visibility-graph-before-filter","visibility-graph-filtered",
                "last_decision_junction","last_creation","snapshots","failure"]
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            [os.makedirs(output_dir+ f"/{_dir}") for _dir in dirs]
        
        [[os.remove(file.path) for file in os.scandir(os.path.join(output_dir+f"/{_dir}"))] for _dir in dirs]



        board = Board()
        board.load_sampled_points(self.files_path + example_name +".csv")

        creator = Creator(board,output_dir)
        # fig, ax = plt.subplots()

        try:
            # start_time = time.time()
            creator.create_puzzles()
            
        except Exception as err:
            pass
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


class TestStatistics(unittest.TestCase):

    def test_first_stats(self):
        current_working_dir = os.getcwd()
        files_paths = os.path.join(current_working_dir,"data","puzzles")
        df_data = df_raw_data(files_paths)
        df_data["min_puzzles"] = df_data.groupby(["n_interior","n_convex_hull"])["n_puzzles"].transform("min")
        df_data["max_puzzles"] = df_data.groupby(["n_interior","n_convex_hull"])["n_puzzles"].transform("max")
        df_data.to_csv("data/first_stats.csv",index=False)



class TestSampledPointsCreator(unittest.TestCase):
    files_path = "data/run from/" #'data/sampled_points/'
   

    def _run(self,example_name,output_dir):
        # dirs = ["results","visibility-graph-before-filter","visibility-graph-filtered",
        #         "last_decision_junction","last_creation","snapshots","failure"]
        dirs = ["results","failure"]
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            [os.makedirs(output_dir+ f"/{_dir}") for _dir in dirs]
        
        [[os.remove(file.path) for file in os.scandir(os.path.join(output_dir+f"/{_dir}"))] for _dir in dirs]

        board = Board()
        board.load_sampled_points(self.files_path + example_name + ".csv")

        creator = Creator(board,output_dir)
        # fig, ax = plt.subplots()

        try:
            # start_time = time.time()
            creator.create_puzzles(num_puzzles=np.inf)
            
        except Exception as err:
            pass
            raise err
        finally:
            plt.close("all")
            del creator


    def _output_dir(self,example_name):
        current_working_dir = os.getcwd()
        return os.path.join(current_working_dir,"data","puzzles",example_name)
        

    def test_run_from(self):
        for file in os.listdir(self.files_path):
            example_name = file.split(".")[0]
            output_dir = self._output_dir(example_name)
            self._run(example_name,output_dir)
            print("Finish with example " + str(example_name))

    def test_single(self):
        example_name = "frame-4-frame_anchor-4-int-2-103"
        output_dir = self._output_dir(example_name)
        self._run(example_name,output_dir)

    def test_save_trans_peleg_output_format(self):
        example_name = "sample_range-10000-convex_hull-8-int-10-6475"
        output_dir = self._output_dir(example_name)
        puzzle_name = "1-66723_1-3_s_s_1-2112_n_n_1-485_s_1-125_1-45_n_s_s_n_s_"
        first_df = pd.read_csv(f"{output_dir}/results/{puzzle_name}.csv")
        puzzle_peleg = transform_peleg_output(first_df)
        puzzle_peleg.to_csv(output_dir+f"/pelegoutput_{puzzle_name}.csv",index=False)
    
    def test_plot_board(self):
        example_name = "frame-4-frame_anchor-4-int-1-600"
        board = Board()
        board.load_sampled_points(self.files_path + example_name +".csv")
        ax = plt.subplot()
        board.plot(ax)
        plt.show()
        pass