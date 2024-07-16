import pandas as pd
from src.data_structures.shapes import Polygon
from src.data_structures import Point,poly_as_matplotlib,plot_polygons
from src.consts import PLOT_COLORS
from math import pi,atan2
import numpy as np


class Puzzle():
    
    def __init__(self,board,polygons=[],name="",pieces_area=0) -> None:
        self.polygons = polygons
        self.pieces_area = pieces_area
        self.board = board
        self.name = name
    
    def __repr__(self) -> str:
        return self.name 

    def load_polygons(self,df_puzzle_csv:pd.DataFrame):
        self.pieces_area = 0
        self.polygons = []
        pieces_ids = df_puzzle_csv["id"].unique().tolist()
        for piece_id in pieces_ids:
            verts_rows = df_puzzle_csv.loc[df_puzzle_csv["id"]==piece_id, ["x","y"]]
            polygon = Polygon(verts_rows.values.tolist())
            self.pieces_area += polygon.area
            self.polygons.append(polygon)

    def plot_naive(self,ax,pieces=None,is_annotate=True,**kwargs):
        self.board.plot(ax)
        if pieces is None:
            pieces = self.polygons
        puzzle_mat_polygons = [poly_as_matplotlib(piece,color=PLOT_COLORS[i%len(PLOT_COLORS)],**kwargs) for i,piece in enumerate(pieces)]
        plot_polygons(ax,puzzle_mat_polygons)
        if is_annotate:
            for i,mat_poly in enumerate(pieces):
                ax.text(mat_poly.centroid.x,mat_poly.centroid.y,str(i+1),style='italic',
                        bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})
    
    def plot(self,ax,snapshot_queue,**kwargs):
        self.board.plot(ax)
        decompose_name = self.name.split("_")[:-1]
        # decompose_name.reverse()
        puzzle_mat_polygons = []
        color_index = 0
        piece_index = 0
        snapshot_head_index = 0
        for iter in decompose_name:
            if iter == "n":
                continue
            if iter == "p":
                snapshot_head_index= snapshot_head_index + 1
                continue
            if iter == "s":
                choice_index = 0
            else:
                choice_index = eval(iter.split("-")[0]) - 1 # -1 because of naming in creator

            pieces = snapshot_queue[snapshot_head_index].options[choice_index].val
            for piece in pieces:
                puzzle_mat_polygons.append(poly_as_matplotlib(piece, 
                    color=PLOT_COLORS[color_index%len(PLOT_COLORS)],**kwargs))
                # ax.text(piece.centroid.x,piece.centroid.y,iter,style='italic', bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})
                # piece_index+=1
                color_index+=1
            # color_index+=1
            snapshot_head_index=snapshot_head_index + 1

        plot_polygons(ax,puzzle_mat_polygons)

    def _count_piece(self,poly):
        # if isinstance(choice.val,Piece):
        self.polygons.append(poly)
        self.pieces_area += poly.area

    def record_choice(self,choice_name):
        self.name = self.name + choice_name + "_"
        
    def check_sanity_polygon(self,curr_polygon:Polygon):
        if not curr_polygon.is_simple:
            raise PuzzleErr(f"Polygon must be simple. coords: {str(curr_polygon)}")
        
        coords = curr_polygon.exterior.coords

        if len(coords) < 4:
            raise PuzzleErr(f"Polygon minimun amount of vertecies is 3. coords: {str(curr_polygon)}")

        if coords[0] != coords[-1]:
            raise PuzzleErr(f"Polygon must end and open with the same vertex. coords: {str(curr_polygon)}")

        if not all(coords[1:-1].count(c)==1 for c in coords[1:-1]):
            raise  PuzzleErr(f"Polygon coords cannot have duplicates. coords: {str(curr_polygon)}")

        for piece in self.polygons:
            if not(curr_polygon.disjoint(piece) or curr_polygon.touches(piece)):
                raise PuzzleErr(f"piece {str(piece)} intersects with new piece {str(curr_polygon)}")
            if curr_polygon.equals(piece):
                raise PuzzleErr(f"Tried to create equal piece to exist one. piece: {str(curr_polygon)}.")


        for inter_point in self.board.interior_points:
            if inter_point.within(curr_polygon):
                raise PuzzleErr(f"Piece {str(curr_polygon)} created contains interior point {str(inter_point)}")

    def write_results(self,output_path,is_peleg_format=True):
        xs = []
        ys = []
        piece_id = []
        for index in range(len(self.polygons)):
            for coord in self.polygons[index].exterior.coords[:-1]:
                xs.append(coord[0])
                ys.append(coord[1])
                piece_id.append(index)
        
        df = pd.DataFrame({"piece":piece_id,"x":xs,"y":ys})

        if is_peleg_format:
            df.columns = ["piece","x","y"]

        df.to_csv(output_path,index=False)

    def _is_edges_angles_convex(self,center_point):
        '''Get pieces containing center point'''
        center_point_coords = list(center_point.coords)[0]
        pieces_contain_point = [list(polygon.exterior.coords) for polygon in self.polygons \
                                if center_point_coords in list(polygon.exterior.coords)]

        '''Get neighbor points - sharing an edge with center_point'''
        neighbors = set()
        for piece_coords in pieces_contain_point:
            index = piece_coords.index(center_point_coords)
            left_neighbor_index = index-1
            right_neighbot_index = index+1
            # if it is the origin of the piece it will apear twice in the coordinates
            # The polygon has at least 3 different verticies
            if index == 0: #or index==len(piece_coords) - 1:
                left_neighbor_index = -2
                right_neighbot_index = 1
            
            neighbors.add(Point(piece_coords[left_neighbor_index]))
            neighbors.add(Point(piece_coords[right_neighbot_index]))

        if len(neighbors) < 2:
            return False

        def calc_angle(neigh_point):
            delta_y = neigh_point.y - center_point.y
            delta_x = neigh_point.x - center_point.x
            res = atan2(delta_y,delta_x)
            if res < 0:
                res+=2*pi
            return np.degrees(res)
        

        neighbors = list(neighbors)
        angles = list(map(calc_angle,neighbors))
        angles.sort()
        neighbors_sorted = [point for _,point in sorted(zip(angles,neighbors))]
        prev_angle = calc_angle(neighbors_sorted[0])
        prev_point = neighbors_sorted[0]

        for angle,point in zip(angles[1:] + [angles[0]+360],neighbors_sorted[1:] + [neighbors_sorted[0]]):
            diff = angle - prev_angle
            if diff > 180:
                # self.logger.debug(f"Around the center point {str(center_point)} \
                #             the points {str(prev_point)} and {str(point)} angle is {angle}-{prev_point}={diff}>180")
                return False
            prev_angle = angle
            prev_point = point
        
        return True
    

    def is_filled(self):
        return round(self.pieces_area,5) >= round(self.board.frame_polygon.area,5)

    def is_completed(self):
        if not self.is_filled():
            raise PuzzleAreaErr(f"Sum of piece's area {self.pieces_area} is less than its convex hull area {self.board.frame_polygon.area}")
        
        for point in self.board.interior_points:
            if not self._is_edges_angles_convex(point): #self.is_angles_convex[str(point)]:
                raise PuzzleEdgeAnglesErr("The angle of the polygon are not convex even though the whole puzzle framework is covered")
                
        return True

class PuzzleErr(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class PuzzleEdgeAnglesErr(Exception):
    pass

class PuzzleAreaErr(Exception):
    pass