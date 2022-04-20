from src.puzzle_creators import Direction,Junction
from src.puzzle_creators.skeleton import PuzzleCreator
import random
from src.data_structures import Point
from src.data_structures.shapes import Polygon
import re

import logging
from src import setup_logger
from matplotlib import pyplot as plt
import os

# import copy


log_handler = setup_logger.get_file_handler(setup_logger.get_debug_log_file())
logger = logging.getLogger("logger.power_group")
logger.addHandler(log_handler)


class Snapshot():
    def __init__(self,junction:Junction,possible_rgons,\
        is_angles_convex,last_possible_rgons,pieces,pieces_area) -> None:
        self._junction = junction # key
        # self._kernel_point = kernel_point # key
        # self._direction = direction # key
        # self.history = []
        self._kernel_first_rgon_options = possible_rgons 
        self._is_angles_convex = is_angles_convex
        self._possible_rgon_at = last_possible_rgons #self.last_possible_rgons = last_possible_rgons # maybe is not necessray
        self._pieces = pieces
        self._pieces_area = pieces_area
    
    def __repr__(self) -> str:
        return repr(self._junction) 
    
    @property
    def kernel_first_rgon_options(self):
        return self._kernel_first_rgon_options
    
    @property
    def is_angles_convex(self):
        return self._is_angles_convex
    
    @property
    def possible_rgon_at(self,junction:Junction):
        return self._possible_rgon_at[repr(junction)]

    @property
    def pieces(self):
        return self._pieces

    @property
    def pieces_area(self):
        return self._pieces_area


    def is_tried_all_paths(self,history_choices):
        return len(history_choices) == len(self.first_possible_rgons)

class PowerGroupCreator(PuzzleCreator):
    
    def __init__(self,output_dir):
        super().__init__()
        self.decision_junc_stack = () #[]
        self.output_dir = output_dir
        self.choices_history_at_snap = {}
    
    def _take_snaphot(self,kernel_point,possible_rgons,curr_pieces):
        logger.info(f"Take a snapshot of the board (Decision Juncion object)")
        # nisuy = [Polygon(p.exterior.coords) for p in self.pieces]
        dec_junc = Snapshot(kernel_point,self.scan_direction,possible_rgons.copy(),\
                ("blabla",dict(self.is_angles_convex)),("blabla",dict(self.last_possible_rgons)),tuple(curr_pieces),self.pieces_area)
        self.decision_junc_stack = list(self.decision_junc_stack)
        self.decision_junc_stack.append(dec_junc)
        self.decision_junc_stack = tuple(self.decision_junc_stack)

    def get_fit_snapshot(self,kernel_point):
        for i in range(len(self.decision_junc_stack)-1,-1,-1):
            if self.decision_junc_stack[i].direction == self.scan_direction and \
                self.decision_junc_stack[i].kernel_point == kernel_point:
                return self.decision_junc_stack[i]
        return None


    # Need to be deleted
    # def _decision_stack_head(self):
    #     return self.decision_junc_stack[-1]

    def _filter_poss_rgons(self,kernel_point,last_possible_rgons):
        # snap = self.get_fit_snapshot(kernel_point)
        # possible_rgons = []
        # if snap is not None:
        #     possible_rgons =  [rgon for rgon in last_possible_rgons if not any(rgon.equals(piece) for piece in snap.history)] 
        
        # return super()._filter_poss_rgons(possible_rgons)
        return super()._filter_poss_rgons(last_possible_rgons)

    def _create_rgon(self, possible_rgons):

        if len(possible_rgons) == 0:
            logger.debug(f"No option availiable for creating rgon at n_iter: {self.n_iter}")
            return None

        next_poly = possible_rgons[0] #random.choice(possible_rgons)
        
        return next_poly

    def prepare_to_create(self,kernel_point):
        logger.info(f"n_iter: {str(self.n_iter)}. Next point potential to origin a polygon is {str(kernel_point)}")
        
        # snap = self.get_fit_snapshot(kernel_point)

        _key = f"from {self.scan_direction.name} "+str(kernel_point)

        if _key not in self.last_possible_rgons.keys(): #and snap is None:
            logger.info("No prior surface scanning at this point and direction, searching for possible polygons.")
            self.last_possible_rgons[_key] = self._find_first_possible_rgons(kernel_point,self.n_iter)
            
            if len(self.last_possible_rgons[_key]) > 1:
                self._take_snaphot(kernel_point,self.last_possible_rgons[_key],[Polygon(p.exterior.coords) for p in self.pieces])
        else:
            logger.info("Prior surface scanning at this point and direction Found, filter possible rgons with the surface current status")
            self.last_possible_rgons[_key] = self._filter_poss_rgons(kernel_point,self.last_possible_rgons[_key])
        
        return self.last_possible_rgons[_key]

    def after_rgon_creation(self, polygon):
        if polygon is not None:
            super().after_rgon_creation(polygon)
            snap = self.get_fit_snapshot(self.last_kernel_point)

            if snap is not None:
                self.decision_junc_stack = list(self.decision_junc_stack)
                snap.history.append(polygon)
                self.decision_junc_stack = tuple(self.decision_junc_stack)
        
            fig,ax = plt.subplots()
            self.plot_puzzle(fig,ax)
            fig.suptitle(f'At {str(self.last_kernel_point)}-from {str(self.scan_direction.name)}')
            fig.savefig(self.output_dir+f"/last_creation/n_iter_{self.n_iter}.png") 
            plt.close()


    def create_puzzles(self):
        self.n_puzzle = 1
        while True:
            super().create()
            logger.info("Finish to assemble a puzzle number:" + str(self.n_puzzle))
            self.write_results(self.output_dir+f"/results/{str(self.n_puzzle)}.csv")
            self.plot_results(self.output_dir+f"/results/{str(self.n_puzzle)}.png")

            self.decision_junc_stack = list(self.decision_junc_stack)
            while self.decision_junc_stack[-1].is_tried_all_paths():
                self.decision_junc_stack.pop()
                logger.debug(f"Poped head of stack of snapshots. left with {len(self.decision_junc_stack)}")
            
            self.decision_junc_stack = tuple(self.decision_junc_stack)

            last_snap = self.decision_junc_stack[-1]
            _key = f"from {last_snap.direction.name} "+str(last_snap.kernel_point)
            last_possible_rgons = last_snap.last_possible_rgons[1] # maybe get this from a getter

            # for _key in last_possible_rgons.keys():
            last_possible_rgons[_key] = [rgon for rgon in last_possible_rgons[_key] if not any(rgon.equals(piece) for piece in last_snap.history)] 

            self.revert(last_snap)

            if len(self.decision_junc_stack) == 0:
                break
            
            logger.info("Plot the current state of the puzzle, and the previous choices hatched")
            fig_path = self.output_dir+f"/last_decision_junction/After puzzle {str(self.n_puzzle)} creation.png"
            fig,axs = plt.subplots(1,3,sharey=True)
            self.plot_puzzle(fig,axs[0])
            axs[0].set_title("Puzzle Snapshot")
            self.plot_puzzle(fig,axs[1],last_snap.history,hatch='\\/...')
            axs[1].set_title("Choises History")
            self.plot_puzzle(fig,axs[2],last_snap.last_possible_rgons[1][_key])
            axs[2].set_title("Possiblities")


            fig.suptitle(f'Snapshot at {str(last_snap.kernel_point)}-from {str(last_snap.direction)}')
            fig.autofmt_xdate()

            fig.savefig(fig_path)
            plt.close()    
            self.n_puzzle+=1

            for file in os.scandir(os.path.join(self.output_dir,"last_creation")):
                os.remove(file.path) 
        

    def revert(self,decision_junction:Snapshot):
        logger.debug(f"Revert to decision junction where direction is from {decision_junction.direction.name}, kernel_point is {str(decision_junction.kernel_point)}")
        self._set_direction_scan(decision_junction.direction.value)
        kernel_index = self.space_points.index(decision_junction.kernel_point)
        self.space_points = self.space_points[kernel_index:]
        self.scan_direction = decision_junction.direction
        self.is_angles_convex = decision_junction.is_angles_convex[1] # [1] because of the tuple
        self.last_possible_rgons = decision_junction.last_possible_rgons[1] # [1] because of the tuple
        self.pieces = list(decision_junction.pieces)
        self.pieces_area = decision_junction.pieces_area


    def _get_surface(self, kernel_point, scan_direction, n_iter=-1):
        return super()._get_surface(kernel_point, scan_direction, n_iter, fig_prefix=f"{str(self.n_puzzle)}_")




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

            if any(next_poly.equals(poly) for poly in possible_rgons):
                logger.debug(f"Restoring polygon {str(next_poly)} for the creation procedure")
                
                # if len(optional_rgons) > 1:
                # self._decision_stack_head().history.append(next_poly)
                return next_poly
            
            logger.debug(f"Attempt to restore polygon {str(next_poly)} but it is not availiable")
        return super()._create_rgon(possible_rgons)
