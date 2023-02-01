Trabalho Prático 2 - SAVI 2022-2023
==============

# Project Introduction

Project developed within the scope of the curricular unit, Advanced Industrial Vision Systems, at the University of Aveiro.

Consists of a program that processes information collected by 3D sensors and conventional cameras, in order to detect and classify objects.

For that it was used point cloud processing tools ([Open3D](http://www.open3d.org/)) and neural networks ([Pytorch](https://pytorch.org/)).


## Dataset

The data used in this project is from [Washington RGB-D Dataset](http://rgbd-dataset.cs.washington.edu/dataset/).

## Requirements
To run the program, the following packages must be installed:
* open3d
* pytorch
* numpy
* pyttsx3
* opencv-python
* colorama
* matplotlib
* tqdm
* glob

## Execution
When running the program from the terminal, use the following notation:
```
./main.py -s
```

After the -s, put the value of the scene you intend to analyze.
If you don't put anything, by default the program opens the scene 1, from the point cloud scene01.ply.

Example to open scene 10:
```
./main.py -s 10
```

## Contact
Guilherme Mota - <motaguilherme99@ua.pt>

Miguel Cruz - <miguelcruz51@ua.pt>

Luís Ascensão - <luispiresascensao@ua.pt>

## Acknowledgments
Professor Miguel Oliveira - <mriem@ua.pt>
