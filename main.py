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
from scenes_information import Scenes



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

def matrix_to_rtvec(matrix):

    "Convert 4x4 matrix to rotation vector and translation vector"
    (rvec, jac) = cv2.Rodrigues(matrix[:3, :3])
    tvec = matrix[:3, 3]

    return rvec, tvec

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

    # --------------------------------------------------------------------------
    # Transformação do referêncial da camara (Global) para o referêncial da Mesa
    # --------------------------------------------------------------------------
    trans = np.eye(4)
    trans[:3,3] = np.array([-tx, -ty, -tz]).transpose() # Converter para matrix
    trans = np.asmatrix(trans)
    # print('trans:\n' + str(trans) + '\n')

    rot1 = np.eye(4)
    r1 = R.from_euler('xyz', [108, 0, 0], degrees=True)
    rot1[:3, :3] = r1.as_matrix()
    # print('rot1:\n' + str(rot1) + '\n')

    rot2 = np.eye(4)
    r2 = R.from_euler('xyz', [0, 0, 37], degrees=True)
    rot2[:3, :3] = r2.as_matrix()
    # print('rot2:\n' + str(rot2) + '\n')

    T_cam_mesa = np.eye(4)
    T_cam_mesa = rot1 * rot2 * T_cam_mesa   # rotação de -108 em torno de x
    # T_cam_mesa = rot2 * T_cam_mesa   # rotação de -37 em torno de z
    T_cam_mesa = trans * T_cam_mesa  # translação tx, ty, tz
    # print('T_cam_mesa:\n' + str(T_cam_mesa) + '\n')

    # exit(0)
    # -----------------------------------------------
    
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
    # app = gui.Application.instance
    # app.initialize()

    # w = app.create_window("Detected Objects", 1020, 800)
    # widget3d = gui.SceneWidget()
    # widget3d.scene = rendering.Open3DScene(w.renderer)
    # widget3d.scene.set_background([1,1,1,1])
    # material = rendering.MaterialRecord()
    # material.shader = "defaultUnlit"
    # material.point_size = 2 * w.scaling

    

    # for entity_idx, entity in enumerate(p.objects_to_draw):
    #     widget3d.scene.add_geometry("Entity" + str(entity_idx),entity, material)
    #     for obj in p.objects_properties:
    #         l = widget3d.add_3d_label(obj['center']+(-0.1,0,((obj['height']/2)+0.05)), 'Object: ' + str(obj['idx']))
    #         l2 = widget3d.add_3d_label(obj['center']+(-0.1,0,((obj['height']/2)+0.08)), 'Aprox. Volume: ' + str(round(obj['x_width']*1000,0)) + 
    #                                    ' x ' + str(round(obj['y_width']*1000,0)) + ' x ' + str(round(obj['height']*1000,0)) + 'mm' )

    #         # l.color = gui.Color(p.objects_to_draw.colors[idx][0], p.objects_to_draw.colors[idx][1],
    #         #                     p.objects_to_draw.colors[idx][2])
    #         # l.scale = np.random.uniform(0.5, 3.0)
    # bbox = widget3d.scene.bounding_box
    # widget3d.setup_camera(60.0, bbox, bbox.get_center())
    # w.add_child(widget3d)
    # app.run()



    
    # ----------------------------------------------------------------------------
    # Classification of objects in the scene
    # ----------------------------------------------------------------------------
    print('\n')

    scene = Scenes(3)

    # Intrinsic Matrix
    intrinsic_matrix = np.float32([[570.3,      0, 320],
                                   [    0,  570.3, 240],
                                   [    0,      0,   1]])

    # Convert quaternion to rotation matrix
    r = R.from_quat(scene.information['rot'])
    rotation = r.as_matrix()
    # print('Rotation: ' + str(rotation) + '\n')

    translation = np.float32(scene.information['trans'])
    # print('Translation: ' + str(translation) + '\n')

    # Print Center position of each object
    objs_center = np.empty([len(p.objects_properties), 3], dtype=np.float32)
    for idx,obj in enumerate(p.objects_properties):
        objs_center[idx,:]= np.float32(obj['center'])
    print('Centros dos objectos detectados visto do referêncial da mesa:\n' + str(objs_center) + '\n')

    new_objs_center = np.empty([len(p.objects_properties), 3], dtype=np.float32)
    for idx,obj_center in enumerate(objs_center):
        t = np.empty([4, 1], dtype=np.float32)
        t[0,0] = obj_center[0]
        t[1,0] = obj_center[1]
        t[2,0] = obj_center[2]
        t[3,0] = 1
        t = np.asmatrix(t)

        New_center = T_cam_mesa * t
        New_center = np.asarray(New_center)
        new2 = New_center.transpose()

        new_objs_center[idx,:] = new2[:,:3]

    print('Centros dos objectos detectados visto do referêncial da camara:\n' + str(new_objs_center) + '\n')

    # Show Scene image
    img = cv2.imread(scene.information['img'])
    height,width,_ = img.shape
    # print('Height: ' + str(height) + ', Width: ' + str(width) + '\n')

    # rvec = cv2.Rodrigues(rotation)
    # print('rvec: ' + str(rvec[0]) + ' - ' + str(type(rvec[0])) + '\n')
    distCoeffs = np.float32([0, 0, 0, 0])
    
    T_world_cam = np.eye(4)
    T_world_cam[:3, :3] = rotation
    T_world_cam[:3, 3] = translation.transpose()

    # print('T_world_cam: ' + str(T_world_cam) + '\n')

    T_world_obj = np.eye(4)
    T_world_obj[:3,3] = np.array([tx, ty, tz]).transpose()
    r1 = R.from_euler('xyz', [-108, 0, -37], degrees=True)
    rot = r1.as_matrix()
    T_world_obj[:3, :3] = rot
    T_world_obj = np.asmatrix(T_world_obj)
    # print('T_world_obj: ' + str(T_world_obj) + '\n')
    # exit(0)

    # Transformação inversa da mesa
    T_mesa_world = np.eye(4)
    T_mesa_world[:3,3] = np.array([-tx, -ty, -tz]).transpose()
    r1 = R.from_euler('zyx', [108, 0, 37], degrees=True)
    rot = r1.as_matrix()
    T_mesa_world[:3, :3] = rot
    T_mesa_world = np.asmatrix(T_mesa_world)
    # print('T_mesa_world: ' + str(T_mesa_world) + '\n')
    # exit(0)

    rvec, tvec = matrix_to_rtvec(T_world_cam)  # T_cam_obj
    # print(str(rvec) + '\n' + str(tvec) + '\n')

    imagePoints,_ = cv2.projectPoints(new_objs_center, rvec, tvec, intrinsic_matrix, distCoeffs)
    print('Image Points:\n' + str(imagePoints) + '\n')

    for point in imagePoints:
        if point[0,0] > 0 and point[0,1] > 0:
            img = cv2.circle(img, (int(point[0,1]), int(point[0,0])), radius=0, color=(0, 0, 255), thickness=7)

    cv2.imshow("Display window", img)

    k = cv2.waitKey(0)

    if k == ord("s"):
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
