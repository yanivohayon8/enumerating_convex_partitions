import argparse
import os
from src.seed_points import sampler
from src.seed_points.board import Board
from src.puzzle_creators.all_partition import AllPartitionsCreator
import matplotlib.pyplot as plt
from datetime import datetime
import shutil


def create_puzzle(puzzles_dst_folder):
    dirs_to_create = [puzzles_dst_folder,os.path.join(puzzles_dst_folder,"results")]

    for _dir in dirs_to_create:
        if not os.path.exists(_dir):
            os.makedirs(_dir)

    if args.sampling_src_file != "":
        board = Board(file_path=args.sampling_src_file)
    elif args.sampling_img_path != "":
        num_sampled_points = int(args.number_sampled_points)
        interior_points,convex_hull_points,_ = sampler.sample_image(num_sampled_points,args.sampling_img_path,output_dir=puzzles_dst_folder)
        board = Board(interior_points=interior_points,convex_hull_points=convex_hull_points)
    elif not args.circle_num_ch is None:
        interior_points,convex_hull_points,_ = sampler.sample_points_on_circle(args.circle_num_ch,args.circle_num_interior,
                                                                               args.circle_radius,output_dir=puzzles_dst_folder)
        board = Board(interior_points=interior_points,convex_hull_points=convex_hull_points)
    else:
        interior_points,convex_hull_points, out_path = sampler.sampler_manual(output_dir=args.manual_sampling_out_dir)
        print("maunal sampling output file path is ",out_path)
        board = Board(interior_points=interior_points,convex_hull_points=convex_hull_points)

    try:
        creator = AllPartitionsCreator(board,puzzles_dst_folder,is_save_partitions_figures=args.save_partitions_figures)
        creator.run()
        
        plt.close("all")

    except Exception as err:
        raise err
    finally:
        plt.close("all")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dst-folder",dest="puzzles_dst_folder")
    parser.add_argument("--num-partitions-collections",dest="num_partitions_collections",default=1,type=int)
    parser.add_argument("--disable-saving-partitions-figures",dest="save_partitions_figures",action="store_false")
    parser.set_defaults(save_partitions_figures=True)
    parser.add_argument("--postfix-dst-partitions-folder",dest="postfix_dst_folder_uuid",default="")
    parser.add_argument("--sampling-src-file",dest="sampling_src_file",default="")
    parser.add_argument("--sampling-img-path",dest="sampling_img_path",default="")
    parser.add_argument("--sampling-img-num-points",dest="number_sampled_points")
    parser.add_argument("--manual-sampling-out-dir",dest="manual_sampling_out_dir")
    parser.add_argument("--sampling-circle-num-interior",default=0,dest="circle_num_interior",type=int)
    parser.add_argument("--sampling-circle-num-ch",dest="circle_num_ch",type=int)
    parser.add_argument("--sampling-circle-radius",default=5000,dest="circle_radius",type=float)
    args = parser.parse_args()

    for creation_i in range(args.num_partitions_collections):
        puzzles_dst_folder = args.puzzles_dst_folder
        current_dateTime = datetime.now()
        random_dir_name = str(current_dateTime).replace(".","+")
        random_dir_name = random_dir_name.replace(":","-")
        random_dir_name = random_dir_name + args.postfix_dst_folder_uuid
        puzzles_dst_folder = os.path.join(puzzles_dst_folder,random_dir_name)

        try:
            print(f"Start to create puzzles to {puzzles_dst_folder} ({creation_i+1}/{args.num_partitions_collections})")
            create_puzzle(puzzles_dst_folder)
        except Exception as e:
            print(f"Error:{e}")
            shutil.rmtree(puzzles_dst_folder,ignore_errors=True) # be carefull not to delete the entire dataset!