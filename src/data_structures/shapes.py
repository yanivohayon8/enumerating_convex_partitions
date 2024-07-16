from shapely.geometry import Polygon as ShapelyPolygon
from functools import reduce

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

