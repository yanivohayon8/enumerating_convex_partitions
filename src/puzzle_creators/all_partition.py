from src.puzzle_creators.utils.surface import find_possible_rgons,get_stared_shaped_polygon,get_accessible_points
from src.puzzle_creators.utils.record import HistoryManager,Snapshot,Choice
from src.puzzle_creators.utils.puzzle_obj import Puzzle,PuzzleAreaErr,PuzzleEdgeAnglesErr
from src.data_structures import Point
from src.data_structures.shapes import Polygon
import matplotlib.pyplot as plt
from datetime import datetime
from random import randint,random
from src.seed_points.board import Board


class AllPartitionsCreator():

    def __init__(self,board:Board,output_dir,is_plg_format=True,is_save_partitions_figures=True) -> None:
        self.board = board
        self.output_dir = output_dir
        self.snapshot_queue = []
        self.history_manager = HistoryManager()
        self.is_plg_format = is_plg_format
        self.is_save_partitions_figures = is_save_partitions_figures
        
        if self.is_save_partitions_figures:
            self.fig, self.ax = plt.subplots()

    def find_combinations(self,kernel_point,possible_polygons):
        connected_points = set()
        for pol in possible_polygons:
            coords = pol.exterior.coords
            for cor in coords:
                p = Point(cor)
                if p!=kernel_point:
                    connected_points.add(Point(cor))

        connected_points = list(connected_points)
        stared_polygon_coords = get_stared_shaped_polygon(kernel_point,connected_points).exterior.coords
        start_point,end_point = stared_polygon_coords[-2],stared_polygon_coords[1]

        polygons_start_at_point = {}
        for polygon in possible_polygons:
            coords = [Point(cor) for cor in polygon.exterior.coords[1:-1]]
            k_point = Point(polygon.exterior.coords[0])
            poly = get_stared_shaped_polygon(k_point,coords)
            first_point_str = str(poly.exterior.coords[-2])

            if first_point_str not in polygons_start_at_point.keys():
                polygons_start_at_point[str(first_point_str)] = []
            
            polygons_start_at_point[str(first_point_str)].append(poly)
        
        possibilities = []
        for poly in polygons_start_at_point[str(start_point)]:
            comb = [poly]
            poly_end_point = poly.exterior.coords[1]
            poss_start_with_poly = self.combs_rec(poly_end_point,end_point,polygons_start_at_point,comb)
            possibilities = possibilities + poss_start_with_poly

        return possibilities

    
    def combs_rec(self,start_point,end_point,polygons_start_at_point,comb):
        if start_point == end_point:
            return [comb]
        
        poss = []
        for next_poly in polygons_start_at_point[str(start_point)]:
            comb_copy = comb[:]
            comb_copy.append(next_poly)
            next_end_point = next_poly.exterior.coords[1]
            next_combs = self.combs_rec(next_end_point,end_point,
                                        polygons_start_at_point,comb_copy)
            poss = poss + next_combs
        
        return poss
    

    def create_single(self,puzzle:Puzzle,scanned_points)->Puzzle:
        
        for kernel_point in scanned_points:
            try:
                if not self.history_manager.is_recorded(str(kernel_point)):
                    potential_points = self.board.potential_points(kernel_point,self.board.space_points)
                    points_to_connect = get_accessible_points(kernel_point,puzzle.polygons,potential_points)
                    possible_polygons = find_possible_rgons(kernel_point,puzzle,points_to_connect)

                    if len(possible_polygons) == 0:
                        puzzle.record_choice("n")
                        continue

                    possible_polygons_combs = self.find_combinations(kernel_point,possible_polygons)
                    n = len(possible_polygons_combs)
                    options = [Choice(c,f"{index+1}-{n}",is_single=n==1) for index,c in enumerate(possible_polygons_combs)]
                
                    copy_polygons = [Polygon(poly.exterior.coords) for poly in puzzle.polygons]
                    snapshot = Snapshot(kernel_point,
                                        Puzzle(self.board,copy_polygons,puzzle.name,puzzle.pieces_area),
                                        options)
                    self.snapshot_queue.append(snapshot)

                    self.history_manager.record_tilings(repr(snapshot),options)
                else:
                    last_snapshot = self.snapshot_queue[-1]
                    options = self.history_manager.get_recorded_tilings(repr(last_snapshot))

                next_choice_index = self.history_manager.next_availiable(str(kernel_point))
                curr_choice = options[next_choice_index]
                
                if isinstance(curr_choice.val,list):
                    for poly in curr_choice.val:
                        puzzle.check_sanity_polygon(poly)                
                        puzzle._count_piece(poly)

                puzzle.record_choice(curr_choice.name)

                if puzzle.is_filled():
                    return puzzle

            # except ValueError as err:
            #     raise err
            
            except Exception as err:
                print("Failure . puzzle name " + puzzle.name + ". svae fig in failure folder.")
                self.ax.cla()
                puzzle.plot_naive(self.ax)
                self.fig.savefig(self.output_dir+f"/failure/naive {kernel_point} {str(puzzle.name)}.png")
                self.ax.cla()
                puzzle.plot(self.ax,self.snapshot_queue)
                self.fig.savefig(self.output_dir+f"/failure/{kernel_point} {str(puzzle.name)}.png")
                raise err

        return puzzle


    def run(self):        
        count_puzzles = 0
        scanned_points,puzzle = self.initialize(self.board.space_points[0])

        while True:
            puzzle = self.create_single(puzzle,scanned_points)

            try:
                puzzle.is_completed()
                dst_path = self.output_dir+f"/{str(puzzle.name)}.csv"
                puzzle.write_results(dst_path,is_plg_format=self.is_plg_format)
                count_puzzles+=1
                
                if self.is_save_partitions_figures:                    
                    self.ax.cla()
                    puzzle.plot_shades(self.ax,linewidth=3,edgecolor="0")
                    self.fig.savefig(self.output_dir+f"/results/{str(puzzle.name)}.png")

            except (PuzzleAreaErr,PuzzleEdgeAnglesErr) as e:
                raise e
            
            while len(self.snapshot_queue) > 0:
                last_snap = self.snapshot_queue[-1]
                next_option = self.history_manager.head_availiable(repr(last_snap))
                
                if not last_snap.is_tried_all_paths(next_option):
                    break

                self.snapshot_queue.pop()

            if len(self.snapshot_queue) == 0:
                break

            scanned_points,puzzle = self.initialize(last_snap.kernel_point,last_snap.puzzle)
        
        print(f"Created {count_puzzles} puzzles")
    
    def initialize(self,start_kernel_point,puzzle=None):
        start_point_index = self.board.space_points.index(start_kernel_point)
        scanned_points = self.board.space_points[start_point_index:]
        last_point_x = max([p.x for p in scanned_points])
        scanned_points = list(filter(lambda p: p.x < last_point_x,scanned_points))
        remember_history_points = [str(p) for p in self.board.space_points[:start_point_index+1]]
        self.history_manager.clear(remember_history_points)

        if puzzle is None:
            puzzle = Puzzle(self.board,polygons=[],name="",pieces_area=0)
        else:
            puzzle = Puzzle(self.board,polygons=list(puzzle.polygons),
                    name=puzzle.name,pieces_area=puzzle.pieces_area)
        
        return scanned_points,puzzle