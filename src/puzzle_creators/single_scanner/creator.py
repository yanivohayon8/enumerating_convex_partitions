from src.puzzle_creators.single_scanner.surface import find_possible_rgons
from src.puzzle_creators.single_scanner.record import HistoryManager,Snapshot,Choice
from src.puzzle_creators.single_scanner.puzzle_obj import Piece, Puzzle,PuzzleAreaErr,PuzzleEdgeAnglesErr
import matplotlib.pyplot as plt

# class CreatorState():

#     def __init__(self) -> None:
#         pass


class Creator():

    def __init__(self,board,output_dir) -> None:
        self.board = board
        self.output_dir = output_dir
        self.snapshot_queue = []
        self.history_manager = HistoryManager()
        self.fig, self.ax = plt.subplots()

    def find_combinations(self,possible_polygons):
        return possible_polygons

    def create_single(self)->Puzzle:
        
        puzzle = Puzzle(self.board)

        for kernel_point in self.board.space_points:
            try:
                potential_points = self.board.potential_points(kernel_point,self.board.space_points)
                possible_polygons = find_possible_rgons(kernel_point,puzzle,potential_points)
                possible_polygons_combs = self.find_combinations(possible_polygons)
                n = len(possible_polygons_combs)
                options = [Choice(c,is_single=n==1) for c in possible_polygons_combs + ["pass"]]
                
                if len(options) == 1:
                    puzzle.record_choice("n")
                    continue

                snapshot = Snapshot(kernel_point,puzzle,options)
                if not self.history_manager.is_recorded(snapshot):
                    self.snapshot_queue.append(snapshot)

                next_choice_index = self.history_manager.next_availiable(repr(snapshot))
                curr_choice = options[next_choice_index]
                
                if isinstance(curr_choice.val,Piece):
                    puzzle.check_sanity_polygon(curr_choice.val.polygon)                
                    puzzle._count_piece(curr_choice)

                puzzle.record_choice(curr_choice.name)

            except ValueError as err:
                raise err

        return puzzle


    def create_puzzles(self):
        while True:

            puzzle = self.create_single()

            try:
                puzzle.is_completed(self.board.frame_polygon)
                puzzle.write_results(self.output_dir+f"/results/{str(puzzle.name)}.csv")
                self.ax.cla()
                puzzle.plot(self.fig,self.ax)
                self.fig.savefig(self.output_dir+f"/results/{str(puzzle.name)}.png")
            except PuzzleAreaErr :
                pass
            except PuzzleEdgeAnglesErr:
                pass
            
            while len(self.snapshot_queue) > 0:
                last_snap = self.snapshot_queue[-1]

                if not last_snap.is_tried_all_paths(self.history_manager.head_availiable(repr(last_snap))):
                    break

                self.snapshot_queue.pop()

            if len(self.snapshot_queue) == 0:
                # self.logger.info("Finish to create all puzzles")
                break
