
# from data_structures.shapes import Polygon
from src.data_structures.shapes import Polygon
from src.puzzle_creators.power_group import HistoryManager,Snapshot
from src.puzzle_creators import Junction
from src.puzzle_creators.skeleton import PuzzleCreator
from matplotlib import pyplot as plt
import os
import logging
from src import setup_logger

log_handler = setup_logger.get_file_handler(setup_logger.get_debug_log_file())
logger = logging.getLogger("logger.power_group")
logger.addHandler(log_handler)


class PowerGroupCreator(PuzzleCreator):
    
    def __init__(self,output_dir):
        super().__init__()
        self.snapshot_queue = [] #[]
        self.output_dir = output_dir
        self.history_manager = HistoryManager()
        self.puzzles = []
    
    def _create_rgon(self, possible_rgons):

        if len(possible_rgons) == 0:
            logger.debug(f"No option availiable for creating rgon at n_iter: {self.n_iter}")
            return None

        next_poly = possible_rgons[0] #random.choice(possible_rgons)
        
        return next_poly

    def prepare_to_create(self,kernel_point):
        logger.info(f"n_iter: {str(self.n_iter)}. Next point potential to origin a polygon is {str(kernel_point)}")
        
        # snap = self.get_fit_snapshot(kernel_point)

        _key = f"from {self.scan_direction.name} at "+str(kernel_point)

        if _key not in self.last_possible_rgons.keys(): #and snap is None:
            logger.info("No prior surface scanning at this point and direction, searching for possible polygons.")
            self.last_possible_rgons[_key] = self._find_first_possible_rgons(kernel_point,self.n_iter)
            
            if len(self.last_possible_rgons[_key]) > 1:
                logger.info(f"Take a snapshot of the board (Decision Juncion object)")
                snapshot = Snapshot(Junction(kernel_point,self.scan_direction),dict(self.last_possible_rgons),
                                    self.pieces.copy(),self.pieces_area)
                
                fig,axs = plt.subplots(1,2,sharey=True)
                self.plot_puzzle(fig,axs[0],snapshot.pieces)
                axs[0].set_title("Puzzle")
                self.plot_puzzle(fig,axs[1],self.last_possible_rgons[_key])
                axs[1].set_title("Possibilities")
                fig.suptitle(f'Snapshot {repr(snapshot)}')
                fig.savefig(self.output_dir+f"/snapshots/{str(snapshot.id)}.png")

                self.snapshot_queue.append(snapshot)
                
        else:
            logger.info("Prior surface scanning at this point and direction Found, filter possible rgons with the surface current status")
            self.last_possible_rgons[_key] = self._filter_poss_rgons(self.last_possible_rgons[_key])
        
        return self.last_possible_rgons[_key]

    def after_rgon_creation(self, polygon):
        super().after_rgon_creation(polygon)
        if polygon is not None:
            
            self.history_manager.add(Junction(self.last_kernel_point, self.scan_direction),self.snapshot_queue,polygon)
        
            fig,ax = plt.subplots()
            self.plot_puzzle(fig,ax)
            fig.suptitle(f'At {str(self.last_kernel_point)}-from {str(self.scan_direction.name)}')
            fig.savefig(self.output_dir+f"/last_creation/n_iter_{self.n_iter}.png") 
            plt.close()


    def create_puzzles(self):
        self.n_puzzle = 1
        
        while True:
            super().create()
            logger.info("Finish to assemble puzzle - check if it is equal to previous puzzle (recursive algo duplicates)")
            
            if not any(all(any(curr_puzzle_piece.equals(exist_puzz_piece) for curr_puzzle_piece in self.pieces) for exist_puzz_piece in exist_puzzle) for exist_puzzle in self.puzzles):
                new_puzzle = []
                for piece in self.pieces:
                    deep_copy_poly = Polygon(piece.exterior.coords)
                    new_puzzle.append(deep_copy_poly)

                self.puzzles.append(new_puzzle)
                logger.info("Finish to assemble a puzzle number:" + str(self.n_puzzle) +". save to file")
                self.write_results(self.output_dir+f"/results/{str(self.n_puzzle)}.csv")
                self.plot_results(self.output_dir+f"/results/{str(self.n_puzzle)}.png")
                self.n_puzzle+=1
            else:
                logger.info("already created this puzlle")

            

            while len(self.snapshot_queue) > 0:
                last_snap = self.snapshot_queue[-1]
                choices_history = self.history_manager.choices_history_at_snap[repr(last_snap)]

                if not last_snap.is_tried_all_paths(choices_history):
                    logger.info(f"Did not traversed on all snapshot possibilities at {repr(last_snap)} - preparing to try different rgon options")
                    break

                self.snapshot_queue.pop()

            if len(self.snapshot_queue) == 0:
                logger.info("Finish to create all puzzles")
                break
        
            self.revert(last_snap)
            
            logger.info("Plot the current state of the puzzle, and the previous choices hatched")
            fig_path = self.output_dir+f"/last_decision_junction/After puzzle {str(self.n_puzzle)} creation.png"
            fig,axs = plt.subplots(1,3,sharey=True)
            self.plot_puzzle(fig,axs[0])
            axs[0].set_title("The Puzzle")
            self.plot_puzzle(fig,axs[1],self.history_manager.choices_history_at_snap[repr(last_snap)],hatch='\\/...')
            axs[1].set_title("Choises History")
            self.plot_puzzle(fig,axs[2],self.last_possible_rgons[repr(last_snap.junction)])
            axs[2].set_title("Possiblities")


            fig.suptitle(f'Snapshot at {str(last_snap.junction.kernel_point)}-from {str(last_snap.junction.from_direction)}')
            fig.autofmt_xdate()

            fig.savefig(fig_path)
            plt.close()    

            for file in os.scandir(os.path.join(self.output_dir,"last_creation")):
                os.remove(file.path) 
        

    def revert(self,snapshot:Snapshot):
        logger.debug(f"Revert to decision junction where direction is from {snapshot.junction.from_direction.name}, kernel_point is {str(snapshot.junction.kernel_point)}")
        self._set_direction_scan(snapshot.junction.from_direction.value)
        kernel_index = self.space_points.index(snapshot.junction.kernel_point)
        self.space_points = self.space_points[kernel_index:]
        self.scan_direction = snapshot.junction.from_direction
        self.last_possible_rgons = snapshot.possible_rgon_at.copy()
        updated_junc_pieces = []
        junction_history = self.history_manager.choices_history_at_snap[repr(snapshot)]
        for rgon in snapshot.possible_rgon_at[repr(snapshot.junction)]:
            if not any(rgon.equals(piece) for piece in junction_history):
                updated_junc_pieces.append(rgon)
        self.last_possible_rgons[repr(snapshot.junction)] = updated_junc_pieces
        
        self.pieces = list(snapshot.pieces)
        self.pieces_area = snapshot.pieces_area


    def _get_surface(self, kernel_point, scan_direction, n_iter=-1):
        return super()._get_surface(kernel_point, scan_direction, n_iter, fig_prefix=f"{str(self.n_puzzle)}_")




