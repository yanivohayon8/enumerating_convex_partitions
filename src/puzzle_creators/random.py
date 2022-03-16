from src.puzzle_creators import PuzzleCreator
from src.data_structures import Polygon,Edge
import random


class RandomCreator(PuzzleCreator):

    def _create_rgon(self, kernel_point, r, edges_max_chain_length, continuity_edges):
        rgon = Polygon()
        rgon.add_vertex(kernel_point)
        r = r - 2

        potential_start_edges = list(filter(lambda e: edges_max_chain_length[e] >=r ,edges_max_chain_length.keys()))

        if len(potential_start_edges)==0:
            raise ("Can't create polygon sized " +str(r) + " from point " + str(kernel_point))
        
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
    
    def _get_next_polygon_num_edges(self):
        return 3

    def _is_finished_scan(self):
        return True