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
import glob
import os
import pyttsx3
import cv2
import copy
import torch
import argparse
import numpy as np
import open3d as o3d
from Classifier.dataset import Dataset
from classifier import Classifier
from scenes_information import Scenes
import open3d.visualization.gui as gui
from pcd_processing import PointCloudProcessing
from scipy.spatial.transform import Rotation as R
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

def matrix_to_rtvec(matrix):

    "Convert 4x4 matrix to rotation vector and translation vector"
    (rvec, jac) = cv2.Rodrigues(matrix[:3, :3])
    tvec = matrix[:3, 3]

    return rvec, tvec

def extractSmallImage(image_full, x1, y1, x2, y2):
    return image_full[y1:y2, x1:x2]

def stringConstruct(old_dict, new_dict):
    if(old_dict==new_dict):
        return "There are no changes to the scenario"
    else:
        new_string = "There are "
        for key in new_dict:
            if (new_dict[key][1] == 1):
                #print(new_dic[key])
                new_string = new_string + str(new_dict[key][1]) + " " + str(new_dict[key][0]).replace("_"," ") + ", "
            elif (new_dict[key][1] != 0):
                new_string = new_string + str(new_dict[key][1]) + " " + str(new_dict[key][0]).replace("_"," ") + "s, "
        new_string = new_string + "on the table."
        return new_string



def main():
    
    # ------------------------------------------------------------------------
    # Initialization 
    # ------------------------------------------------------------------------

    # Initialize parser
    parser = argparse.ArgumentParser(description="Point Cloud Scene")
    parser.add_argument("-s", "--scene", nargs='?', const=1, type=int, help="Scene selection", default=1)
    args = vars(parser.parse_args())

    preset_dictionary = {0:['apple',0],1:['ball',0],2:['banana',0],3:['bell_peper',0],4:['binder',0],5:['bowl',0],6:['calculator',0],
    7:['camera',0],8:['cap',0],9:['cell_phone',0],10:['cereal_box',0],11:['coffee_mug',0],12:['comb',0],13:['dry_battery',0],14:['flashlight',0],15:['food_bag',0],
    16:['food_box',0],17:['food_can',0],18:['food_cup',0],19:['food_jar',0],20:['garlic',0],21:['glue_stick',0],22:['greens',0],23:['hand_towel',0],24:['instant_noodles',0],
    25:['keyboard',0],26:['kleenex',0],27:['lemon',0],28:['lightbulb',0],29:['lime',0],30:['marker',0],31:['mushroom',0],32:['notebook',0],33:['onion',0],
    34:['orange',0],35:['peach',0],36:['pear',0],37:['pitcher',0],38:['plate',0],39:['pliers',0],40:['potato',0],41:['rubber_eraser',0],42:['scissors',0],
    43:['shampoo',0],44:['soda_can',0],45:['sponge',0],46:['stapler',0],47:['tomato',0],48:['toothbrush',0],49:['toothpaste',0],50:['water_bottle',0]}

    old_dict = preset_dictionary.copy()
    new_dict = old_dict.copy()
    engine = pyttsx3.init()
    
    # Init Scene
    scene = Scenes(args['scene'])

    # Load PCD
    print('Starting Scene 3D Processing...\n')
    p = PointCloudProcessing()
    p.loadpcd(scene.information['pcd'])   
    
    
    # ------------------------------------------------------------------------
    # Execution 
    # ------------------------------------------------------------------------

    # Pre Processing with Voxel downsampling to increase process velocity
    p.downsample()  # 0.01

    # Calculation of the reference transformation parameters for the center of the table - In this case only for TRANS
    tx, ty, tz = p.frameadjustment()        
  
    # Frame Transform CAM to TABLE
    p.frametransform(0, 0, 0, tx, ty, tz)
    # p.frametransform(-108, 0, 0, 0, 0, 0)
    p.frametransform(-112, 0, 0, 0, 0, 0)
    p.frametransform(0, 0, -37, 0, 0, 0)

    # --------------------------------------------------------------------------
    # Transformação do referêncial da camara (Global) para o referêncial da Mesa
    # --------------------------------------------------------------------------
    trans = np.eye(4)
    trans[:3,3] = np.array([-tx, -ty, -tz]).transpose() # Converter para matrix
    trans = np.asmatrix(trans)

    rot1 = np.eye(4)
    r1 = R.from_euler('xyz', [108, 0, 0], degrees=True)
    rot1[:3, :3] = r1.as_matrix()
    rot1 = np.asmatrix(rot1)

    rot2 = np.eye(4)
    r2 = R.from_euler('xyz', [0, 0, 37], degrees=True)
    rot2[:3, :3] = r2.as_matrix()
    rot2 = np.asmatrix(rot2)

    T_cam_mesa = np.eye(4)
    T_cam_mesa = rot1 * T_cam_mesa   # rotação de -108 em torno de x
    T_cam_mesa = rot2 * T_cam_mesa
    T_cam_mesa = trans * T_cam_mesa  # translação tx, ty, tz
    # -----------------------------------------------
    
    # Isolation of interest part (table + objects)
    p.croppcd(-0.6, -0.6, -0.02, 0.6, 0.6, 0.4)
    
    # Plane segmentation ---> Table detection and objects isolation
    p.planesegmentation()
    
    # Object Clustering
    p.pcdclustering()
    
    # ------------------------------------------------------------------------
    # Visualization
    # ------------------------------------------------------------------------

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
    entities_to_draw = np.concatenate((entities_to_draw, p.objects_to_draw))

    # Visualization of original PCD with picking points window 
    # print("")
    # print("1) Please pick at least three correspondences using [shift + left click]")
    # print("   Press [shift + right click] to undo point picking")
    # print("2) After picking points, press 'Q' to close the window")
    # vis = o3d.visualization.VisualizerWithEditing()
    # vis.create_window()
    # vis.add_geometry(p.originalpcd)
    # vis.run()  # user picks points
    # vis.destroy_window()
    # print("")

    # Visualization of objects + frame + bbox + object bbox
    o3d.visualization.draw_geometries(entities_to_draw,
                                            zoom = view['trajectory'][0]['zoom'],
                                            front = view['trajectory'][0]['front'],
                                            lookat = view['trajectory'][0]['lookat'],
                                            up = view['trajectory'][0]['up'])
    
    # Visualization of objects + object bbox
    # o3d.visualization.draw_geometries(p.objects_to_draw,
    #                                          zoom = view['trajectory'][0]['zoom'],
    #                                          front = view['trajectory'][0]['front'],
    #                                          lookat = view['trajectory'][0]['lookat'],
    #                                          up = view['trajectory'][0]['up'])


    # ----------------------------------------------------------------------------
    # Relation between 3D points and RGB images
    # ----------------------------------------------------------------------------
    print('\n')

    # Center position of each object --------------------------------------------
    objs_center = np.empty([len(p.objects_properties), 3], dtype=np.float32)
    for idx,obj in enumerate(p.objects_properties):
        objs_center[idx,:]= np.float32(obj['center'])
    # print('Centros dos objectos detectados visto do referêncial da mesa:\n' + str(objs_center) + '\n')

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
    # ------------------------------------------------------------------------

    # Show Scene image -------------------------------------------------------
    img_original = cv2.imread(scene.information['img'])
    img_gui = copy.deepcopy(img_original)
    # height,width,_ = img_original.shape
    # print('Height: ' + str(height) + ', Width: ' + str(width) + '\n')
    # ------------------------------------------------------------------------

    # Convert quaternion to rotation matrix ----------------------------------
    r = R.from_quat(scene.information['rot'])
    rotation = r.as_matrix()
    # print('Rotation: ' + str(rotation) + '\n')

    translation = np.float32(scene.information['trans'])
    # print('Translation: ' + str(translation) + '\n')
    
    T_world_cam = np.eye(4)
    T_world_cam[:3, :3] = rotation
    T_world_cam[:3, 3] = translation.transpose()
    # print('T_world_cam: ' + str(T_world_cam) + '\n')
    rvec, tvec = matrix_to_rtvec(T_world_cam)  # T_cam_obj
    # print('rvec:\n' + str(rvec) + '\n\n' + 'tvec:\n' + str(tvec) + '\n')
    # ------------------------------------------------------------------------

    # Intrinsic Matrix -------------------------------------------------------
    alhpa = 570.3
    intrinsic_matrix = np.float32([[alhpa,      0, 320],
                                   [    0,  alhpa, 240],
                                   [    0,      0,   1]])
    # print('Intrinsic Matrix:\n' + str(intrinsic_matrix) + '\n')
    # ------------------------------------------------------------------------

    distCoeffs = np.float32([0, 0, 0, 0])
    # print('distCoeffs:\n' + str(distCoeffs) + '\n')
    # ------------------------------------------------------------------------

    imagePoints,_ = cv2.projectPoints(new_objs_center, rvec, tvec, intrinsic_matrix, distCoeffs)
    print('Image Points:\n' + str(imagePoints) + '\n')


    # ----------------------------------------------------------------------------
    # Classification of objects in the scene
    # ----------------------------------------------------------------------------
    c = 60  # size of the box araound the object
    obj_imgs = []  # list of object imgs
    for idx, point in enumerate(imagePoints):

        if point[0,0] > 0 and point[0,1] > 0:

            # Draw circle in the center of the object
            img_gui = cv2.circle(img_gui, (int(point[0,0]), int(point[0,1])), radius=0, color=(0, 0, 255), thickness=7)

            # Draw BoundingBox around object
            x1 = int(point[0,0]) - c
            y1 = int(point[0,1]) - c
            x2 = int(point[0,0]) + c
            y2 = int(point[0,1]) + c
            cv2.rectangle(img_gui,(x1,y1),(x2, y2),color=(0, 0, 255),thickness=3)

            # Extract small img of the obj
            obj_img = extractSmallImage(img_original, x1, y1, x2, y2)

            # Add img to list
            obj_imgs.append(obj_img)

            # Save image of new face detected in database
            # TODO: Eleminar img antes de guardar as novas
            obj_img = cv2.cvtColor(obj_img, cv2.COLOR_BGR2RGB)
            cv2.imwrite('Image_Database/obj' + str(idx) + '.png', obj_img)

    # Init Classifier
    classifier = Classifier()

    predicted_labels = classifier.classifieImages()
    #exit(0)
    for label in predicted_labels:
        if new_dict.get(label) is not None:
                new_dict[label] = [new_dict[label][0],new_dict[label][1] + 1]
        else:
            raise ValueError('Unknow class')

    num_of_objects = len(p.objects_to_draw)
    print('Number of detected objects = ' + str(num_of_objects) + '     ')
    
    # Visualization throuh Application (objects + objects bboxes + labels)
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
        iterator_of_obj = 0
        for obj in p.objects_properties:
            name_of_object = new_dict[predicted_labels[iterator_of_obj]][0]
            l = widget3d.add_3d_label(obj['center']+(-0.1,0,((obj['height']/2)+0.05)), 'Object: ' + name_of_object)#str(obj['idx']))
            l2 = widget3d.add_3d_label(obj['center']+(-0.1,0,((obj['height']/2)+0.08)), 'Aprox. Volume: ' + str(round(obj['x_width']*1000,0)) + 
                                    ' x ' + str(round(obj['y_width']*1000,0)) + ' x ' + str(round(obj['height']*1000,0)) + 'mm' )

            #l.color = gui.Color(p.objects_to_draw.colors[idx][0], p.objects_to_draw.colors[idx][1],
            #                      p.objects_to_draw.colors[idx][2])
            #l.scale = np.random.uniform(0.5, 3.0)
            iterator_of_obj+=1
    bbox = widget3d.scene.bounding_box
    widget3d.setup_camera(60.0, bbox, bbox.get_center())
    w.add_child(widget3d)
    app.run()

    # ----------------------------------------------------------------------------
    # Termination
    # ----------------------------------------------------------------------------
    cv2.imshow("Display window", img_gui)
    
    engine.say(stringConstruct(old_dict,new_dict))
    engine.runAndWait()
    old_dict = new_dict.copy()
    new_dict = preset_dictionary.copy()


    # Display all objects
    for idx,img in enumerate(obj_imgs):
        cv2.imshow("Obj" + str(idx), img)

    k = cv2.waitKey(0)

    if k == ord("s"):
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
