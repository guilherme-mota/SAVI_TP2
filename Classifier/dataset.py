#!/usr/bin/env python3


# -------------------------------------------------------------------------------
# Name:        dataset
# Purpose:     Dataset model for classifying 51 objects
# Authors:     Guilherme Mota | Miguel Cruz | Luís Ascenção
# Created:     29/12/2022
# -------------------------------------------------------------------------------


#-----------------
# Imports
#-----------------
import torch
from PIL import Image
from torchvision import transforms


class Dataset(torch.utils.data.Dataset):

    def __init__(self, image_filenames):
        """
        Initialize the objecte attributes
        :param image_filenames: image directory list
        """

        # Init base class
        super().__init__()

        # Initialize Attributes
        self.image_filenames = image_filenames
        self.num_images = len(self.image_filenames)
        self.labels = []

        # fill list with image labels
        for image_filename in self.image_filenames:
            self.labels.append(self.getClassFromFilename(image_filename))
        
        # Create a set of transformations
        self.transforms = transforms.Compose([transforms.Resize((224,224)),transforms.ToTensor()])


    def __getitem__(self, index):
        """
        Given a specific index, returns the image transformed and the corresponding label
        :param index: index of the image
        :return: image transformed and it's label
        """

        # Load the image
        image_pil = Image.open(self.image_filenames[index])

        # Transform image to tensor
        image_t = self.transforms(image_pil)

        return image_t, self.labels[index]


    def __len__(self):
        """
        Returns the length of the dataset
        :return: number of images in the dataset
        """
        return self.num_images


    def getClassFromFilename(self, filename):
        """
        Given a given filename, returns the corresponding label
        :param filename: name of the image file
        :return: image label, from 0 to 50; in case of non-match, returns -1
        """

        parts = filename.split('/')
        part = parts[-1]
        parts = part.split('_')

        # File name -> class_name_#_#_#_crop.png
        if len(parts) - 4 == 1:
            class_name = parts[0]
        elif len(parts) - 4 == 2:
            class_name = parts[0] + '_' + parts[1]
        else:
            class_name = ''
        
        # use the idx of the outputs vector where the 1 should be
        if class_name == 'apple':
            label = 0
        elif class_name == 'ball':
            label = 1
        elif class_name == 'banana':
            label = 2
        elif class_name == 'bell_pepper':
            label = 3
        elif class_name == 'binder':
            label = 4
        elif class_name == 'bowl':
            label = 5
        elif class_name == 'calculator':
            label = 6
        elif class_name == 'camera':
            label = 7
        elif class_name == 'cap':
            label = 8
        elif class_name == 'cell_phone':
            label = 9
        elif class_name == 'cereal_box':
            label = 10
        elif class_name == 'coffee_mug':
            label = 11
        elif class_name == 'comb':
            label = 12
        elif class_name == 'dry_battery':
            label = 13
        elif class_name == 'flashlight':
            label = 14
        elif class_name == 'food_bag':
            label = 15
        elif class_name == 'food_box':
            label = 16
        elif class_name == 'food_can':
            label = 17
        elif class_name == 'food_cup':
            label = 18
        elif class_name == 'food_jar':
            label = 19
        elif class_name == 'garlic':
            label = 20
        elif class_name == 'glue_stick':
            label = 21
        elif class_name == 'greens':
            label = 22
        elif class_name == 'hand_towel':
            label = 23
        elif class_name == 'instant_noodles':
            label = 24
        elif class_name == 'keyboard':
            label = 25
        elif class_name == 'kleenex':
            label = 26
        elif class_name == 'lemon':
            label = 27
        elif class_name == 'lightbulb':
            label = 28
        elif class_name == 'lime':
            label = 29
        elif class_name == 'marker':
            label = 30
        elif class_name == 'mushroom':
            label = 31
        elif class_name == 'notebook':
            label = 32
        elif class_name == 'onion':
            label = 33
        elif class_name == 'orange':
            label = 34
        elif class_name == 'peach':
            label = 35
        elif class_name == 'pear':
            label = 36
        elif class_name == 'pitcher':
            label = 37
        elif class_name == 'plate':
            label = 38
        elif class_name == 'pliers':
            label = 39
        elif class_name == 'potato':
            label = 40
        elif class_name == 'rubber_eraser':
            label = 41
        elif class_name == 'scissors':
            label = 42
        elif class_name == 'shampoo':
            label = 43
        elif class_name == 'soda_can':
            label = 44
        elif class_name == 'sponge':
            label = 45
        elif class_name == 'stapler':
            label = 46
        elif class_name == 'tomato':
            label = 47
        elif class_name == 'toothbrush':
            label = 48
        elif class_name == 'toothpaste':
            label = 49
        elif class_name == 'water_bottle':
            label = 50
        else:
            label = -1          #in case we don't know the label
            #raise ValueError('Unknown class')

        return label