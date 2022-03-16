from turtle import color, right
import pandas as pd
from src.data_structures import Point,Polygon,Graph
import matplotlib.pyplot as plt
from enum import Enum
from src.hypothesis import rgon_1988 as Rgon1988
from src.consts import PLOT_COLORS

class Direction(Enum):
    left = 1
    right = -1


class PuzzleCreator():
    def __init__(self):
        self.interior_points = []
        self.border_points = []
        self.frame_points = []
        # self.connections_graph = Graph()
        self.pieces = []
    
    def load_sampled_points(self,file_path):
        role_points = {
            "interior":self.interior_points,
            "border":self.border_points,
            "frame":self.frame_points
        }
        df = pd.read_csv(file_path,index_col=False)

        for row in df.to_numpy():
            point = Point(row[0],row[1])
            role_points[row[2]].append(point)
        
    def plot_scratch(self,ax):
        '''
            Plot the border, frame, interior lines prior to the puzzle creation
        '''
        Point.scatter_points(ax,self.interior_points,color="blue")
        Point.scatter_points(ax,self.border_points,color="red")        

        frame_polygon = Polygon(self.frame_points)
        mat_polygon = frame_polygon.get_as_matplotlib(edgecolor=[0,0,0],facecolor=[1,1,1],lw=2,fill=False)
        Polygon.plot_polygons(ax,[mat_polygon])

    def plot_puzzle(self,fig,ax):
        Point.scatter_points(ax,self.interior_points,color="blue")
        Point.scatter_points(ax,self.border_points,color="red")        
        frame_polygon = Polygon(self.frame_points)
        frame_mat_polygon = frame_polygon.get_as_matplotlib(edgecolor="black",facecolor='white',lw=2)
        puzzle_mat_polygons = [piece.get_as_matplotlib(color=PLOT_COLORS[i%len(PLOT_COLORS)]) for i,piece in enumerate(self.pieces)]
        puzzle_mat_polygons.insert(0, frame_mat_polygon)
        Polygon.plot_polygons(ax,puzzle_mat_polygons)

    def _get_accessible_points(self,point,direction=1):
        # on default - ahead to the left
        filter_condition = lambda item: item.x>=point.x and item!=point  
        space = list(self.interior_points+self.border_points)

        # if requested ahead to right
        if direction == -1:
            filter_condition = lambda item: item.x<=point.x and item!=point    
            space.reverse()

        '''Sweep Line algorithm here'''
        # TODO
        
        return list(filter(filter_condition,space))


    def _preprocess(self):
        pass
        # for point in self.interior_points + self.border_points:
            # self.connections_graph.insert_vertex(point)
    
    
    def _scan(self,direction=1):
        for inter_point in self.interior_points:
            points_to_connect = self._get_accessible_points(inter_point,direction=direction)
            
            stared_polygon = Rgon1988.get_stared_shape_polygon(inter_point,points_to_connect)
            visual_graph_polygon = Rgon1988.get_visualization_graph(inter_point,stared_polygon)
            continuity_edges = Rgon1988.get_convex_chain_connectivity(visual_graph_polygon)
            edges_max_chain_length = Rgon1988.get_edges_max_chain_length(visual_graph_polygon,continuity_edges)

            num_edges = self._get_next_polygon_num_edges()
            polygon = self._create_rgon(inter_point,num_edges,edges_max_chain_length,continuity_edges)

            self.pieces.append(polygon)

    
    
    def create(self):
        self._preprocess()
        scan_direction = Direction.left
        while True:
            self._scan(direction=scan_direction)
            scan_direction = Direction(scan_direction.value * (-1))
            if self._is_finished_scan:
                break
    
    def _is_finished_scan(self):
        raise NotImplementedError("need to be implemented")
        
    def _create_rgon(self,kernel_point,r,edges_max_chain_length,continuity_edges):
        raise NotImplementedError("need to be implemented")

    def _get_next_polygon_num_edges(self):
        raise NotImplementedError("need to be implemented")
