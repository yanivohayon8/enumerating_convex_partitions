from src.puzzle_creators import PuzzleCreator
from src.data_structures import Point
from src.data_structures.shapes import Polygon
from src.data_structures.graph import Edge
import random
import re

class RandomCreator(PuzzleCreator):
    
    def __init__(self):
        super().__init__()
        self.count_scans = 0

    def _create_rgon(self, kernel_point, r, edges_max_chain_length, continuity_edges):
        rgon = Polygon()
        rgon.add_vertex(kernel_point)
        r = r - 2

        potential_start_edges = list(filter(lambda e: edges_max_chain_length[e] >=r ,edges_max_chain_length.keys()))

        if len(potential_start_edges)==0:
            #raise Exception("Can't create polygon sized " +str(r) + " from point " + str(kernel_point))
            return None
        
        next_edge = Edge(random.choice(potential_start_edges))

        while True:
            rgon.add_vertex(next_edge.src_point)
            rgon.add_vertex(next_edge.dst_point)
            r-=1

            if r <= 0:
                break
            
            potential_start_edges = list(filter(lambda e: edges_max_chain_length[str(e)] >=r ,
                                                continuity_edges[str(next_edge)]))
            next_edge = random.choice(potential_start_edges)

        return rgon
    
    def _get_next_polygon_num_edges(self,continuity_edges,edges_max_chain_length):
        possble_edge_len = [edges_max_chain_length[_key] for _key in edges_max_chain_length.keys()]
        try:
            min_len = min(possble_edge_len)
            max_len = max(possble_edge_len)
        except:
            return 0
        # if min_len == 0:
        #     return 0
        return random.randint(min_len,max_len) + 2
        # return 3

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
                    polygon = Polygon()
                    vertices_str = re.findall("(\([\d,\-.]*\);)",line) # E.g.(1.0,1.0);(11.0,5.0);(5.0,5.0);(2.0,4.0);
                    for vert_str in vertices_str:
                        vert_str = re.sub(r"[;()]","",vert_str)
                        values = vert_str.split(",")
                        vert = Point(float(values[0]),float(values[1]))
                        polygon.add_vertex(vert)
                    self.polygons_to_create.append(polygon)

    def _create_rgon(self, kernel_point, r, edges_max_chain_length, continuity_edges):
        if len(self.polygons_to_create)>0:
            return self.polygons_to_create.pop(0)

        return super()._create_rgon(kernel_point, r, edges_max_chain_length, continuity_edges)

    