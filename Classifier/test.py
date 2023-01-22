#!/usr/bin/env python3


#-----------------
# Imports
#-----------------
import glob
import torch
import random
from tqdm import tqdm
from model import Model
from dataset import Dataset
from statistics import mean
from colorama import Fore, Style
from data_visualizer import DataVisualizer
from sklearn.model_selection import train_test_split
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
    dataset_path = '/home/guilherme/SAVI_Datasets/rgbd-dataset/test'
    image_filenames = glob.glob(dataset_path + '/*.png')

    # Sample only a few images to speed up testing
    image_filenames = random.sample(image_filenames, k=400)

    # Create the dataset
    dataset_test = Dataset(image_filenames)
    loader_test = torch.utils.data.DataLoader(dataset=dataset_test, batch_size=256, shuffle=True)

    # Move the model variable to the gpu if one exists
    model.to(device)

    # Run test in batches ---------------------------------------
    test_losses = []
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

        # Update Index
        idx = batch_idx + 1
    # --------------------------------------------------------

if __name__ == "__main__":
    main()