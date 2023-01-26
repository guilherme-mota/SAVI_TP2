#!/usr/bin/env python3

# -------------------------------------------------------------------------------
# Name:        main
# Purpose:     AI system to detect and track objects
# Authors:     Guilherme Mota | Miguel Cruz | Luís Ascenção
# Created:     29/12/2022
# -------------------------------------------------------------------------------

# ------------------------------------
# Imports
# ------------------------------------
import numpy as np
import open3d as o3d
from pcd_processing import PointCloudProcessing
import copy
import os

# ------------------------------------
# View
# ------------------------------------
view = {
	"class_name" : "ViewTrajectory",
	"interval" : 29,
	"is_loop" : False,
	"trajectory" : 
	[
		{
			"boundingbox_max" : [ 2.4968247576504106, 2.2836352945191325, 0.87840679827947743 ],
			"boundingbox_min" : [ -2.5744585151435198, -2.1581489860671899, -0.60582068710203252 ],
			"field_of_view" : 60.0,
			"front" : [ 0.64259021703866903, 0.52569095376874997, 0.55742877041995087 ],
			"lookat" : [ 0.35993510810021934, 0.20028892156868539, 0.25558948566773715 ],
			"up" : [ -0.41838167468135773, -0.36874521998147031, 0.8300504424621673 ],
			"zoom" : 0.14000000000000001
		}
	],
	"version_major" : 1,
	"version_minor" : 0
}

def main():


    # ------------------------------------
    # Initialization 
    # ------------------------------------

    print('Starting Scene 3D Processing...\n')
    
    # Load PCD
    p = PointCloudProcessing()
    # /home/miguel/Documents/SAVI_TP2/docs/rgbd-scenes-v2_pc/rgbd-scenes-v2/pc/01.ply
    p.loadpcd('docs/rgbd-scenes-v2_pc/rgbd-scenes-v2/pc/05.pcd')   
    

    
    # ------------------------------------
    # Execution 
    # ------------------------------------

    # Pre Processing with Voxel downsampling to increase process velocity
    p.downsample()

    # Calculation of the reference transformation parameters for the center of the table - In this case only for TRANS
    tx, ty, tz = p.frameadjustment()        
  
    # Frame Transform CAM to TABLE
    p.frametransform(0, 0, 0, tx, ty, tz)
    p.frametransform(-108, 0, 0, 0, 0, 0)
    p.frametransform(0, 0, -37, 0, 0, 0)
    
    # Isolation of interest part (table + objects)
    p.croppcd(-0.6, -0.6, -0.02, 0.6, 0.6, 0.4)

    # Plane segmentation ---> Table detection and objects isolation
    p.planesegmentation()
    
    # Object Clustering
    p.pcdclustering()

    # Object isolation and caracterization


    
    # ------------------------------------
    # Visualization
    # ------------------------------------

    #Draw BBox
    entities_to_draw = []
    bbox = o3d.geometry.LineSet.create_from_axis_aligned_bounding_box(p.bbox)
    entities_to_draw.append(bbox)
    
    # Draw Table Plane
    p.inliers.paint_uniform_color([0.9,0.9,1])
    correct_center = p.inliers.get_center()
    #print('correct center: ' + str(correct_center))
    entities_to_draw.append(p.inliers) # Draw only de plane (ouliers are the objects)
    
    # Create coordinate system
    frame = o3d.geometry.TriangleMesh().create_coordinate_frame(size=0.2, origin=np.array([0, 0, 0]))
    entities_to_draw.append(frame)
   

    # Draw objects 
    num_of_objects = len(p.objects_to_draw)
    print('Number of detected objects = ' + str(num_of_objects) + '     ')
    
    # Draw table plane + frame + objects
    entities_to_draw = np.concatenate((entities_to_draw, p.objects_to_draw))

    o3d.visualization.draw_geometries(entities_to_draw,
                                            zoom = view['trajectory'][0]['zoom'],
                                            front = view['trajectory'][0]['front'],
                                            lookat = view['trajectory'][0]['lookat'],
                                            up = view['trajectory'][0]['up'])

    o3d.visualization.draw_geometries(p.objects_to_draw,
                                            zoom = view['trajectory'][0]['zoom'],
                                            front = view['trajectory'][0]['front'],
                                            lookat = view['trajectory'][0]['lookat'],
                                            up = view['trajectory'][0]['up'])    




if __name__ == "__main__":
    main()
