# enumerating_convex_partitions
Imagine sampling N points in the Euclidean plane and computing their convex hull. A convex partition is a planar graph that includes the edges of this convex hull, ensuring that every face of the graph is convex and contains no sampled point in its interior. This project aims to generate the complete set of convex partitions for a given set of sampled points. The primary motivation is to create 2D jigsaw puzzles, so the output graph is described by its faces, which correspond to the individual puzzle pieces.

<p align="center">
    <figure>
    <img src="https://github.com/user-attachments/assets/f22671ef-0f61-4406-8f91-1b53c3ec57cc" alt="partitionSet">
    <figcaption>Fig.1. Enumerating all the convex partitions for a given input of 6 sampled points, where five sit on their convex hull (colored in red) while one is in its interior (colored in blue).</figcaption>
    </figure>
</p>

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)

## Installation 

Install the required packages
```sh
pip install -r requirements.txt
```

## Usage
You can run the script in several different modes, where every mode differently provides the inputted sampled points. Although, all of the modes have the following common arguments:

|Parameter  |Type|Default|Required|description|
|-----------|----|-------|--------|-----------|
|`--dst-folder`|string|None|Yes|The parent directory to store the output.|
|`--num-partitions-collections`|int|1|No|The number of sampling sets to create. For each, the entire set of partitions is computed.|
|`--disable-saving-partitions-figures`|boolean|True|No|If specified, the images visualizing every partition are not created.|
|`--postfix-dst-partitions-folder`|string|`""`|No|Adds a postfix string at the end of a directory name for the entire partitions of a sampled points set.|


### Generate from handcraft sampling
In this mode, a GUI is launched for the user to sample manually the points. `--manual-sampling-out-dir` specifies the directory path where to save the file describing the sampling. Since, it is an optional argument, if it is not specified, this file is not saved.

<p align="center">
    <img src="https://github.com/user-attachments/assets/0acfd4f8-b535-48fc-bc8a-32662ba8217c" alt="sampling seed set">
</p>

#### Quick Start
```shell
main.py --dst-folder "data/quick start/handcraft" --manual-sampling-out-dir "data/quick start/handcraft" 
```

### Generate from sampled points on a circle
The following are the mode special arguments:

|Parameter  |Type|Default|Required|description|
|-----------|----|-------|--------|-----------|
|`--sampling-circle-num-ch`|int|None|Yes| The number of points to sample on the circle, constituing the points on the convex hull of the sampled points.|
|`--sampling-circle-num-interior`|int|0|No| The number points to sample within the circle, constituing the points within the convex hull of the sampled points.|
|`--sampling-circle-radius`|float|5000|No| The radius of the circle.|

#### Quick Start
```shell
main.py --dst-folder "data/quick start/circle" --sampling-circle-num-ch 4  --sampling-circle-num-interior 2 --sampling-circle-radius 3000
```

### Generate from sampled points on an image
This mode samples the points in a uniform distribution along a its X and Y axes indepedently, within a bounding box that a given image width and height defines. As oppose to the `circle mode`, the division to interior or convex hull points is not deterministic. The following are the mode special arguments:
|Parameter  |Type|Default|Required|description|
|-----------|----|-------|--------|-----------|
|`--sampling-img-path`|string|None|Yes|The path to the inputted image.|
|`--sampling-img-num-points`|int|None|Yes| The number of points to sample.|

#### Quick Start
```shell
main.py --dst-folder "data/quick start/image" --sampling-img-path "data/quick start/unsplash.jpg" --sampling-img-num-points 6
```

### Generate from a inputted file
Using this mode, you need to specify only the argument `--sampling-src-file`, which indicates the path of the inputted file of the sampled points. 

#### Quick Start
```shell
main.py --dst-folder "data/quick start/src-file" --sampling-src-file "data/quick start/CH-6-INT-0.csv" 
```
