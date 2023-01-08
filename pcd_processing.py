import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt
from more_itertools import locate
import pandas as pd
from matplotlib import cm
import math




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
        # print(self.originalpcd)
        # print(np.asarray(self.originalpcd.points))
        self.pcd = self.originalpcd
        
    def downsample(self):

        # Pre Processing with Voxel downsampling
        self.pcd = self.originalpcd.voxel_down_sample(voxel_size=0.01) 

    def frameadjustment(self, distance_threshold=0.05, ransac_n=5, num_iterations=100):
        detected_plane_idx = []
        num_planes = 2

        while True:
            plane_model, inliers = self.pcd.segment_plane(distance_threshold, ransac_n, num_iterations)
            [a, b, c, d] = plane_model

            if b < 0:
                num_planes=3
            

            print(f"Plane equation: {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0")


            inlier_cloud = self.pcd.select_by_index(inliers)
            inlier_cloud.paint_uniform_color([1.0, 0, 0])

            outlier_cloud = self.pcd.select_by_index(inliers, invert=True)
            
            o3d.visualization.draw_geometries([inlier_cloud],
                                            zoom=0.8,
                                            front=[-0.4999, -0.1659, -0.8499],
                                            lookat=[2.1813, 2.0619, 2.0999],
                                            up=[0.1204, -0.9852, 0.1215])
            self.pcd = outlier_cloud
            detected_plane_idx.append(inlier_cloud)
            if len(detected_plane_idx) >= num_planes: 
                num_planes = 2
                break

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
        
    def planesegmentation(self, distance_threshold=0.05, ransac_n=3, num_iterations=100):
        
        plane_model, inliers = self.pcd.segment_plane(distance_threshold,ransac_n, num_iterations)
        
        [a, b, c, d] = plane_model
        
        #print(f"Plane equation: {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0")

        self.inliers = self.pcd.select_by_index(inliers)
        
        self.outlier_cloud = self.pcd.select_by_index(inliers, invert=True)

        

    def pcdclustering(self):
        
        # Clustering 
        cluster_idx = np.array(self.outlier_cloud.cluster_dbscan(eps=0.04, min_points=50, print_progress=True))
        
        # Clusters Index
        objects_idx = list(set(cluster_idx))

        # Remove noise 
        #objects_idx.remove(-1) 

        # If exist remove noise (bug solution)
        if cluster_idx.any() == -1:
            objects_idx.remove(-1)  
        
        colormap = cm.Pastel1(list(range(0,len(objects_idx))))
        objects=[]
        for object_idx in objects_idx:
            
            object_point_idx = list(locate(cluster_idx, lambda X: X== object_idx))
            object_points = self.outlier_cloud.select_by_index(object_point_idx)

            # Create a dictionary to represent objects
            d = {}
            d['idx'] = str(objects_idx)
            d['points'] = object_points
            d['color'] = colormap[object_idx, 0:3]
            d['points'].paint_uniform_color(d['color'])
        
            objects.append(d)

        self.objects_to_draw=[]

        # to draw each object already separated
        for object in objects:
            self.objects_to_draw.append(object['points'])
            
        

        
