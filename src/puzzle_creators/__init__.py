from turtle import color, right
from numpy import poly
import pandas as pd
from src.data_structures import Point,Polygon,Graph,Edge
import matplotlib.pyplot as plt

from enum import Enum
from src.hypothesis import rgon_1988 as Rgon1988
from src.consts import PLOT_COLORS
from src.algorithms.sweep_line.sweep_line import SweepLine
import logging
from src import setup_logger


class Direction(Enum):
    left = 1
    right = -1

log_handler = setup_logger.get_file_handler(setup_logger.get_debug_log_file())
logger = logging.getLogger("logger.puzzle_creator")
logger.addHandler(log_handler)
debug_dir = setup_logger.get_debug_lastrun_dir()

class PuzzleCreator():

    def __init__(self):
        self.interior_points = []
        self.frame_anchor_points = [] #frame anchor points
        self.frame_points = []
        self.connections_graph = Graph()
        self.pieces = []
    
    def load_sampled_points(self,file_path):
        role_points = {
            "interior":self.interior_points,
            "frame_anchor":self.frame_anchor_points,
            "frame":self.frame_points
        }
        df = pd.read_csv(file_path,index_col=False)

        for row in df.to_numpy():
            point = Point(row[0],row[1])
            role_points[row[2]].append(point)
        
    def plot_scratch(self,ax):
        '''
            Plot the frame_anchor, frame, interior lines prior to the puzzle creation
        '''
        Point.scatter_points(ax,self.interior_points,color="blue")
        Point.scatter_points(ax,self.frame_anchor_points,color="red")        

        frame_polygon = Polygon(self.frame_points)
        mat_polygon = frame_polygon.get_as_matplotlib(edgecolor=[0,0,0],facecolor=[1,1,1],lw=2,fill=False)
        Polygon.plot_polygons(ax,[mat_polygon])

    def plot_puzzle(self,fig,ax):
        Point.scatter_points(ax,self.interior_points,color="blue")
        Point.scatter_points(ax,self.frame_anchor_points,color="red")        
        frame_polygon = Polygon(self.frame_points)
        frame_mat_polygon = frame_polygon.get_as_matplotlib(edgecolor="black",facecolor='white',lw=2)
        puzzle_mat_polygons = [piece.get_as_matplotlib(color=PLOT_COLORS[i%len(PLOT_COLORS)]) for i,piece in enumerate(self.pieces)]
        puzzle_mat_polygons.insert(0, frame_mat_polygon)
        Polygon.plot_polygons(ax,puzzle_mat_polygons)

    def _get_accessible_points(self,kernel_point,direction=1):
        # on default - ahead to the left
        filter_condition = lambda item: item.x>=kernel_point.x and item!=kernel_point  
        space = list(self.interior_points+self.frame_anchor_points)

        # if requested ahead to right
        if direction == -1:
            filter_condition = lambda item: item.x<=kernel_point.x and item!=kernel_point    
            space.reverse()

        space = list(filter(filter_condition,space)) 
        '''Sweep Line algorithm here'''
        # TODO
        sweepline = SweepLine()
        conn_graph = self.connections_graph.get_copy()
        [conn_graph.insert_edge(Edge(kernel_point,point)) for point in space] 
        edges = list(conn_graph.edges)
        sweepline.preprocess(edges)
        intersections = []
        try:
            df_results = sweepline.run_algo(is_debug=True)
            intersections = list(filter(lambda item: not(item[0] == kernel_point.x and item[1] == kernel_point.y),\
                                df_results.values.tolist()))
        except Exception as err:
            ax = plt.subplot()
            ax.title.set_text(f"Debug sweep line at {str(kernel_point)}")
            conn_graph.plot_directed(ax) # way to plot the graph
            plt.savefig(debug_dir + "/Last sweep Line graph.png")
            # logger.exception(err)
            raise err
    
        for inter_point in intersections:
            seg_index = int(inter_point[2])
            point_to_remove = edges[seg_index].dst_point
            if point_to_remove == kernel_point:
                point_to_remove = edges[seg_index].src_point
            
            space = list(filter(lambda p: p != point_to_remove,space))

        return space


    def _preprocess(self,direction):
        self.interior_points = sorted(self.interior_points,key=lambda p: p.x,reverse=direction<0)
        self.frame_anchor_points = sorted(self.frame_anchor_points,key=lambda p: p.x,reverse=direction<0)

    def _get_surface(self,kernel_point,direction):
        points_to_connect = self._get_accessible_points(kernel_point,direction=direction)            
        stared_polygon = Rgon1988.get_stared_shape_polygon(kernel_point,points_to_connect)
        visual_graph_polygon = Rgon1988.get_visualization_graph(kernel_point,stared_polygon)
        # ax = plt.subplot()
        # visual_graph_polygon.plot_directed(ax) # way to plot the graph
        # plt.show()
        continuity_edges = Rgon1988.get_convex_chain_connectivity(visual_graph_polygon)
        edges_max_chain_length = Rgon1988.get_edges_max_chain_length_new(kernel_point,visual_graph_polygon,continuity_edges)
        return continuity_edges,edges_max_chain_length
    
    
    def create(self):
        logger.info("Starts create function")
        for point in self.interior_points + self.frame_anchor_points:
            self.connections_graph.insert_vertex(point)

        scan_direction = Direction.left
        self._preprocess(scan_direction.value)
        while True:
            for interior_point in self.interior_points:
                continuity_edges,edges_max_chain_length = self._get_surface(interior_point,direction=scan_direction.value)
                num_edges = self._get_next_polygon_num_edges(continuity_edges,edges_max_chain_length)
                polygon = self._create_rgon(interior_point,num_edges,edges_max_chain_length,continuity_edges)        

                if polygon is not None:
                    logger.debug(f"Next Polygon to create is : {str(polygon)}")
                    # update maps
                    polygon_grph = polygon.get_graph()
                    self.connections_graph.union(polygon_grph)
                    fig,ax = plt.subplots()
                    ax.title.set_text("Debug Connectivity Graph")
                    self.connections_graph.plot_directed(ax) # way to plot the graph
                    fig.savefig(debug_dir + "/Last Connectivity Graph.png")
                    self.pieces.append(polygon)
            
            scan_direction = Direction(scan_direction.value * (-1))
            self._preprocess(scan_direction.value)

            if self._is_finished_scan:
                break
    
    def _is_finished_scan(self):
        raise NotImplementedError("need to be implemented")
        
    def _create_rgon(self,kernel_point,r,edges_max_chain_length,continuity_edges):
        raise NotImplementedError("need to be implemented")

    def _get_next_polygon_num_edges(self,continuity_edges,edges_max_chain_length):
        raise NotImplementedError("need to be implemented")
