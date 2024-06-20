import argparse
from PIL import Image
import os
from src.seed_points import sampler
from src.data_structures.shapes import Polygon
from src.data_structures import Point
from shapely.geometry import MultiPoint
from datetime import datetime
from src.puzzle_creators.single_scanner.puzzle_obj import Board
from src.puzzle_creators.single_scanner.creator import Creator
import matplotlib.pyplot as plt
import pandas as pd
import shutil


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--img_path",default="")
    parser.add_argument("--number_sampled_points")
    parser.add_argument("--sampling_dst_folder",default="data/run from")
    parser.add_argument("--sampling_src_file",default="")
    parser.add_argument("--puzzles_dst_folder",default="data/puzzles/new_puzzles")
    parser.add_argument("--num_puzzles",default=10,type=int)

    args = parser.parse_args()

    if args.sampling_src_file == "":
        img = Image.open(args.img_path)
        width,height = img.size

        frame_tuples = [(0,0),(0,height),(width,height),(width,0)] # because ofir asked these dimensions
        frame_polygon_points = [Point(p) for p in frame_tuples]
        frame_polygon = Polygon(frame_tuples)
        x_min, y_min, x_max, y_max = frame_polygon.bounds

    
        number_sampled_points = int(args.number_sampled_points)
    
    
        
    try:
        for puzzle_i in range(args.num_puzzles):

            if args.sampling_src_file == "":
                sampled_points = MultiPoint(sampler.sample_float(number_sampled_points,x_min, y_min, x_max, y_max))                
                convex_hull = sampled_points.convex_hull
                interior_points = [point for point in sampled_points if not convex_hull.touches(point)]
                convex_hull_points = MultiPoint(list(Polygon(sampled_points.convex_hull).exterior.coords)[:-1])
                
                
                current_time = datetime.now().strftime("%H-%M-%S")
                img_name = args.img_path.split("/")[-1].split(".")[0]
                file_name = f"{img_name}-CH-{len(convex_hull_points)}-INT-{len(interior_points)}-{current_time}.csv"
                dst_file = args.sampling_dst_folder + "/"+file_name

                sampler.write_sampling(dst_file,interior_points,
                                    convex_hull_points,convex_hull_points)#,
                                                        #is_write=args.dst_folder != "")
            else:
                dst_file = args.sampling_src_file
            
            
            board = Board()
            board.load_sampled_points(dst_file)

            puzzles_dst_folder = args.puzzles_dst_folder
            
            if args.img_path != "":
                puzzles_dst_folder = puzzles_dst_folder+"/"+img_name

            creator = Creator(board,puzzles_dst_folder)
            dirs_to_create = [puzzles_dst_folder,puzzles_dst_folder+"/results"]

            for _dir in dirs_to_create:
                if not os.path.exists(_dir):
                    os.makedirs(_dir)

            creator.sample_puzzle_space(num_puzzles=1)

            print(f"Iteration {puzzle_i}/{args.num_puzzles}", )
            if args.sampling_src_file=="":
                os.remove(dst_file)

            plt.close("all")
    except Exception as err:
        raise err
    finally:
        plt.close("all")


