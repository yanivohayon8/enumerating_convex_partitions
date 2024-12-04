from shapely.geometry import Polygon as ShapelyPolygon
from functools import reduce
from shapely.geometry import Point

class Polygon(ShapelyPolygon):
    def __str__(self) -> str:
        xs,ys = self.exterior.coords.xy
        verticies = [(x,y) for x,y in zip(xs,ys)]
        return reduce(lambda acc,vert_str: acc + vert_str+";",\
                list(map(lambda x: str(x),verticies)),"")
    
    def __repr__(self) -> str:
        return str(self)

    def __hash__(self) -> int:
        xs,ys = self.exterior.coords.xy
        # return hash(tuple(reduce(lambda acc,x:acc+x,[[x,y] for x,y in zip(xs,ys)])))
        return hash(tuple(reduce(lambda acc,x:acc+x,[f"{x},{y}" for x,y in zip(xs,ys)])))


def get_diameter(polygon):
    # Get all coordinates on the boundary
    boundary_coords = list(polygon.exterior.coords)
    max_distance = 0

    # Compare all pairs of points
    for i in range(len(boundary_coords)):
        for j in range(i + 1, len(boundary_coords)):
            p1 = boundary_coords[i]
            p2 = boundary_coords[j]
            distance = Point(p1).distance(Point(p2))
            max_distance = max(max_distance, distance)

    return max_distance
