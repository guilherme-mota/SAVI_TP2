#!/usr/bin/env python3


# -------------------------------------------------------------------------------
# Name:        data_visualizer
# Purpose:     Plot the loss from each epoch
# Authors:     Guilherme Mota | Miguel Cruz | Luís Ascenção
# Created:     29/12/2022
# -------------------------------------------------------------------------------


#-----------------
# Imports
#-----------------
import torch
import matplotlib.pyplot as plt


class DataVisualizer():

    def __init__(self, title):
        """
        Initialize the objecte attributes
        :param title: title of the figure
        """
    
        # Initialize Attributes
        self.handles = {}  # dictionary of handles per layer
        self.title = title  # figure title
         
        # Setup figure
        self.figure = plt.figure(title)
        self.figure.canvas.manager.set_window_title(title)
        self.figure.set_size_inches(4,3)
        plt.suptitle(title)
        plt.legend(loc='best')
        plt.waitforbuttonpress(0.1)


    def draw(self,xs,ys,layer='default',marker='.',markersize=1,color=[0.5,0.5,0.5], alpha=1, label='', x_label='', y_label=''):
        """
        Draws the graph of the loss for a given epoch
        :param xs: values of the x axis
        :param ys: values of the y axis
        :param layer: (defaulte value = 'default')
        :param marker: marker type (defaulte value = '.')
        :param markersize: marker size (defaulte value = 1)
        :param color: color of the marker (defaulte value = [0.5,0.5,0.5])
        :param alpha: (defaulte value = 1)
        :param label: label for the plot (defaulte value = '')
        :param x_label: label for the x axis (defaulte value = '')
        :param y_label: label for the y axis (defaulte value = '')
        """

        xs, ys = self.toNP(xs,ys) # make sure we have np arrays
        plt.figure(self.title)

         # Verify if it's the first time drawing this layer
        if not layer in self.handles:
            self.handles[layer] = plt.plot(xs, ys, marker, markersize=markersize, 
                                        color=color, alpha=alpha, label=label)
            plt.legend(loc='best')
        else: # use set to edit plot
            plt.setp(self.handles[layer], data=(xs, ys))  # update lm

        plt.xlabel(x_label)    
        plt.ylabel(y_label)    
        plt.draw()

        # Wait key input
        key = plt.waitforbuttonpress(0.01)
        if not plt.fignum_exists(1):
            print('Terminating')
            exit(0)


    def toNP(self, xs, ys):
        """
        Convertes values from torch.tensor to numpy arrays. Must be exucuted before passing the values to plot!
        :param xs: values of the x axis as torch.tensor
        :param ys: values of the y axis as torch.tensor
        :return: xs and ys as numpy arrays
        """

        if torch.is_tensor(xs):
            xs = xs.cpu().detach().numpy()

        if torch.is_tensor(ys):
            ys = ys.cpu().detach().numpy()

        return xs,ys


    def recomputeAxisRanges(self):
        """
        Update axis ranges
        """

        plt.figure(self.title)

        ax = plt.gca()
        ax.relim()
        ax.autoscale_view()
        
        plt.draw()