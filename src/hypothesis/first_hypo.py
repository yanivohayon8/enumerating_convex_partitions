from ..hypothesis import HypothesisAlgo
from ..hypothesis import rgon_1988  as Rgon1988
# from . import data_structures 
from src.data_structures.graph import Graph,Edge
import functools

'''THIS IS DEPRECATED MODULE'''

class FirstHypo(HypothesisAlgo):
    """
        This class implements my first idea.
        Scanning from left to right and then the opposite.
        Each scan random polygon from each point...
    """
    def __init__(self,interior_points,border_points):
        super().__init__(interior_points,border_points)
        self.polygons = []
        self.graph = Graph()
        self.space_points = interior_points + border_points


    def get_accessible_points(self,kernel_point,subspace_points):
        # you will need to filter here the subspace points 
        # according the view of the current point: 
        # it could be blocked by edges (and by direction)
        return subspace_points    

    def scan_space(self,interior_points,direction="left"):
        
        polygons = []
        for point in self.space_points:
            self.graph.insert_vertex(point)

        for kernel_point in interior_points:
            # calculate the angle between each edge
            vertex_connected = [e.src_point for e in self.graph.get_input_edges(kernel_point)] + \
                               [e.dst_point for e in self.graph.get_output_edges(kernel_point)]

            if len(vertex_connected) > 1:
                angles = [Rgon1988.calc_angle_around_point(kernel_point,point) for point in vertex_connected]
                angles.sort()
                is_angles_convex = functools.reduce(lambda a,b: b-a < 180, angles + angles[0])
            
                if is_angles_convex:
                    continue
            
            points_ahead = Rgon1988.get_points_horizontal_ahead(kernel_point,self.space_points,direction)
            
            # Get the accessable points 
            ''' TODO'''
            accesible_points = self.get_accessible_points(kernel_point,points_ahead)

            # compute the rgon
            stared_polygon = Rgon1988.get_stared_shape_polygon(kernel_point,accesible_points)
            visual_graph_polygon = Rgon1988.get_visualization_graph(kernel_point,stared_polygon)
            continuity_edges = Rgon1988.get_convex_chain_connectivity(visual_graph_polygon)
            edges_max_chain_length = Rgon1988.get_edges_max_chain_length(visual_graph_polygon,continuity_edges)
            rgon = Rgon1988.create_rgon(kernel_point,3,edges_max_chain_length,continuity_edges)
            polygons.append(rgon)

            print("Polygon kernel: " + str(kernel_point)),
            # update the relationships map
            for vert_index in range(len(rgon.vertcies)):
                print(str(rgon.vertcies[vert_index]) + "-"),
                src_point = rgon.vertcies[vert_index]
                dst_point = rgon.vertcies[(vert_index + 1)%len(rgon.vertcies)]
                self.graph.insert_edge(Edge(src_point,dst_point))

            print()
        return polygons





    def run_algo(self):
        # sort the point asc by x
        self.interior_points.sort(key=lambda p: p.x)
        polygons = self.scan_space(self.interior_points,direction="left")
        #graph,polygons = self.scan_space(self.interior_points.reverse(),direction="right")

        return polygons
