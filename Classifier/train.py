#!/usr/bin/env python3


# -------------------------------------------------------------------------------
# Name:        train
# Purpose:     Trains the classifier
# Authors:     Guilherme Mota | Miguel Cruz | Luís Ascenção
# Created:     29/12/2022
# -------------------------------------------------------------------------------


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


def main():

    # -----------------------------------------------------------------
    # Initialization
    # -----------------------------------------------------------------
    # Define hyper parameters
    resume_training = True
    learning_rate = 0.001
    maximum_num_epochs = 8
    termination_loss_threshold =  0.01
    loss_function = torch.nn.CrossEntropyLoss()
    model = Model()  # Instantiate model
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    model_path = 'model.pkl'

    # Verify if the GPU is available
    device = 'cuda:0' if torch.cuda.is_available() else 'cpu' # cuda: 0 index of gpu


    # -----------------------------------------------------------------
    # Datasets
    # -----------------------------------------------------------------
    dataset_path = '/home/guilherme/SAVI_Datasets/rgbd-dataset/train'
    image_filenames = glob.glob(dataset_path + '/*.png')

    # Create the dataset
    dataset_train = Dataset(image_filenames)
    loader_train = torch.utils.data.DataLoader(dataset=dataset_train, batch_size=648, shuffle=True)


    # -----------------------------------------------------------------
    # Training
    # -----------------------------------------------------------------
    # Init visualization of loss
    loss_visualizer = DataVisualizer('Loss')
    loss_visualizer.draw([0,maximum_num_epochs], [termination_loss_threshold, termination_loss_threshold], layer='threshold', marker='--', markersize=1, color=[0.5,0.5,0.5], alpha=1, label='threshold', x_label='Epochs', y_label='Loss')

    # Resume training ---------------------------------------------------
    if resume_training:
        checkpoint = torch.load(model_path)
        model.load_state_dict(checkpoint['model_state_dict'])
        optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        idx_epoch = checkpoint['epoch'] + 1
        epoch_train_losses = checkpoint['train_losses']
    else:
        idx_epoch = 0
        epoch_train_losses = []
    # -----------------------------------------------------------------------

    # Move the model variable to the gpu if one exists
    model.to(device)

    while True:

        # Train batch by batch -----------------------------------------------
        train_losses = []
        for batch_idx, (image_t, label_t) in tqdm(enumerate(loader_train), total=len(loader_train), desc=Fore.GREEN + 'Training batches for Epoch ' + str(idx_epoch) +  Style.RESET_ALL):

            image_t = image_t.to(device)
            label_t = label_t.to(device)

            # Apply the network to get the predicted ys
            label_t_predicted = model.forward(image_t)

            # Compute the error based on the predictions
            loss = loss_function(label_t_predicted, label_t)

            # Update the model, i.e. the neural network's weights 
            optimizer.zero_grad() # resets the weights to make sure we are not accumulating
            loss.backward() # propagates the loss error into each neuron
            optimizer.step() # update the weights


            train_losses.append(loss.data.item())
        # ------------------------------------------------------------------

        # Compute the loss for the epoch
        epoch_train_loss = mean(train_losses)
        epoch_train_losses.append(epoch_train_loss)

        # Visualization
        loss_visualizer.draw(list(range(0, len(epoch_train_losses))), epoch_train_losses, layer='train loss', marker='-', markersize=1, color=[0,0,0.7], alpha=1, label='Train Loss', x_label='Epochs', y_label='Loss')
        loss_visualizer.recomputeAxisRanges()

        # Save checkpoint
        model.to('cpu')
        torch.save({
            'epoch': idx_epoch,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'train_losses': epoch_train_losses,
            }, model_path)
        model.to(device)

        # Increment Epoch count
        idx_epoch += 1

        # Termination criteria
        if idx_epoch > maximum_num_epochs:
            print('Finished training. Reached maximum number of epochs.')
            break
        elif epoch_train_loss < termination_loss_threshold:
            print('Finished training. Reached target loss.')
            break


if __name__ == "__main__":
    main()