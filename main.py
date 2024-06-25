import argparse
import os
from src.seed_points import sampler
from src.seed_points.board import Board
from src.puzzle_creators.all_partition import AllPartitionsCreator
import matplotlib.pyplot as plt


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sampling_src_file",default="")
    parser.add_argument("--sampling_img_path",default="")
    parser.add_argument("--manual_sampling_out_dir")
    parser.add_argument("--number_sampled_points")
    parser.add_argument("--sampling_dst_folder",default="data/run from")
    parser.add_argument("--puzzles_dst_folder",default="data/puzzles/new_puzzles")
    parser.add_argument("--num_puzzles",default=10,type=int)
    args = parser.parse_args()


    if args.sampling_src_file != "":
        board = Board(file_path=args.sampling_src_file)
    elif args.sampling_img_path != "":
        num_sampled_points = int(args.number_sampled_points)
        interior_points,convex_hull_points,_ = sampler.sample_image(num_sampled_points,args.img_path)
        board = Board(interior_points=interior_points,convex_hull_points=convex_hull_points)
    else:
        interior_points,convex_hull_points, out_path = sampler.sampler_manual(output_dir=args.manual_sampling_out_dir)
        print("maunal sampling output file path is ",out_path)
        board = Board(interior_points=interior_points,convex_hull_points=convex_hull_points)

    try:
        dirs_to_create = [args.puzzles_dst_folder,os.path.join(args.puzzles_dst_folder,"results")]

        for _dir in dirs_to_create:
            if not os.path.exists(_dir):
                os.makedirs(_dir)

        creator = AllPartitionsCreator(board,args.puzzles_dst_folder)
        creator.run()
        
        plt.close("all")

    except Exception as err:
        raise err
    finally:
        plt.close("all")