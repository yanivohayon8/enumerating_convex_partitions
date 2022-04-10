from src.puzzle_creators.skeleton import PuzzleCreator
import random

import logging
from src import setup_logger

log_handler = setup_logger.get_file_handler(setup_logger.get_debug_log_file())
logger = logging.getLogger("logger.power_group")
logger.addHandler(log_handler)



class Creator(PuzzleCreator):
    
    def __init__(self):
        super().__init__()
        
        # mapping the 


    def _create_rgon(self, possible_rgons):
        if len(possible_rgons) == 0:
            logger.debug("No option availiable for creating rgon")
            return None
        return random.choice(possible_rgons)
    
    def run(self):
        pas
    