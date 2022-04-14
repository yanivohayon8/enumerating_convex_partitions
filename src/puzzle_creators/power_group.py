from src.puzzle_creators import Direction
from src.puzzle_creators.skeleton import PuzzleCreator
import random
from src.data_structures import Point
from src.data_structures.shapes import Polygon
import re

import logging
from src import setup_logger

log_handler = setup_logger.get_file_handler(setup_logger.get_debug_log_file())
logger = logging.getLogger("logger.power_group")
logger.addHandler(log_handler)


class Snapshot():
    def __init__(self,kernel_point,direction,possible_rgons,\
        is_angles_convex,last_possible_rgons,pieces,pieces_area) -> None:
        self.history = []
        self.first_possible_rgons = possible_rgons
        self.kernel_point = kernel_point
        self.direction = direction
        self.is_angles_convex = is_angles_convex
        self.last_possible_rgons = last_possible_rgons # maybe is not necessray
        self.pieces_area = pieces_area
        self.pieces = pieces

    
    def is_tried_all_paths(self):
        return len(self.history) == len(self.first_possible_rgons)

class PowerGroupCreator(PuzzleCreator):
    
    def __init__(self,output_dir):
        super().__init__()
        self.decision_junc_stack = []
        self.output_dir = output_dir
        # self.puzzle_creator = PuzzleCreator()
    
    def _take_snaphot(self,kernel_point,possible_rgons):
        logger.info(f"Take a snapshot of the board (Decision Juncion object)")
        dec_junc = Snapshot(kernel_point,self.scan_direction,possible_rgons.copy(),\
                    self.is_angles_convex.copy(),self.last_possible_rgons.copy(),self.pieces.copy(),self.pieces_area)
        self.decision_junc_stack.append(dec_junc)

    def get_fit_snapshot(self,kernel_point):
        for i in range(len(self.decision_junc_stack)-1,-1,-1):
            if self.decision_junc_stack[i].direction == self.scan_direction and \
                self.decision_junc_stack[i].kernel_point == kernel_point:
                return self.decision_junc_stack[i]
        return None


    # Need to be deleted
    def _decision_stack_head(self):
        return self.decision_junc_stack[-1]

    def _filter_poss_rgons(self,kernel_point,last_possible_rgons):
        snap = self.get_fit_snapshot(kernel_point)

        if snap is not None:
            last_possible_rgons =  [rgon for rgon in last_possible_rgons if not any(rgon.equals(piece) for piece in snap.history)] 
        
        return super()._filter_poss_rgons(last_possible_rgons)

    def _create_rgon(self, possible_rgons):
        # - 
        # optional_rgons = self._filter_poss_rgons(possible_rgons)
        # last_dec_junc = self._decision_stack_head()

        if len(possible_rgons) == 0:
            logger.debug(f"No option availiable for creating rgon at n_iter: {self.n_iter}")
            return None

        next_poly = possible_rgons[0] #random.choice(possible_rgons)
        
        return next_poly

    def prepare_to_create(self,kernel_point):
        logger.info(f"n_iter: {str(self.n_iter)}. Next point potential to origin a polygon is {str(kernel_point)}")
        
        snap = self.get_fit_snapshot(kernel_point)

        _key = f"from {self.scan_direction.name} "+str(kernel_point)
        # self.is_decision_point = False

        if _key not in self.last_possible_rgons.keys() and snap is None:
            logger.info("No prior surface scanning at this point and direction, searching for possible polygons.")
            self.last_possible_rgons[_key] = self._find_first_possible_rgons(kernel_point,self.n_iter)
            
            if len(self.last_possible_rgons[_key]) > 1:
                self._take_snaphot(kernel_point,self.last_possible_rgons[_key])
                # self.is_decision_point = True
        else:
            logger.info("Prior surface scanning at this point and direction Found, filter possible rgons with the surface current status")
            self.last_possible_rgons[_key] = self._filter_poss_rgons(kernel_point,self.last_possible_rgons[_key])
        
        return self.last_possible_rgons[_key]

    def after_rgon_creation(self, polygon):
        if polygon is not None:
            super().after_rgon_creation(polygon)
            snap = self.get_fit_snapshot(self.last_kernel_point)

            if snap is not None:
                snap.history.append(polygon)


    def create_puzzles(self):
        n_puzzle = 1
        while True:
            super().create()
            logger.info("Finish to assemble a puzzle number:" + str(n_puzzle))
            self.write_results(self.output_dir+f"/results/{str(n_puzzle)}.csv")
            self.plot_results(self.output_dir+f"/results/{str(n_puzzle)}.png")

            while self.decision_junc_stack[-1].is_tried_all_paths():
                self.decision_junc_stack.pop()
            
            self.revert(self.decision_junc_stack[-1])

            # # make a decision
            # _key = f"from {self.scan_direction.name} "+str(self.decision_junc_stack[-1].kernel_point)
            # for rgon in self.last_possible_rgons[_key]:
            #     for piece in self._decision_stack_head().history:
            #         if rgon.equals(piece):
            #             self.last_possible_rgons[_key].remove(rgon)

            # possible_rgons = self._filter_poss_rgons(self.last_possible_rgons[_key])
            # next_polygon = self._create_rgon(self.decision_junc_stack[-1].kernel_point,possible_rgons)
            # if next_polygon is not None:
            #     self.decision_junc_stack[-1].history.append(next_polygon)
            #     self._count_piece(next_polygon)

            if len(self.decision_junc_stack) == 0:
                break

            self.plot_results(self.output_dir+f"/last_decision_junction/{str(self.decision_junc_stack[-1].kernel_point)}-from {str(self.decision_junc_stack[-1].direction)}.png")
            n_puzzle+=1
        

    def revert(self,decision_junction:Snapshot):
        logger.debug(f"Revert to decision junction where direction is {decision_junction.direction.name}, kernel_point is {str(decision_junction.kernel_point)}")
        self._set_direction_scan(decision_junction.direction.value)
        kernel_index = self.space_points.index(decision_junction.kernel_point)
        self.space_points = self.space_points[kernel_index:]
        self.direction = decision_junction.direction
        self.is_angles_convex = decision_junction.is_angles_convex
        self.last_possible_rgons = decision_junction.last_possible_rgons
        self.pieces_area = decision_junction.pieces_area
        self.pieces = decision_junction.pieces

    def plot_results(self,file_path):
        return super().plot_results(file_path) # 





class PowerGroupRestore(PowerGroupCreator):

    def __init__(self,output_dir,log_path):
        super().__init__(output_dir)
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
            next_poly = self.polygons_to_create.pop(0)
            # optional_rgons  = self._filter_poss_rgons(possible_rgons)

            if any(next_poly.equals(poly) for poly in possible_rgons):
                logger.debug(f"Restoring polygon {str(next_poly)} for the creation procedure")
                
                # if len(optional_rgons) > 1:
                # self._decision_stack_head().history.append(next_poly)
                return next_poly
            
            logger.debug(f"Attempt to restore polygon {str(next_poly)} but it is not availiable")
        return super()._create_rgon(possible_rgons)
