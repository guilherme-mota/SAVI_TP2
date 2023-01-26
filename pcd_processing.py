# -------------------------------------------------------------------------------
# Name:        pcd_processing
# Purpose:     features for AI system to detect and track objects
# Authors:     Guilherme Mota | Miguel Cruz | Luís Ascenção
# Created:     29/12/2022
# -------------------------------------------------------------------------------

# ------------------------------------
# Imports
# ------------------------------------
import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt
from more_itertools import locate
import pandas as pd
from matplotlib import cm
import math
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


class PointCloudProcessing():

    def __init__ (self):
        pass

    def loadpcd (self, filepath):

        # Load PCD
        self.originalpcd = o3d.io.read_point_cloud(filepath)
        self.pcd = self.originalpcd

        
    def downsample(self):

        # Pre Processing with Voxel downsampling
        self.pcd = self.originalpcd.voxel_down_sample(voxel_size=0.01) 

    def frameadjustment(self, distance_threshold=0.08, ransac_n=5, num_iterations=100):
        
        frame = o3d.geometry.TriangleMesh().create_coordinate_frame(size=1, origin=np.array([0, 0, 0]))
        
        # Frame Transform CAM to BEST FRAME CAM POS
        # R = frame.get_rotation_matrix_from_quaternion((0.923902, 0.0034424, -0.348289, -0.158423))
        # frame.rotate(R)  # , center=(0, 0, 0)
        # frame.translate((1.93816, -0.19751, 0.331437))




        # -------- Segmentation ----------
        
        # Segmentation Vars
        table_pcd = self.pcd
        num_planes = 2
        detected_plane_idx = []
        detected_plane_d = []
        

        while True:
            # Plane Segmentation
            plane_model, inliers = table_pcd.segment_plane(distance_threshold, ransac_n, num_iterations)

            # Plane Model
            [a, b, c, d] = plane_model
            
            # If there is a plane that have de negative y, will be necessary make one more measurement/segmentation 
            if b < 0:
                num_planes = 3
            
            # Print plane equation
            # print(f"Plane equation: {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0")

            # Inlier Cloud
            inlier_cloud = table_pcd.select_by_index(inliers)
            inlier_cloud.paint_uniform_color([1.0, 0, 0])
            
            # Segmetation pcd update
            outlier_cloud = table_pcd.select_by_index(inliers, invert=True)
            table_pcd = outlier_cloud

            # Append detected plane
            if b > 0:
                detected_plane_idx.append(inlier_cloud)
                detected_plane_d.append(d)

            # Condition to stop pcd segmetation (2 measurments/segmentations)
            if len(detected_plane_idx) >= num_planes: 
                num_planes = 2
                break
        
        # Find idx of the table plane 
        d_max_idx = min(range(len(detected_plane_d)), key=lambda i: abs(detected_plane_d[i]-0))
        table_pcd = detected_plane_idx[d_max_idx]
        
        # -------- Planes in Table Plane Clustering ----------
        # Clustering 
        cluster_idx = np.array(table_pcd.cluster_dbscan(eps=0.08, min_points=50))
        
        # Clusters Index
        objects_idx = list(set(cluster_idx))

        # Remove noise 
        #objects_idx.remove(-1) 

        # If exist remove noise (bug solution)
        if cluster_idx.any() == -1:
            objects_idx.remove(-1)  
        
        # -------- Planes Caracterization ----------

        # Colormap
        colormap = cm.Pastel1(list(range(0,len(objects_idx))))

        # Caracterize all planes found to proceed to table detection/isolation 
        objects=[]
        for object_idx in objects_idx:
            
            object_point_idx = list(locate(cluster_idx, lambda X: X== object_idx))
            object_points = table_pcd.select_by_index(object_point_idx)
            object_center = object_points.get_center()

            # Create a dictionary to represent all planes
            d = {}
            d['idx'] = str(objects_idx)
            d['points'] = object_points
            d['color'] = colormap[object_idx, 0:3]
            d['points'].paint_uniform_color(d['color'])
            d['center'] = object_center
            objects.append(d)

        # -------- Table Selection ----------

        # The table is deteted with the comparison between the coordinates of centers (pcd and frame) and need to have more than 10000 points
        tables_to_draw=[]
        minimum_mean_xy = 1000
        
        for object in objects:
            tables_to_draw.append(object['points'])
            mean_x = object['center'][0]
            mean_y = object['center'][1]
            mean_z = object['center'][2]
            mean_xy = abs(mean_x) + abs(mean_y)
            if mean_xy < minimum_mean_xy:
                minimum_mean_xy = mean_xy
                if len(np.asarray(object['points'].points)) > 12000:
                    #print('Mesa')
                    self.table_cloud = object['points']
                # Quando a segmentação não é bem feita dá erro aqui, é necessário colocar um try catch ou algo do genero 


        # -------- Frames ----------
        #frame = o3d.geometry.TriangleMesh().create_coordinate_frame(size=1, origin=np.array([0, 0, 0]))
        tables_to_draw.append(frame)

        # # Frame Transform CAM to BEST FRAME CAM POS
        # frame_new = copy.deepcopy(frame)
        # R = frame.get_rotation_matrix_from_quaternion((0.923902, 0.0034424, -0.348289, -0.158423))
        # frame_new.rotate(R)  # , center=(0, 0, 0)
        # frame_new.translate((1.93816, -0.19751, 0.331437))
        # tables_to_draw.append(frame_new)

        # -------- Visualization ----------
        #tables_to_draw.append(object['points'])
        o3d.visualization.draw_geometries(tables_to_draw)
        #o3d.visualization.draw_geometries([table_cloud])
        
        center = self.table_cloud.get_center()
        tx, ty, tz = center[0], center[1], center[2]
        #print('tx: ' + str(tx) + 'ty: ' + str(ty) + 'tz: ' + str(tz)) 

        return(-tx, -ty, -tz)

    def frametransform(self, r, p , y, tx, ty, tz):
    

        # Rad to Deg
        r = math.pi * r/180.0
        p = math.pi * p/180.0
        y = math.pi * y/180.0

        # Rotation
        rotation = self.pcd.get_rotation_matrix_from_xyz((r, p, y))
        self.pcd.rotate(rotation, center=(0, 0, 0))

        # Translate
        self.pcd = self.pcd.translate((tx, ty, tz))
        
    def croppcd(self, x_min, y_min, z_min, x_max, y_max, z_max):
        
        # BBOX 
        np_points = np.ndarray((8,3), dtype=float)
        np_points[0, :] = [x_min, y_min, z_min]
        np_points[1, :] = [x_max, y_min, z_min]
        np_points[2, :] = [x_max, y_max, z_min]
        np_points[3, :] = [x_min, y_max, z_min]

        np_points[4, :] = [x_min, y_min, z_max]
        np_points[5, :] = [x_max, y_min, z_max]
        np_points[6, :] = [x_max, y_max, z_max]
        np_points[7, :] = [x_min, y_max, z_max]

        
        bbox_points = o3d.utility.Vector3dVector(np_points)

        self.bbox = o3d.geometry.AxisAlignedBoundingBox.create_from_points(bbox_points)
        self.bbox.color = (0, 1, 0)
        self.pcd = self.pcd.crop(self.bbox)
        
    def planesegmentation(self, distance_threshold=0.01, ransac_n=3, num_iterations=100):
        
        plane_model, inliers = self.pcd.segment_plane(distance_threshold,ransac_n, num_iterations)
        #plane_model, inliers = self.table_cloud.segment_plane(distance_threshold,ransac_n, num_iterations)
        
        [a, b, c, d] = plane_model
        
        #print(f"Plane equation: {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0")

        self.inliers = self.pcd.select_by_index(inliers)
        
        self.outlier_cloud = self.pcd.select_by_index(inliers, invert=True)
        
        #self.inliers = self.table_cloud.select_by_index(inliers)
        #self.outlier_cloud = self.table_cloud.select_by_index(inliers, invert=True)
        

    def pcdclustering(self):
        
        # Clustering 
        cluster_idx = np.array(self.outlier_cloud.cluster_dbscan(eps=0.030, min_points=60, print_progress=True))
        
        # Clusters Index
        objects_idx = list(set(cluster_idx))

        # Remove noise 
        objects_idx.remove(-1) 

        # If exist remove noise (bug solution)
        # if objects_idx.any() == -1:
        #     objects_idx.remove(-1)  
        
        #colormap = cm.Pastel1(list(range(0,len(objects_idx))))
        objects=[]
       
        for object_idx in objects_idx:
            
            object_point_idx = list(locate(cluster_idx, lambda X: X== object_idx))
            object_points = self.outlier_cloud.select_by_index(object_point_idx)
            object_center = object_points.get_center()
            # Create a dictionary to represent objects
            d = {}
            d['idx'] = str(objects_idx)
            d['points'] = object_points
            #d['color'] = colormap[object_idx, 0:3]
            #d['points'].paint_uniform_color(d['color'])
            d['center'] = object_center
            print('center of object' + str(object_idx) + ': ' + str(object_center))
            # -------------- STDeviation of each coordinate about XY and Z Axis ------------------

            
            # points = len(np.asarray(object_points.points))
            # x_coordnites = []
            # y_coordnites = []
            # z_coordnites = []

            # for num in range(points):
            #     # print(np.asarray(object_points.points[num][0]))
            #     # print(np.asarray(object_points.points[num][1]))
            #     # print(np.asarray(object_points.points[num][2]))
            #     x_coordnites.append(np.asarray(object_points.points[num][0]))
            #     y_coordnites.append(np.asarray(object_points.points[num][1]))
            #     z_coordnites.append(np.asarray(object_points.points[num][2]))

            # stdeviation_x = np.std(x_coordnites)
            # print('desvio padrão das coord no eixo do x, obj: ' +  str(object_idx) + ' ' + str(stdeviation_x))
            # stdeviation_y = np.std(y_coordnites)
            # print('desvio padrão das coord no eixo do y, obj: ' +  str(object_idx) + ' ' + str(stdeviation_y))
            # stdeviation_z = np.std(z_coordnites)
            # print('desvio padrão das coord no eixo do z, obj: ' +  str(object_idx) + ' ' + str(stdeviation_z))

            # # print(np.asarray(object_points.points[0]))
            # # print(np.asarray(object_points.points[0][0]))
            # # print(len(np.asarray(object_points.points)))

      
            objects.append(d)
        

        self.objects_to_draw=[]

        # to draw each object already separated
        for object in objects:
            self.objects_to_draw.append(object['points'])



        
