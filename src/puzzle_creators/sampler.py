from numpy.random import randint
from src.data_structures import Point
import pandas as pd

# class Sampler():
#     pass

# class InternalSampler():

#     def __init__(self,frame_anchor_points,frame_points) -> None:
#         self.frame_anchor_points = frame_anchor_points
#         self.frame_points = frame_points

def sample_internal(n_int_points,frame_polygon,epsilon = 5):
    x_min, y_min, x_max, y_max = frame_polygon.bounds
    points = []
    while n_int_points > 0:
        sampled_point = Point(
                randint(x_min + epsilon,x_max - epsilon),
                randint(y_min + epsilon,y_max - epsilon))
        if frame_polygon.contains(sampled_point):
            points.append(sampled_point)
            n_int_points = n_int_points - 1
    
    return points

def write_sampling(output_file,internal_points,frame_points,frame_anchor_points):
    xs = []
    ys = []
    roles = []
    for p in internal_points:
        xs.append(p.x)
        ys.append(p.y)
        roles.append("interior")

    for p in frame_anchor_points:
        xs.append(p.x)
        ys.append(p.y)
        roles.append("frame_anchor")
    
    for p in frame_points:
        xs.append(p.x)
        ys.append(p.y)
        roles.append("frame")
    
    df = pd.DataFrame(data={
        "x": xs,
        "y":ys,
        "role":roles
    })

    df.to_csv(output_file,index=False)


