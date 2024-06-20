from src.seed_points import sampler
from src.data_structures.shapes import Polygon
from src.data_structures import Point
from shapely.geometry import MultiPoint
from random import randint

def sample_points(width,height,n_points):
    frame_tuples = [(0,0),(0,height),(width,height),(width,0)]
    frame_polygon_points = [Point(p) for p in frame_tuples]
    frame_polygon = Polygon(frame_tuples)
    x_min, y_min, x_max, y_max = frame_polygon.bounds

    
    sampled_points = MultiPoint(sampler.sample_float(n_points,x_min, y_min, x_max, y_max))                
    # convex_hull = 
    convex_hull = sampled_points.convex_hull
    interior_points = [point for point in sampled_points if not convex_hull.touches(point)]
    convex_hull_points = MultiPoint(list(Polygon(sampled_points.convex_hull).exterior.coords)[:-1])
    rnd_int = randint(1,10000)
    sample_name = f"convex_hull-{len(convex_hull_points)}-int-{len(interior_points)}-{rnd_int}"
    return sample_name, interior_points, convex_hull_points
    # file_name = f"{output_dir}\\{sample_name}.csv"
    # sampler.write_sampling(file_name,interior_points,convex_hull_points,convex_hull_points)
