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
import os
import cv2
import copy
import numpy as np
import open3d as o3d
from scipy.spatial.transform import Rotation as R
from pcd_processing import PointCloudProcessing
import open3d.visualization.gui as gui
import open3d.visualization.rendering as rendering



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
    # print('Number of detected objects = ' + str(num_of_objects) + '     ')
    
    # Draw table plane + frame + objects
    entities_to_draw = np.concatenate((entities_to_draw, p.objects_to_draw))

    # o3d.visualization.draw_geometries(entities_to_draw,
    #                                         zoom = view['trajectory'][0]['zoom'],
    #                                         front = view['trajectory'][0]['front'],
    #                                         lookat = view['trajectory'][0]['lookat'],
    #                                         up = view['trajectory'][0]['up'])

    # o3d.visualization.draw_geometries(p.objects_to_draw,
    #                                         zoom = view['trajectory'][0]['zoom'],
    #                                         front = view['trajectory'][0]['front'],
    #                                         lookat = view['trajectory'][0]['lookat'],
    #                                         up = view['trajectory'][0]['up'])
   

    # Visualization throuh Application 
    app = gui.Application.instance
    app.initialize()

    w = app.create_window("Detected Objects", 1020, 800)
    widget3d = gui.SceneWidget()
    widget3d.scene = rendering.Open3DScene(w.renderer)
    widget3d.scene.set_background([1,1,1,1])
    material = rendering.MaterialRecord()
    material.shader = "defaultUnlit"
    material.point_size = 2 * w.scaling

    

    for entity_idx, entity in enumerate(p.objects_to_draw):
        widget3d.scene.add_geometry("Entity" + str(entity_idx),entity, material)
        for obj in p.objects_properties:
            l = widget3d.add_3d_label(obj['center']+(-0.1,0,((obj['height']/2)+0.05)), 'Object: ' + str(obj['idx']))
            l2 = widget3d.add_3d_label(obj['center']+(-0.1,0,((obj['height']/2)+0.08)), 'Aprox. Volume: ' + str(round(obj['x_width']*1000,0)) + 
                                       ' x ' + str(round(obj['y_width']*1000,0)) + ' x ' + str(round(obj['height']*1000,0)) + 'mm' )

            # l.color = gui.Color(p.objects_to_draw.colors[idx][0], p.objects_to_draw.colors[idx][1],
            #                     p.objects_to_draw.colors[idx][2])
            # l.scale = np.random.uniform(0.5, 3.0)
    bbox = widget3d.scene.bounding_box
    widget3d.setup_camera(60.0, bbox, bbox.get_center())
    w.add_child(widget3d)
    app.run()



    
    # --------------------------------------
    # Classification of objects in the scene
    # --------------------------------------
    print('\n')

    # Intrinsic Matrix
    intrinsic_matrix = np.matrix([[570.3,      0, 0, 320],
                                  [    0,  570.3, 0, 240],
                                  [    0,      0, 1,   0],
                                  [    0,      0, 0,   1]], copy=False,  dtype=np.float64)
    print('Camera Intrinsic Matrix: ' + str(intrinsic_matrix) + '\n')

    # 0.92118 0.00982951 -0.355027 -0.15905 1.96118 -0.200736 0.341896
    # Convert quaternion to rotation matrix
    r = R.from_quat([0.92118, 0.00982951, -0.355027, -0.15905])
    rotation = r.as_matrix()
    print('Rotation: ' + str(rotation) + '\n')

    translation = np.array([1.96118, -0.200736, 0.341896], dtype = np.float64)
    print('Translation: ' + str(translation) + '\n')

    # Print Ccnter position of each object
    center = np.asmatrix(np.zeros((4,1)))
    for obj in p.objects_properties:
        print('object center: ' + str(obj['center']) + ' - ' + str(type(obj['center'])) + '\n')

        # Conversão para matriz e homegenização
        center[0:3,0] = np.asmatrix(obj['center']).T
        center[3,0]= 1
        print(str(center) + '\n')

    # Show Scene image
    img = cv2.imread("docs/rgbd-scenes-v2_imgs/00404-color.png")

    rvec = cv2.Rodrigues(rotation)
    print('rvec: ' + str(rvec) + ' - ' + str(type(rvec)) + '\n')
    distCoeffs = np.array([0, 0, 0, 0], dtype=np.float64)

    # imagePoints,_ = cv2.projectPoints(np.array(center), rvec[0], translation, intrinsic_matrix, distCoeffs)
    # print('Image Points: ' + str(imagePoints) + '\n')

    coords = np.array([[4.27874, 115.15968, 18.1621], [27.52924, 113.3441, 17.70207]])
    cop = np.array([-14.45194, 34.59882, 19.11343])
    points_2d = cv2.projectPoints(np.array(coords), (0,0,0), (0,0,0), intrinsic_matrix, distCoeffs)

    cv2.imshow("Display window", img)

    k = cv2.waitKey(0)

    if k == ord("s"):
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
