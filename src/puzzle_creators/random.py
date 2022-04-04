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

    def _create_rgon(self, kernel_point, r, edges_max_chain_length, continuity_edges):
        rgon = [kernel_point]
        r = r - 2
        
        if r <=0:
            return None


        potential_start_edges = list(filter(lambda e: edges_max_chain_length[e] >=r ,edges_max_chain_length.keys()))

        if len(potential_start_edges)==0:
            return None
        
        next_edge = Edge(random.choice(potential_start_edges))
        rgon.append(next_edge.src_point)

        while True:
            rgon.append(next_edge.dst_point)
            r-=1

            if r <= 0:
                break
            
            potential_start_edges = list(filter(lambda e: edges_max_chain_length[str(e)] >=r ,
                                                continuity_edges[str(next_edge)]))
            next_edge = random.choice(potential_start_edges)

        return Polygon(rgon)
    
    def _get_next_polygon_num_verticies(self,continuity_edges,edges_max_chain_length):
        logger.debug("Randomizing the number of edges to travel on them in the visibility graph")
        possble_edge_len = [edges_max_chain_length[_key] for _key in edges_max_chain_length.keys()]
        try:
            min_len = min(possble_edge_len)
            max_len = max(possble_edge_len)
        except ValueError:
            return 0
        if max_len <= 0:
            logger.debug("No edge is available - return 0")            
            return 0

        logger.debug(f"Random int number in range [{str(min_len)},{str(max_len)}]")
        random_num = random.randint(min_len,max_len) + 2
        logger.debug(f"Randomizing results is {str(random_num)}")
        return random_num

    def _is_finished_scan(self):
        self.count_scans +=1
        return self.count_scans >= 2


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

    def _create_rgon(self, kernel_point, r, edges_max_chain_length, continuity_edges):
        if len(self.polygons_to_create)>0:
            return self.polygons_to_create.pop(0)

        return super()._create_rgon(kernel_point, r, edges_max_chain_length, continuity_edges)

    