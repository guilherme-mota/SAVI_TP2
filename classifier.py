#!/usr/bin/env python3


# -------------------------------------------------------------------------------
# Name:        classifier
# Purpose:     Classifies the diferent object detected
# Authors:     Guilherme Mota | Miguel Cruz | Luís Ascenção
# Created:     29/12/2022
# -------------------------------------------------------------------------------


#-----------------
# Imports
#-----------------
import glob
import torch
import numpy as np
from Classifier.model import Model
from Classifier.dataset import Dataset
import cv2


class Classifier:

    def __init__(self):
        """
        Initialize the objecte attributes
        """

        # Instantiate model
        self.model = Model()

        # Define hyper parameters
        self.loss_function = torch.nn.CrossEntropyLoss()
        self.model_path = 'Classifier/model.pkl'
        self.checkpoint = torch.load(self.model_path)
        self.model.load_state_dict(self.checkpoint['model_state_dict'])

        # Verify if the GPU is available
        self.device = 'cuda:0' if torch.cuda.is_available() else 'cpu' # cuda: 0 index of gpu

        # Initialize Attributes
        self.image_filenames = glob.glob('Image_Database' + '/*.png')
        self.dataset = Dataset(self.image_filenames)
        self.loader = torch.utils.data.DataLoader(dataset=self.dataset, batch_size=len(self.dataset), shuffle=True)
    

    def classifieImages(self):
        """
        Classifies a list of images by feeding them into a neural network
        :return: predicted label for each image
        """

        # Move the model variable to the gpu if one exists
        self.model.to(self.device)

        predicted_labels = []
        for batch_idx, (image_t, label_t) in enumerate(self.loader):

            image_t = image_t.to(self.device)
            label_t = label_t.to(self.device)

            # Feed the image to the network in order to get the predicted ys
            label_t_predicted = self.model.forward(image_t)

            for probability in label_t_predicted.cpu().tolist():
                predicted_labels.append(np.argmax(probability))

        print('Predicted Labels:\n' + str(predicted_labels) + '\n')

        return predicted_labels