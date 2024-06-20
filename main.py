import argparse
import os
from src.seed_points import sampler
from src.seed_points.board import Board
from src.puzzle_creators.utils.creator import Creator
from src.puzzle_creators.all_partition import AllPartitionsCreator
import matplotlib.pyplot as plt


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--img_path",default="")
    parser.add_argument("--number_sampled_points")
    parser.add_argument("--sampling_dst_folder",default="data/run from")
    parser.add_argument("--sampling_src_file",default="")
    parser.add_argument("--puzzles_dst_folder",default="data/puzzles/new_puzzles")
    parser.add_argument("--num_puzzles",default=10,type=int)
    args = parser.parse_args()

    num_sampled_points = int(args.number_sampled_points)

    try:
        for puzzle_i in range(args.num_puzzles):

            if args.sampling_src_file == "":
                interior_points,convex_hull_points,_ = sampler.sample_image(num_sampled_points,args.img_path)
                board = Board(interior_points=interior_points,convex_hull_points=convex_hull_points)
            else:
                board = Board(file_path=args.sampling_src_file)
            
            puzzles_dst_folder = args.puzzles_dst_folder
            
            # if args.img_path != "":
            #     puzzles_dst_folder = puzzles_dst_folder+"/"+img_name

            # creator = Creator(board,puzzles_dst_folder)
            dirs_to_create = [puzzles_dst_folder,os.path.join(puzzles_dst_folder,"results")]

            for _dir in dirs_to_create:
                if not os.path.exists(_dir):
                    os.makedirs(_dir)

            creator = AllPartitionsCreator(board,puzzles_dst_folder)
            creator.run()

            print(f"Iteration {puzzle_i}/{args.num_puzzles}", )

            plt.close("all")
    except Exception as err:
        raise err
    finally:
        plt.close("all")


