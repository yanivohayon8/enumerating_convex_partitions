# from turtle import color, right
# from numpy import poly
from xml.dom import ValidationErr
from matplotlib.style import available
import pandas as pd
from src.data_structures.graph import Edge
from src.data_structures import Point,scatter_points,poly_as_matplotlib,plot_polygons
from src.data_structures.shapes import Polygon #,MultiPoint
from shapely.geometry import LineString
# from src.data_structures.graph import  Graph,Edge
import matplotlib.pyplot as plt

from src.puzzle_creators import rgon_1988_wrap as Rgon1988
from src.consts import PLOT_COLORS
# from src.algorithms.sweep_line.sweep_line import SweepLine
import logging
from src import setup_logger
from functools import reduce

from src.data_structures.shapes import Polygon
from src.puzzle_creators import Direction

from math import pi,atan2
import numpy as np


log_handler = setup_logger.get_file_handler(setup_logger.get_debug_log_file())
logger = logging.getLogger("logger.puzzle_creator")
logger.addHandler(log_handler)
debug_dir = setup_logger.get_debug_lastrun_dir()

class PuzzleCreator():

    def __init__(self):
        self.interior_points = []
        self.frame_anchor_points = [] #frame anchor points
        self.frame_points = []
        self.pieces = [] #MultiPolygon
        # self.is_angles_convex = {}
        self.pieces_area = 0
        self.frame_polygon = None
        self.last_possible_rgons ={}
        self.n_iter = 0
    
    def load_sampled_points(self,file_path):
        role_points = {
            "interior": self.interior_points,
            "frame_anchor":self.frame_anchor_points,
            "frame":self.frame_points
        }
        df = pd.read_csv(file_path,index_col=False)

        for row in df.to_numpy():
            point = Point(row[0],row[1])
            role_points[row[2]].append(point)

        self.frame_polygon = Polygon(self.frame_points)
        
        # maybe this should not be here
        self.scan_direction = Direction.left
        self._set_direction_scan(self.scan_direction.value)

        # for point in self.interior_points:
        #     self.is_angles_convex[str(point)] = False
        
    def plot_puzzle(self,fig,ax,pieces=None,**kwargs):
        if pieces is None:
            pieces = self.pieces
        scatter_points(ax,self.interior_points,color="blue")
        scatter_points(ax,self.frame_anchor_points,color="red")        
        frame_mat_polygon = poly_as_matplotlib(self.frame_polygon,edgecolor="black",facecolor='white',lw=2)
        puzzle_mat_polygons = [poly_as_matplotlib(piece,color=PLOT_COLORS[i%len(PLOT_COLORS)],**kwargs) for i,piece in enumerate(pieces)]
        puzzle_mat_polygons.insert(0, frame_mat_polygon)
        plot_polygons(ax,puzzle_mat_polygons)
        for i,mat_poly in enumerate(pieces):
            ax.text(mat_poly.centroid.x,mat_poly.centroid.y,str(i+1),style='italic',
                    bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})

    def _get_points_ahead(self,kernel_point,direction=1):
        logger.info("Start _get_points_ahead function. Filter point in space to get reachable points")
        logger.debug("Filter point that are not ahead the scanning direction")
        # on default - ahead to the left
        filter_condition = lambda item: item.x>=kernel_point.x and item!=kernel_point  
        space = self.space_points.copy() #list(self.interior_points+self.frame_anchor_points)
        space.remove(kernel_point)

        # if requested ahead to right
        if direction == -1:
            filter_condition = lambda item: item.x<=kernel_point.x and item!=kernel_point    
            space.reverse()

        space = list(filter(filter_condition,space)) 
        space_str = reduce(lambda acc,x: acc + x + ";" ,["",""] + list(map(lambda x: str(x),space)))
        logger.debug(f"Points ahead are {str(space_str)}")
        return space

    def _get_accessible_points(self,kernel_point,space,direction=1):
        logger.info("Start _get_accessible_points method")
        # fig,ax = plt.subplots()
        # ax.title.set_text(f"Debug accesible point")
        # self.plot_puzzle(fig,ax)
        visible_points = []
        ker_to_p_lines = [LineString([kernel_point,point])for point in space]

        for point,curr_ker_to_p_line in zip(space,ker_to_p_lines):

            # If the kernel, current point and other point forms a line, 
            # the far distant point is not visible
            if any(curr_ker_to_p_line.contains(line) and not line.equals(curr_ker_to_p_line)\
                for line in ker_to_p_lines):
                continue
            
            # if other piece is blocking view to point
            if any((curr_ker_to_p_line.crosses(piece) and not curr_ker_to_p_line.touches(piece) or curr_ker_to_p_line.within(piece))\
                for piece in self.pieces):
                continue
            
            # If it does visible
            visible_points.append(point)
            x, y = curr_ker_to_p_line.xy
            # ax.plot(x, y,color="black")

        # fig.savefig(debug_dir + f"/Last debug accesible point.png")
        # plt.close()

        visible_points_str = reduce(lambda acc,x: acc + x + ";" ,["",""] + list(map(lambda x: str(x),visible_points)))
        logger.debug(f"{str(len(visible_points))} points are visible: {str(visible_points_str)}")
        return visible_points

    def _set_direction_scan(self,direction):
        self.interior_points = sorted(self.interior_points,key=lambda p: p.x,reverse=direction<0)
        self.frame_anchor_points = sorted(self.frame_anchor_points,key=lambda p: p.x,reverse=direction<0)
        self.space_points = sorted(self.interior_points + self.frame_anchor_points,key=lambda p: p.x,reverse=direction<0)
    
    
    def create(self):
        logger.info("Starts create function")
        self.n_iter = 0
        Rgon1988.direction = self.scan_direction


        while True:
            logger.info(f"Start to scan board to from {str(self.scan_direction.name)}")
            for kernel_point in self.space_points:
                self.last_kernel_point = kernel_point # for the power group creator
                self.n_iter +=1

                try:
                    possible_rgons = self.prepare_to_create(kernel_point)
                    polygon = self._create_rgon(possible_rgons)
                    self.after_rgon_creation(polygon)
                   
                except Exception as err:
                    logger.exception(err)
                    raise err 
            
            
            if self._is_finished_scan():
                break

            self.scan_direction = Direction(self.scan_direction.value * (-1))
            # Rgon1988.direction = self.scan_direction
            self._set_direction_scan(self.scan_direction.value)
        
        # logger.info("Finish to assemble a puzzle")
    
    

    def plot_results(self,fig_path):
        fig,ax = plt.subplots()
        self.plot_puzzle(fig,ax)
        fig.savefig(fig_path)
        plt.close()    

    def _count_piece(self,polygon):
        self.pieces.append(polygon)
        self.pieces_area += polygon.area
    
    def prepare_to_create(self,kernel_point):
        raise NotImplementedError("need to be implemented")

    def after_rgon_creation(self,polygon):
        if polygon is not None:
            logger.debug(f"Next Polygon to create is : {str(polygon)}")
            self.check_sanity_polygon(polygon)
            self._count_piece(polygon)

    def _is_edges_angles_convex(self,center_point):
        # logger.debug(f"Find out wheter the angles between edges of point {str(center_point)} are all less than 180")
        '''Get pieces containing center point'''
        center_point_coords = list(center_point.coords)[0]
        pieces_contain_point = [list(piece.exterior.coords) for piece in self.pieces \
                                if center_point_coords in list(piece.exterior.coords)]

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
                logger.debug(f"Around the center point {str(center_point)} \
                            the points {str(prev_point)} and {str(point)} angle is {angle}-{prev_point}={diff}>180")
                return False
            prev_angle = angle
            prev_point = point
        
        return True

    def check_sanity_polygon(self,curr_piece:Polygon):
        if not curr_piece.is_simple:
            ValidationErr(f"Polygon must be simple. coords: {str(curr_piece)}")
        
        coords = curr_piece.exterior.coords

        if len(coords) < 4:
            raise ValidationErr(f"Polygon minimun amount of vertecies is 3. coords: {str(curr_piece)}")

        if coords[0] != coords[-1]:
            raise ValidationErr(f"Polygon must end and open with the same vertex. coords: {str(curr_piece)}")

        if not all(coords[1:-1].count(c)==1 for c in coords[1:-1]):
            raise  ValidationErr(f"Polygon coords cannot have duplicates. coords: {str(curr_piece)}")

        for piece in self.pieces:
            if not(curr_piece.disjoint(piece) or curr_piece.touches(piece)):
                raise ValidationErr(f"piece {str(piece)} intersects with new piece {str(curr_piece)}")
            if curr_piece.equals(piece):
                raise ValidationErr(f"Tried to create equal piece to exist one. piece: {str(curr_piece)}.")


        for inter_point in self.interior_points:
            if inter_point.within(curr_piece):
                raise ValidationErr(f"Piece {str(piece)} created contains interior point {str(inter_point)}")

    def _is_finished_scan(self):
        logger.info("Check whether to stop board scanning or not")
        logger.debug("Check the sum of the pieces area against the whole framework")
        if self.pieces_area<self.frame_polygon.area:
            logger.debug(f"The sum of the pieces is less than the whole framework: {self.pieces_area}<{self.frame_polygon.area}")
            return False
        
        logger.debug("Checking if all the interior points angles between their edges are less than 180")
        for point in self.interior_points:
            if not self._is_edges_angles_convex(point): #self.is_angles_convex[str(point)]:
                return False
        
        
        return True

    def _find_rgons_comb(self,kernel_point,continuity_edges):
        rgons_strings = set()

        for edge_str in list(continuity_edges.keys()):
            traverses = [list(dict.fromkeys(tr)) for tr in self._get_traverse(Edge(edge_str),continuity_edges)]
            # rgons.append(traverses)
            # find all sequential sub combinations:
            for trav in traverses:
                for index_start in range(len(trav)):
                    for index_end in range(index_start+1,len(trav)):
                        sub_trav = trav[index_start:index_end+1]
                        sub_trav.insert(0,str(kernel_point))
                        rgons_strings.add(";".join(sub_trav))
        

        rgons = []
        for rgon_str in list(rgons_strings):
            points = rgon_str.split(";")
            poly = Polygon([Point(eval(point_str)) for point_str in points])

            try:
                self.check_sanity_polygon(poly)
                rgons.append(poly)
            except ValidationErr as err:
                pass


        return rgons

    def _get_traverse(self,origin_edge,continuity_edges):
        if len(continuity_edges[str(origin_edge)]) == 0:
            return [[str(origin_edge.src_point),str(origin_edge.dst_point)]]

        travs = []
        available_edges = continuity_edges[str(origin_edge)]
        for next_edge in available_edges:
            cont_travs = self._get_traverse(next_edge,continuity_edges)

            if isinstance(cont_travs[0],list):
                flat_travs = [item for sublist in cont_travs for item in sublist]
                flat_travs.insert(0,str(origin_edge.dst_point))
                flat_travs.insert(0,str(origin_edge.src_point))

            travs.append(flat_travs)
        
        return travs


    def _create_rgon(self,possible_rgons):
        raise NotImplementedError("need to be implemented")
    
    def write_results(self,output_path):
        xs = []
        ys = []
        piece_id = []
        for index in range(len(self.pieces)):
            for coord in self.pieces[index].exterior.coords:
                xs.append(coord[0])
                ys.append(coord[1])
                piece_id.append(index)
        
        df = pd.DataFrame({"x":xs,"y":ys,"id":piece_id})
        df.to_csv(output_path)

    def _get_surface(self,kernel_point,scan_direction,n_iter=-1,fig_prefix=""):
        # observe surface data
        points_to_connect = self._get_points_ahead(kernel_point,direction=self.scan_direction.value)            
        points_to_connect = self._get_accessible_points(kernel_point,points_to_connect,direction=self.scan_direction.value)            

        if len(points_to_connect) < 2:
            logger.debug(f"Not enough points to connect ({len(points_to_connect)} < 2)")
            # self.is_angles_convex[str(kernel_point)] = self._is_edges_angles_convex(kernel_point)
            return {}
        
        stared_polygon = Rgon1988.get_stared_shape_polygon(kernel_point,points_to_connect)
        visual_graph_polygon = Rgon1988.get_visualization_graph(kernel_point,stared_polygon)
        fig,ax = plt.subplots()
        self.plot_puzzle(fig,ax)
    
        [Edge(kernel_point,p).plot(ax,color='black', linestyle='dotted') for p in list(visual_graph_polygon.get_verticies())]
        visual_graph_polygon.plot_directed(ax) # way to plot the graph
        fig.savefig(debug_dir + f"/visibility-graph-before-filter/{fig_prefix}{str(self.n_iter)}.png")
        plt.close()

        # Remove edges that are covered by polygons - do it more elegant less naive
        logger.info("Filter edges covered by exist pieces")
        vs_grph_edges = list(visual_graph_polygon.get_edges()).copy()
        lines =  [LineString([edge.src_point,edge.dst_point]) for edge in vs_grph_edges]

        for edge,line in zip(vs_grph_edges,lines):
            for piece in self.pieces:
                
                if line.crosses(piece) and not line.touches(piece):
                    logger.debug(f"Edge {str(edge)} is crossed by piece {str(piece)} ,so remove it from visibility graph")
                    visual_graph_polygon.remove_edge(edge)
                    break

                if line.within(piece):
                    logger.debug(f"Edge {str(edge)} is within piece {str(piece)} ,so remove it from visibility graph")
                    visual_graph_polygon.remove_edge(edge)
                    break

        fig,ax = plt.subplots()
        self.plot_puzzle(fig,ax)
        [Edge(kernel_point,p).plot(ax,color='black', linestyle='dotted') for p in list(visual_graph_polygon.get_verticies())]
        visual_graph_polygon.plot_directed(ax) # way to plot the graph
        fig.savefig(debug_dir + f"/visibility-graph-filtered/{fig_prefix}{str(self.n_iter)}.png")
        plt.close()

        if len(list(visual_graph_polygon.get_edges())) == 0:
            logger.debug(f"Not enough edge to iterate on the visibility graph")
            # self.is_angles_convex[str(kernel_point)] = self._is_edges_angles_convex(kernel_point)
            return {}

        return Rgon1988.get_convex_chain_connectivity(visual_graph_polygon)

    def _find_first_possible_rgons(self,kernel_point,n_iter=-1):
        continuity_edges = self._get_surface(kernel_point,self.scan_direction,n_iter)

        # num_edges = self._get_next_polygon_num_verticies(continuity_edges,edges_max_chain_length)
        possible_rgons = self._find_rgons_comb(kernel_point,continuity_edges)
        possible_rgons = list(filter(lambda pc:all(pc.disjoint(pc2) or pc.touches(pc2) for pc2 in self.pieces),possible_rgons))
        return possible_rgons

    def _filter_poss_rgons(self,last_possible_rgons):
        return list(filter(lambda pc:all(pc.disjoint(pc2) or pc.touches(pc2) for pc2 in self.pieces),last_possible_rgons))#