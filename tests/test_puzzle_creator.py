import sys
import os

from src.puzzle_creators import Direction

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import unittest
from src.puzzle_creators.skeleton import PuzzleCreator
from src.puzzle_creators.random import RandomCreator,RestoreRandom
from src.puzzle_creators.power_group.primary import PowerGroupCreator
import matplotlib.pyplot as plt
import logging
from src import setup_logger


class TestParentCreator(unittest.TestCase):

    files_path = 'data/starting_points/'
        
    def test_data_loading(self):
        creator = PuzzleCreator()
        creator.load_sampled_points(self.files_path + "TBN_01.csv")

        fig, ax = plt.subplots()
        creator.plot_scratch(ax)
        
        plt.show()


        pass


class TestRandomCreator(unittest.TestCase):

    files_path = 'data/starting_points/'
    example_name =  "general_002.csv" # "TBN_01.csv"

    def test_example_01_restored(self):
        
        debug_dir = setup_logger.get_debug_lastrun_dir()
        for file in os.scandir(os.path.join(debug_dir,"results")):
            os.remove(file.path)

        for file in os.scandir(os.path.join(debug_dir,"visibility-graph-before-filter")):
            os.remove(file.path)

        for file in os.scandir(os.path.join(debug_dir,"visibility-graph-filtered")):
            os.remove(file.path)    

        log_path = setup_logger.get_cwd()+"/data/debug/TBN_01_02/run.log" #setup_logger.get_debug_log_file()
        creator = RestoreRandom(log_path)

        # Override last running directory
        log_handler = setup_logger.get_file_handler(setup_logger.get_debug_log_file(),mode="w")
        logger = logging.getLogger("logger.test_puzzle_creator")
        logger.addHandler(log_handler)
        logger.debug("Starting....")

        creator.load_sampled_points(self.files_path + self.example_name)
        fig, ax = plt.subplots()

        try:
            creator.create()
            creator.plot_puzzle(fig,ax)
            plt.show()
            fig.savefig(debug_dir + "/results.png")
        except Exception as err:
            raise err

        pass

    def test_example_01_logged(self):
        

        debug_dir = setup_logger.get_debug_lastrun_dir()
        for file in os.scandir(os.path.join(debug_dir,"results")):
            os.remove(file.path)

        for file in os.scandir(os.path.join(debug_dir,"visibility-graph-before-filter")):
            os.remove(file.path)

        for file in os.scandir(os.path.join(debug_dir,"visibility-graph-filtered")):
            os.remove(file.path)    
            
        # Override last running directory
        log_handler = setup_logger.get_file_handler(setup_logger.get_debug_log_file(),mode="w")
        logger = logging.getLogger("logger.test_puzzle_creator")
        logger.addHandler(log_handler)
        logger.debug("Starting....")

        creator = RandomCreator()
        creator.load_sampled_points(self.files_path + self.example_name)
        fig, ax = plt.subplots()

        try:
            creator.create()
            creator.plot_puzzle(fig,ax)
            plt.show()
            fig.savefig(debug_dir + "/results.png")
            creator.write_results(debug_dir + "/puzzle.csv")

        except Exception as err:
            # logger.exception(err)
            raise err

        plt.close("all")

class TestPowergroupCreator(unittest.TestCase):
    files_path = 'data/starting_points/'
   

    def test_simple_square(self):
        example_name = "simple_square"
        current_working_dir = os.getcwd()
        output_dir = os.path.join(current_working_dir,"data","debug_powergroup_creator",example_name)

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            os.makedirs(output_dir+"/results")
            os.makedirs(output_dir+"/visibility-graph-before-filter")
            os.makedirs(output_dir+"/visibility-graph-filtered")
            os.makedirs(output_dir+"/last_decision_junction")
            os.makedirs(output_dir+"/last_creation")
            os.makedirs(output_dir+"/snapshots")
        
        for file in os.scandir(os.path.join(output_dir+"/results")):
            os.remove(file.path)
        
        for file in os.scandir(os.path.join(output_dir,"visibility-graph-before-filter")):
            os.remove(file.path)

        for file in os.scandir(os.path.join(output_dir,"visibility-graph-filtered")):
            os.remove(file.path)    
        
        for file in os.scandir(os.path.join(output_dir,"last_decision_junction")):
            os.remove(file.path)    

        for file in os.scandir(os.path.join(output_dir,"last_creation")):
            os.remove(file.path)  

        for file in os.scandir(os.path.join(output_dir,"snapshots")):
            os.remove(file.path)  

        setup_logger.set_debug_lastrun_dir(output_dir)
        log_handler = setup_logger.get_file_handler(os.path.join(output_dir,"run.log"),mode="w")
        logger = logging.getLogger("logger.test_puzzle_creator")
        logger.addHandler(log_handler)
        logger.debug("Starting....")

        creator = PowerGroupCreator(output_dir)
        creator.load_sampled_points(self.files_path + example_name +".csv")
        # fig, ax = plt.subplots()

        try:
            creator.create_puzzles()
        except Exception as err:
            # logger.exception(err)
            raise err

        plt.close("all")


    def test_simple_square_crossing_cuts(self):
        example_name = "simple_square_crossing_cuts"
        current_working_dir = os.getcwd()
        output_dir = os.path.join(current_working_dir,"data","debug_powergroup_creator",example_name)

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            os.makedirs(output_dir+"/results")
            os.makedirs(output_dir+"/visibility-graph-before-filter")
            os.makedirs(output_dir+"/visibility-graph-filtered")
            os.makedirs(output_dir+"/last_decision_junction")
            os.makedirs(output_dir+"/last_creation")
            os.makedirs(output_dir+"/snapshots")
        
        for file in os.scandir(os.path.join(output_dir+"/results")):
            os.remove(file.path)
        
        for file in os.scandir(os.path.join(output_dir,"visibility-graph-before-filter")):
            os.remove(file.path)

        for file in os.scandir(os.path.join(output_dir,"visibility-graph-filtered")):
            os.remove(file.path)    
        
        for file in os.scandir(os.path.join(output_dir,"last_decision_junction")):
            os.remove(file.path)    

        for file in os.scandir(os.path.join(output_dir,"last_creation")):
            os.remove(file.path)  

        for file in os.scandir(os.path.join(output_dir,"snapshots")):
            os.remove(file.path)  

        setup_logger.set_debug_lastrun_dir(output_dir)
        log_handler = setup_logger.get_file_handler(os.path.join(output_dir,"run.log"),mode="w")
        logger = logging.getLogger("logger.test_puzzle_creator")
        logger.addHandler(log_handler)
        logger.debug("Starting....")

        creator = PowerGroupCreator(output_dir)
        creator.load_sampled_points(self.files_path + example_name +".csv")
        # fig, ax = plt.subplots()

        try:
            creator.create_puzzles()
        except Exception as err:
            # logger.exception(err)
            raise err

        plt.close("all")