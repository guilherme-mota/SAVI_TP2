#!/usr/bin/env python3


# -------
# Imports
# -------
import os
import glob
import shutil
import random


def main():

    # Get the name of folders in a directory
    directory = '/home/guilherme/SAVI_Datasets/rgbd-dataset/'
    folders = os.listdir(directory)
    
    # Reorder folders in Alphabetical Order
    print(folders[0] + '\n')

    # List of images
    imgs = glob.glob(directory + '/*.png')
    print(str(len(imgs)) + ' imagens\n')
    # imgs[0] -> /home/guilherme/SAVI_Datasets/rgbd-dataset/apple_1_1_100_crop.png


    # ------------------------------------------------
    # Divisão do dataset em treino e teste (80% / 20%)
    # ------------------------------------------------
    # train_imgs = random.sample(imgs, k=165711)  # Sample random training images 
    # print(str(len(train_imgs)) + ' train imagens\n')
    # print(train_imgs[0] + '\n')
    # train_directory = '/home/guilherme/SAVI_Datasets/rgbd-dataset/train/'
    # for train_img in train_imgs:
    #     img = train_img.split('/')
    #     shutil.move(train_img, train_directory + '/' + img[-1])
    # test_directory = '/home/guilherme/SAVI_Datasets/rgbd-dataset/test/'
    # for test_img in imgs:
    #     img = test_img.split('/')
    #     shutil.move(test_img, test_directory + '/' + img[-1])


    # --------------
    # Print results
    # --------------
    # print(str(len(imgs)) + ' imagens\n')
    # print(str(type(folders)) + '\n')
    # print(str(type(folders[0])) + '\n')
    # print('Folders: ' + str(folders))
    # for img in folders:
    #     print(img + '\n')

    # -------------------------
    # Create txt file with code
    # -------------------------
    # file = open("python_code.txt", "w")
    # # Insert text in file
    # for idx,folder in enumerate(folders):
    #     if idx == 0:
    #         file.write("if class_name == '" + folder + "':\r\n\tlabel = " + str(idx))
    #     else:
    #         file.write("\r\nelif class_name == '" + folder + "':\r\n\tlabel = " + str(idx))
    # # Close file
    # file.close()


    # ------------------------
    # Delete unnecessary files
    # ------------------------
    # for folder in folders:
    #     # New directory inside class folder
    #     folders2 = os.listdir(directory + '/' + folder)
    #     for folder2 in folders2:
    #         # New directory inside diferente type insede class
    #         # folders3 = os.listdir(directory + '/' + folder + '/' + folder2)
    #         files_to_delete = glob.glob(directory + '/' + folder + '/' + folder2 + '/*depthcrop.png')
    #         files_to_delete.extend(glob.glob(directory + '/' + folder + '/' + folder2 + '/*loc.txt'))
    #         files_to_delete.extend(glob.glob(directory + '/' + folder + '/' + folder2 + '/*maskcrop.png'))
    #         # Delete files
    #         for file in files_to_delete:
    #             os.remove(file)


    # -------------------------------------------
    # Cut all images to the same folder/directory
    # -------------------------------------------
    # for folder in folders:
    #     # New directory inside class folder
    #     directory2 = directory + '/' + folder
    #     folders2 = os.listdir(directory2)
    #     for folder2 in folders2:
    #         directory3 = directory2 + '/' + folder2
    #         imgs = glob.glob(directory3 + '/*.png')
    #         folders3 = os.listdir(directory3)
    #         print(str(imgs))
    #         for idx,img in enumerate(imgs):
    #             # print('\n' + directory + '/' + folders3[idx] + '\n')
    #             # print('\n' + directory3 + '/' + folders3[idx] + '\n')
    #             shutil.move(directory3 + '/' + folders3[idx], directory + '/' + folders3[idx])
            

if __name__ == "__main__":
    main()