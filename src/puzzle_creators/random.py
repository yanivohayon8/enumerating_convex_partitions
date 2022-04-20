from src.puzzle_creators.skeleton import PuzzleCreator
from src.data_structures import Point
from src.data_structures.shapes import Polygon
from src.data_structures.graph import Edge
import random
import re

import logging
from src import setup_logger


log_handler = setup_logger.get_file_handler(setup_logger.get_debug_log_file())
logger = logging.getLogger("logger.random_creator")
logger.addHandler(log_handler)

class RandomCreator(PuzzleCreator):
    
    def __init__(self):
        super().__init__()
        self.count_scans = 0


    def prepare_to_create(self,kernel_point):
        logger.info(f"n_iter: {str(self.n_iter)}. Next point potential to origin a polygon is {str(kernel_point)}")
        
        _key = f"from {self.scan_direction.name} "+str(kernel_point)

        if _key not in self.last_possible_rgons.keys():
            logger.info("No prior surface scanning at this point and direction, searching for possible polygons.")
            self.last_possible_rgons[_key] = self._find_first_possible_rgons(kernel_point,self.n_iter)
            # self._take_snaphot(kernel_point,self.last_possible_rgons[_key])
        else:
            logger.info("Prior surface scanning at this point and direction Found, filter possible rgons with the surface current status")
            self.last_possible_rgons[_key] = self._filter_poss_rgons(self.last_possible_rgons[_key])
        
        return self.last_possible_rgons[_key]


    def _create_rgon(self,possible_rgons):
        if len(possible_rgons) == 0:
            logger.debug("No option availiable for creating rgon")
            return None
        return random.choice(possible_rgons)

class RestoreRandom(RandomCreator):

    def __init__(self,log_path):
        super().__init__()
        self.polygons_to_create = []

        with open(log_path) as f:
            f = f.readlines()

            for line in f:
                if "Next Polygon to create is" in line:
                    polygon = []
                    vertices_str = re.findall("(\([\s\d,\-.]*\);)",line) # E.g.(1.0,1.0);(11.0,5.0);(5.0,5.0);(2.0,4.0);
                    for vert_str in vertices_str:
                        vert_str = re.sub(r"[;()]","",vert_str)
                        values = vert_str.split(",")
                        vert = Point(float(values[0]),float(values[1]))
                        polygon.append(vert)
                    self.polygons_to_create.append(Polygon(polygon))

    def _create_rgon(self, possible_rgons):
        if len(self.polygons_to_create)>0:
            return self.polygons_to_create.pop(0)

        return super()._create_rgon(possible_rgons)

    