from functools import reduce
import imp
from turtle import pu
from src.puzzle_creators.utils.surface import find_possible_rgons,get_stared_shaped_polygon,get_accessible_points
from src.puzzle_creators.utils.record import HistoryManager,Snapshot,Choice
from src.puzzle_creators.utils.puzzle_obj import Puzzle,PuzzleAreaErr,PuzzleEdgeAnglesErr
from src.data_structures import Point
from src.data_structures.shapes import Polygon
import matplotlib.pyplot as plt
from datetime import datetime
from random import randint,random


class SubsetPartitionCreator():

    def __init__(self,board,output_dir,is_plg_format=True) -> None:
        self.board = board
        self.output_dir = output_dir
        self.snapshot_queue = []
        self.history_manager = HistoryManager()
        self.fig, self.ax = plt.subplots()
        self.is_plg_format = is_plg_format

    def find_combinations_limited(self,kernel_point,possible_polygons,num_iteration_possible_polys=1):
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
        

        '''
            In order to prevent the puzzles piece to be narrow and long
        '''
        def get_aspect_ratio(poly):
            # minx, miny, maxx, maxy = poly.bounds
            # return -(maxy-miny)/(maxx-minx+1e-4)
            return -poly.area
            # return poly.area
        for key_ in polygons_start_at_point.keys():
            polygons_start_at_point[key_] = sorted(polygons_start_at_point[key_],key=get_aspect_ratio)
            polygons_start_at_point[key_] = polygons_start_at_point[key_][len(polygons_start_at_point[key_])//2:]
        #     polygons_start_at_point[key_] = [poly for poly in polygons_start_at_point[key_] if poly.area > 400]




        possibilities = []
        num_iter = 0
        for poly in polygons_start_at_point[str(start_point)]:
            
            # if num_iter == num_iteration_possible_polys:
            #     break
            
            num_iter+=1

            comb = [poly]
            poly_end_point = poly.exterior.coords[1]
            poss_start_with_poly = self.combs_rec_limited(poly_end_point,end_point,polygons_start_at_point,comb)
            # acc = []
            # self.combs_rec(poly_end_point,end_point,polygons_start_at_point,comb,acc)

            # possibilities.append(poss_start_with_poly)
            possibilities = possibilities + poss_start_with_poly
            # possibilities = possibilities + acc

        return possibilities

    def combs_rec_limited(self,start_point,end_point,polygons_start_at_point,comb):
        if start_point == end_point:
            return [comb]
        
        poss = []
        # for next_poly in polygons_start_at_point[str(start_point)]:
        next_poly = polygons_start_at_point[str(start_point)][0]
        comb_copy = comb[:]
        comb_copy.append(next_poly)
        next_end_point = next_poly.exterior.coords[1]
        next_combs = self.combs_rec_limited(next_end_point,end_point,
                                    polygons_start_at_point,comb_copy)
        
        # for _ in next_combs:
        #     poss.append(_)
        poss = poss + next_combs
        # poss.append(next_combs)
        
        return poss

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

    def create_single_limited(self,puzzle:Puzzle,scanned_points)->Puzzle:
        
        for kernel_point in scanned_points:
            try:
                potential_points = self.board.potential_points(kernel_point,self.board.space_points)
                points_to_connect = get_accessible_points(kernel_point,puzzle.polygons,potential_points)
                possible_polygons = find_possible_rgons(kernel_point,puzzle,points_to_connect)

                # possible_polygons = [poly for poly in possible_polygons if poly.area > 50]

                if len(possible_polygons) == 0:
                    puzzle.record_choice("n")
                    continue

                possible_polygons_combs = self.find_combinations_limited(kernel_point,possible_polygons)
                total_poss = possible_polygons_combs
                n = len(total_poss)
                options = [Choice(c,f"{index+1}-{n}",is_single=n==1) for index,c in enumerate(total_poss)]
                
                if not self.history_manager.is_recorded(repr(kernel_point)):
                    copy_polygons = [Polygon(poly.exterior.coords) for poly in puzzle.polygons]
                    snapshot = Snapshot(kernel_point,
                                        Puzzle(self.board,copy_polygons,puzzle.name,puzzle.pieces_area),
                                        options)
                    self.snapshot_queue.append(snapshot)

                next_choice_index = self.history_manager.next_availiable(repr(kernel_point))
                curr_choice = options[next_choice_index]
                
                if isinstance(curr_choice.val,list):
                    for poly in curr_choice.val:
                        puzzle.check_sanity_polygon(poly)                
                        puzzle._count_piece(poly)

                puzzle.record_choice(curr_choice.name)

                if puzzle.is_filled():
                    return puzzle

            except Exception as err:
                raise err

        return puzzle

    def run(self,probability_skip_snapshot=0,num_puzzles=1,kernel_possiblities_iterations=2):        
        scanned_points,puzzle = self.initialize(self.board.space_points[0])
        curr_puzzle_i = 0 # if num_puzzles is -1 than compute all the permutations

        while True and curr_puzzle_i < num_puzzles:
            curr_puzzle_i+=1
            puzzle = self.create_single_limited(puzzle,scanned_points)

            try:
                puzzle.is_completed()
                # dst_path = self.output_dir+f"/{str(puzzle.name)}.csv"
                my_time = datetime.now().strftime("%d-%m-%Y")
                rnd_int = randint(1,99999999)
                # dst_path = self.output_dir+f"/{my_time}_numPieces_{len(puzzle.polygons)}_rand_{rnd_int}.csv"

                file_name = f"numPieces_{len(puzzle.polygons)}_rand_{rnd_int}"
                dst_path = self.output_dir+f"/{file_name}.csv"
                puzzle.write_results(dst_path,is_plg_format=self.is_plg_format)
                self.ax.cla()
                puzzle.plot(self.ax,self.snapshot_queue)
                self.fig.savefig(self.output_dir+f"/results/{file_name}.png")
               
            except (PuzzleAreaErr,PuzzleEdgeAnglesErr) as e:
                # self.ax.cla()
                # puzzle.plot(self.ax,self.snapshot_queue)
                # self.fig.savefig(self.output_dir+f"/failure/{str(puzzle.name)}.png")
                # print("Plotted failure on failure directory")
                # raise e
                curr_puzzle_i-=1
                continue
            
            while len(self.snapshot_queue) > 0:
                last_snap = self.snapshot_queue[-1]

                if probability_skip_snapshot > 0:
                    coin = random()

                    if probability_skip_snapshot < coin:
                        if not last_snap.is_tried_all_paths(self.history_manager.head_availiable(repr(last_snap))):
                            break

                self.snapshot_queue.pop()

            if len(self.snapshot_queue) == 0:
                break

            scanned_points,puzzle = self.initialize(last_snap.kernel_point,last_snap.puzzle)