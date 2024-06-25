from numpy.random import randint
import random
from src.data_structures.shapes import Polygon
from src.data_structures import Point
from shapely.geometry import Point as ShapelyPoint
from shapely.geometry import MultiPoint
import pandas as pd
from datetime import datetime
import os
from PIL import Image
from src.seed_points import manual_sampling_gui


def sample_int_(n_int_points,frame_polygon,epsilon = 5):
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

def sample_float_(n_points,x_min, y_min, x_max, y_max):
    points = []
    while n_points > 0:
        x = random.uniform(x_min,x_max)
        y = random.uniform(y_min,y_max)
        points.append(Point((x,y)))
        n_points = n_points - 1
    
    return points

def arange_df_(internal_points,frame_points):
    xs = []
    ys = []
    roles = []
    frame_anchor_points = frame_points # deprecated

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
    
    return df


def sort_hull_interior_(sampled_points:list):
    sampled_points_ = MultiPoint(sampled_points)                
    convex_hull = sampled_points_.convex_hull

    # For just the debugging of the refactoring use the custom point rather than shapely point
    interior_points = [Point(point.x,point.y) for point in sampled_points_ if not convex_hull.touches(point)]
    # convex_hull_points = MultiPoint(list(Polygon(sampled_points_.convex_hull).exterior.coords)[:-1])
    
    # xs, ys = sampled_points_.convex_hull.exterior.xy
    convex_hull_points = [Point(p[0],p[1]) for p in list(Polygon(sampled_points_.convex_hull).exterior.coords)[:-1]]

    return interior_points,convex_hull_points


def sample_AABB(num_points, x_max, y_max,x_min=0, y_min=0,output_dir=None):
    sampled_points = sample_float_(num_points,x_min, y_min, x_max, y_max)
    interior_points,convex_hull_points = sort_hull_interior_(sampled_points)

    if not output_dir is None:
        df = arange_df_(interior_points,convex_hull_points)
        current_time = datetime.now().strftime("%H-%M-%S")
        file_name = f"CH-{len(convex_hull_points)}-INT-{len(interior_points)}-{current_time}.csv"
        out_path = os.path.join(output_dir,file_name)
        df.to_csv(out_path,index=False)
    else:
        out_path = None

    return interior_points,convex_hull_points,out_path

def sample_image(num_points,img_path,output_dir=None):
    img = Image.open(img_path)
    width,height = img.size

    frame_tuples = [(0,0),(0,height),(width,height),(width,0)] # because ofir asked these dimensions
    frame_polygon = Polygon(frame_tuples)
    x_min, y_min, x_max, y_max = frame_polygon.bounds

    sampled_points = sample_float_(num_points,x_min, y_min, x_max, y_max)
    interior_points,convex_hull_points = sort_hull_interior_(sampled_points)

    if not output_dir is None:
        df = arange_df_(interior_points,convex_hull_points)
        current_time = datetime.now().strftime("%H-%M-%S")
        img_name = os.path.basename(img_path)
        file_name = f"{img_name}-CH-{len(convex_hull_points)}-INT-{len(interior_points)}-{current_time}.csv"
        out_path = os.path.join(output_dir,file_name)
        df.to_csv(out_path,index=False)
    else:
        out_path = None

    return interior_points,convex_hull_points,out_path
    
def sampler_manual(canvas_width=4000, canvas_height=4000,output_dir=None):
    sampled_points = manual_sampling_gui.create_click_tracker(canvas_width=canvas_width,canvas_height=canvas_height)

    interior_points,convex_hull_points = sort_hull_interior_(sampled_points)

    if not output_dir is None:
        df = arange_df_(interior_points,convex_hull_points)
        current_time = datetime.now().strftime("%H-%M-%S")
        file_name = f"CH-{len(convex_hull_points)}-INT-{len(interior_points)}-{current_time}.csv"
        out_path = os.path.join(output_dir,file_name)

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        df.to_csv(out_path,index=False)
    else:
        out_path = None

    return interior_points,convex_hull_points,out_path