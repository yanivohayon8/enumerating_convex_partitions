from functools import reduce
import imp
from src.puzzle_creators.single_scanner.surface import find_possible_rgons,get_stared_shaped_polygon,get_accessible_points
from src.puzzle_creators.single_scanner.record import HistoryManager,Snapshot,Choice
from src.puzzle_creators.single_scanner.puzzle_obj import Puzzle,PuzzleAreaErr,PuzzleEdgeAnglesErr
from src.data_structures import Point
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

    def find_combinations(self,kernel_point,possible_polygons):
        connected_points = set()
        for pol in possible_polygons:
            coords = pol.exterior.coords
            for cor in coords:
                p = Point(cor)
                if p!=kernel_point:
                    connected_points.add(Point(cor))

        connected_points = list(connected_points)
        # connected_points = list(reduce(lambda acc,lst: acc+lst.exterior.coords,possible_polygons,[]))
        # connected_points = [Point(cor) for cor in connected_points]
        stared_polygon_coords = get_stared_shaped_polygon(kernel_point,connected_points).exterior.coords
        start_point,end_point = stared_polygon_coords[-2],stared_polygon_coords[1]

        polygons_start_at_point = {}
        for polygon in possible_polygons:
            coords = [Point(cor) for cor in polygon.exterior.coords[1:-1]]
            poly = get_stared_shaped_polygon(Point(polygon.exterior.coords[0]),coords)
            first_point_str = str(poly.exterior.coords[-2])

            if first_point_str not in polygons_start_at_point.keys():
                polygons_start_at_point[str(first_point_str)] = []
            
            polygons_start_at_point[str(first_point_str)].append(poly)
        
        possibilities = []
        for poly in polygons_start_at_point[str(start_point)]:
            comb = [poly]
            poly_end_point = poly.exterior.coords[1]
            poss_start_with_poly = self.combs_rec(poly_end_point,end_point,polygons_start_at_point,comb)
            possibilities.append(poss_start_with_poly)

        return possibilities

    def combs_rec(self,start_point,end_point,polygons_start_at_point,comb):
        if start_point == end_point:
            return comb
        poss = []
        for next_poly in polygons_start_at_point[str(start_point)]:
            next_end_point = next_poly.exterior.coords[1]
            next_comb = self.combs_rec(next_end_point,end_point,polygons_start_at_point,comb + [next_poly])
            poss = poss + next_comb
        
        return poss


    def create_single(self,scanned_points)->Puzzle:
        
        puzzle = Puzzle(self.board)

        for kernel_point in scanned_points:
            try:
                potential_points = self.board.potential_points(kernel_point,self.board.space_points)
                points_to_connect = get_accessible_points(kernel_point,puzzle.polygons,potential_points)
                possible_polygons = find_possible_rgons(kernel_point,puzzle,points_to_connect)
                possible_polygons_combs = self.find_combinations(kernel_point,possible_polygons)
                total_poss = possible_polygons_combs + ["pass"]
                n = len(total_poss)
                options = [Choice(c,f"{index+1}-{n-1}",is_single=n-1==1) for index,c in enumerate(total_poss)]
                
                if len(options) == 1:
                    puzzle.record_choice("n")
                    continue

                snapshot = Snapshot(kernel_point,puzzle,options)
                if not self.history_manager.is_recorded(snapshot):
                    self.snapshot_queue.append(snapshot)

                next_choice_index = self.history_manager.next_availiable(repr(snapshot))
                curr_choice = options[next_choice_index]
                
                if isinstance(curr_choice.val,list):
                    for poly in curr_choice.val:
                        puzzle.check_sanity_polygon(poly)                
                        puzzle._count_piece(poly)

                puzzle.record_choice(curr_choice.name)

            except ValueError as err:
                raise err

        return puzzle


    def create_puzzles(self):
        
        start_point_index = 0
        scanned_points = self.board.space_points[start_point_index:]
        last_point_x = max([p.x for p in scanned_points])
        scanned_points = list(filter(lambda p: p.x < last_point_x,scanned_points))

        while True:

            puzzle = self.create_single(scanned_points)

            try:
                # puzzle.is_completed(self.board.frame_polygon)
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
                break
