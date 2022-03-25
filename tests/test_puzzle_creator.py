import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import unittest
from src.puzzle_creators import PuzzleCreator
from src.puzzle_creators.random import RandomCreator,RestoreRandom
import matplotlib.pyplot as plt
import logging
from src import setup_logger

# plt.close('all')

import shutil

# logging.basicConfig()#level=logging.DEBUG,filename=log_path, filemode='w', format='%(name)s - %(levelname)s - %(message)s')


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
    
    def test_example_01_restored(self):
        
        log_path = setup_logger.get_cwd()+"/data/debug/2403insertSL/run.log" #setup_logger.get_debug_log_file()

        creator = RestoreRandom(log_path)

        # Override last running directory
        log_handler = setup_logger.get_file_handler(setup_logger.get_debug_log_file(),mode="w")
        logger = logging.getLogger("logger.test_puzzle_creator")
        logger.addHandler(log_handler)
        logger.debug("Starting....")

        creator.load_sampled_points(self.files_path + "TBN_01.csv")
        debug_dir = setup_logger.get_debug_lastrun_dir()
        fig, ax = plt.subplots()

        try:
            creator.create()
            creator.plot_puzzle(fig,ax)
            plt.show()
            fig.savefig(debug_dir + "/results.png")
        except Exception as err:
            # logger.exception(err)
            raise err

        # plt.show()
        pass

    def test_example_01_logged(self):
        
        # Override last running directory
        debug_dir = setup_logger.get_debug_lastrun_dir()
        # shutil.rmtree(debug_dir)
        # os.makedirs(debug_dir)
        log_handler = setup_logger.get_file_handler(setup_logger.get_debug_log_file(),mode="w")
        logger = logging.getLogger("logger.test_puzzle_creator")
        logger.addHandler(log_handler)
        logger.debug("Starting....")

        creator = RandomCreator()
        creator.load_sampled_points(self.files_path + "TBN_01.csv")
        fig, ax = plt.subplots()

        try:
            creator.create()
            creator.plot_puzzle(fig,ax)
            plt.show()
        except Exception as err:
            # logger.exception(err)
            plt.close("all")
            raise err
        
        pass

    # def test_example_01(self):
    #     creator = RandomCreator()
    #     creator.load_sampled_points(self.files_path + "TBN_01.csv")
    #     fig, ax = plt.subplots()
    #     try:
    #         creator.create()
    #         creator.plot_puzzle(fig,ax)
    #         plt.show()
    #     except Exception as err:
    #         logger.excep
    #         raise err


if __name__ == "__main__":
    unittest.main()
    # TestSweepLine.test_line_status_insert()
    pass
    