#!/usr/bin/env python3

# -------------------------------------------------------------------------------
# Name:        test
# Purpose:     Tests the classifier
# Authors:     Guilherme Mota | Miguel Cruz | Luís Ascenção
# Created:     29/12/2022
# -------------------------------------------------------------------------------


#-----------------
# Imports
#-----------------
import glob
import torch
import random
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sn
import pandas as pd
from tqdm import tqdm
from model import Model
from dataset import Dataset
from statistics import mean
from colorama import Fore, Style
from data_visualizer import DataVisualizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix,classification_report
from classification_visualizer import ClassificationVisualizer


def main():

    # -----------------------------------------------------------------
    # Initialization
    # -----------------------------------------------------------------
    # Define hyper parameters
    loss_function = torch.nn.CrossEntropyLoss()
    model = Model()  # Instantiate model
    model_path = 'model.pkl'
    checkpoint = torch.load(model_path)
    model.load_state_dict(checkpoint['model_state_dict'])

    # Init visualization
    test_visualizer = ClassificationVisualizer('Test Images')

    # Verify if the GPU is available
    device = 'cuda:0' if torch.cuda.is_available() else 'cpu' # cuda: 0 index of gpu


    # -----------------------------------------------------------------
    # Datasets
    # -----------------------------------------------------------------
    dataset_path = '../docs/rgbd-dataset/test'
    image_filenames = glob.glob(dataset_path + '/*.png')

    # Sample only a few images to speed up testing
    image_filenames = random.sample(image_filenames, k=1536)

    # Create the dataset
    dataset_test = Dataset(image_filenames)
    loader_test = torch.utils.data.DataLoader(dataset=dataset_test, batch_size=256, shuffle=True)

    # Move the model variable to the gpu if one exists
    model.to(device)
    

    # Run test in batches -----------------------------------------------------------------------------------------------
    test_losses = []
    labels = []
    predicted_labels = []
    idx = 0
    for batch_idx, (image_t, label_t) in tqdm(enumerate(loader_test), total=len(loader_test), desc=Fore.GREEN + 'Testing batches' + str(idx) +  Style.RESET_ALL):

        image_t = image_t.to(device)
        label_t = label_t.to(device)

        # Apply the network to get the predicted ys
        label_t_predicted = model.forward(image_t)

        # Compute the error based on the predictions
        loss = loss_function(label_t_predicted, label_t)

        test_losses.append(loss.data.item())

        test_visualizer.draw(image_t, label_t, label_t_predicted)

        
        for probability in label_t_predicted.cpu().tolist():
            predicted_labels.append(np.argmax(probability))
        labels.append(label_t.cpu().tolist())

        # Update Index
        idx = batch_idx + 1
    # ----------------------------------------------------------------------------------------------------------------

    
    # Terminal Prints -----------------------------------------------------------------------
    print(test_losses)
    labels = [item for sublist in labels for item in sublist]
    total_matrix_of_confusion = confusion_matrix(labels, predicted_labels)
    print(classification_report(labels, predicted_labels))
    print("Number of Labels: ",len(labels),"Number of Predicted Labels: ",len(predicted_labels))


    # Visualization -----------------------------------------------------------------------
    df_cm = pd.DataFrame(total_matrix_of_confusion)
    plt.figure()
    sn.set(font_scale=0.7) # for label size
    sn.heatmap(df_cm, annot=True)
    plt.show()


if __name__ == "__main__":
    main()