# from turtle import color, right
# from numpy import poly
from xml.dom import ValidationErr
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
        self.is_angles_convex = {}
    
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
        
    def plot_puzzle(self,fig,ax):
        scatter_points(ax,self.interior_points,color="blue")
        scatter_points(ax,self.frame_anchor_points,color="red")        
        frame_polygon = Polygon(self.frame_points)
        frame_mat_polygon = poly_as_matplotlib(frame_polygon,edgecolor="black",facecolor='white',lw=2)
        puzzle_mat_polygons = [poly_as_matplotlib(piece,color=PLOT_COLORS[i%len(PLOT_COLORS)]) for i,piece in enumerate(self.pieces)]
        puzzle_mat_polygons.insert(0, frame_mat_polygon)
        plot_polygons(ax,puzzle_mat_polygons)

    def _get_points_ahead(self,kernel_point,direction=1):
        logger.info("Start _get_points_ahead function. Filter point in space to get reachable points")
        logger.debug("Filter point that are not ahead the scanning direction")
        # on default - ahead to the left
        filter_condition = lambda item: item.x>=kernel_point.x and item!=kernel_point  
        space = list(self.interior_points+self.frame_anchor_points)
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
    
    def create(self):
        logger.info("Starts create function")
        scan_direction = Direction.left
        self._set_direction_scan(scan_direction.value)

        for point in self.interior_points:
            self.is_angles_convex[str(point)] = False

        n_iter = 0
        while True:
            logger.info(f"Start to scan board to from {str(scan_direction.name)}")
            for kernel_point in self.interior_points:
                n_iter +=1

                try:
                    logger.info(f"n_iter: {str(n_iter)}. Next interior point potential to origin a polygon is {str(kernel_point)}")
                    self.is_angles_convex[str(kernel_point)] = self._is_edges_angles_convex(kernel_point)
                    # observe surface data
                    points_to_connect = self._get_points_ahead(kernel_point,direction=scan_direction.value)            
                    points_to_connect = self._get_accessible_points(kernel_point,points_to_connect,direction=scan_direction.value)            

                    if len(points_to_connect) < 2:
                        logger.debug(f"Not enough points to connect ({len(points_to_connect)} < 2)")
                        # self.is_angles_convex[str(kernel_point)] = self._is_edges_angles_convex(kernel_point)
                        continue
                    
                    stared_polygon = Rgon1988.get_stared_shape_polygon(kernel_point,points_to_connect)
                    visual_graph_polygon = Rgon1988.get_visualization_graph(kernel_point,stared_polygon)
                    fig,ax = plt.subplots()
                    self.plot_puzzle(fig,ax)
                
                    [Edge(kernel_point,p).plot(ax,color='black', linestyle='dotted') for p in list(visual_graph_polygon.get_verticies())]
                    visual_graph_polygon.plot_directed(ax) # way to plot the graph
                    fig.savefig(debug_dir + f"/visibility-graph-before-filter/{str(n_iter)}.png")
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

                            # if line.covered_by(piece):
                            #     logger.debug(f"Edge {str(edge)} is covered by piece {str(piece)} ,so remove it from visibility graph")
                            #     visual_graph_polygon.remove_edge(edge)
                            #     break

                    fig,ax = plt.subplots()
                    self.plot_puzzle(fig,ax)
                    [Edge(kernel_point,p).plot(ax,color='black', linestyle='dotted') for p in list(visual_graph_polygon.get_verticies())]
                    visual_graph_polygon.plot_directed(ax) # way to plot the graph
                    fig.savefig(debug_dir + f"/visibility-graph-filtered/{str(n_iter)}.png")
                    plt.close()

                    if len(list(visual_graph_polygon.get_edges())) == 0:
                        logger.debug(f"Not enough edge to iterate on the visibility graph")
                        # self.is_angles_convex[str(kernel_point)] = self._is_edges_angles_convex(kernel_point)
                        continue

                    continuity_edges = Rgon1988.get_convex_chain_connectivity(visual_graph_polygon)
                    edges_max_chain_length = Rgon1988.get_edges_max_chain_length_new(kernel_point,visual_graph_polygon,continuity_edges)

                    num_edges = self._get_next_polygon_num_verticies(continuity_edges,edges_max_chain_length)
                    polygon = self._create_rgon(kernel_point,num_edges,edges_max_chain_length,continuity_edges)        

                    if polygon is not None:
                        logger.debug(f"Next Polygon to create is : {str(polygon)}")
                        self.check_sanity_polygon(polygon)
                        self.pieces.append(polygon)
                    
                    self.is_angles_convex[str(kernel_point)] = self._is_edges_angles_convex(kernel_point)

                # except ValueError as err:
                #     logger.warning(f"Failed to create polygon from point {str(kernel_point)}. The scan direction is from {scan_direction.name}")     
                #     logger.exception(err)
                except Exception as err:
                    logger.exception(err)
                    raise err 
                
                fig,ax = plt.subplots()
                self.plot_puzzle(fig,ax)
                fig.savefig(debug_dir + f"/results/{str(n_iter)}.png")
                plt.close()

            if self._is_finished_scan() and \
                all(self.is_angles_convex[str(point)] for point in self.interior_points):
                break

            scan_direction = Direction(scan_direction.value * (-1))
            Rgon1988.direction = scan_direction
            self._set_direction_scan(scan_direction.value)
        
        logger.info("Finish to create pieces")
    

    def _is_edges_angles_convex(self,center_point):
        '''Get pieces containing center point'''
        center_point_coords = list(center_point.coords)[0]
        pieces_contain_point = [list(piece.exterior.coords) for piece in self.pieces \
                                if center_point_coords in list(piece.exterior.coords)]

        '''Get neighbor points - sharing an edge with center_point'''
        neighbors = []
        for piece_coords in pieces_contain_point:
            index = piece_coords.index(center_point_coords)
            left_neighbor_index = index-1
            right_neighbot_index = index+1
            # if it is the origin of the piece it will apear twice in the coordinates
            # The polygon has at least 3 different verticies
            if index == 0: #or index==len(piece_coords) - 1:
                left_neighbor_index = -2
                right_neighbot_index = 1
            
            neighbors.append(Point(piece_coords[left_neighbor_index]))
            neighbors.append(Point(piece_coords[right_neighbot_index]))

        if len(neighbors) < 2:
            return False

        angles = [Rgon1988.calc_angle_around_point(center_point,point) for point in neighbors]
        angles = list(map(lambda ang: ang if ang>=0 else 360+ang,angles))
        angles.sort()
        is_angles_convex = all(ang2-ang1>180 for ang1, ang2 in zip(angles, angles[1:] + [angles[0]]))
                        
        return is_angles_convex


    def check_sanity_polygon(self,curr_piece:Polygon):
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

        for inter_point in self.interior_points:
            if inter_point.within(curr_piece):
                raise ValidationErr(f"Piece {str(piece)} created contains interior point {str(inter_point)}")

    def _is_finished_scan(self):
        raise NotImplementedError("need to be implemented")
        
    def _create_rgon(self,kernel_point,r,edges_max_chain_length,continuity_edges):
        raise NotImplementedError("need to be implemented")

    def _get_next_polygon_num_verticies(self,continuity_edges,edges_max_chain_length):
        raise NotImplementedError("need to be implemented")
    