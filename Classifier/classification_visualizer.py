#!/usr/bin/env python3


#-----------------
# Imports
#-----------------
import numpy as np
import random
import matplotlib.pyplot as plt
import torch.nn.functional as F
from torchvision import transforms


class ClassificationVisualizer():

    def __init__(self, title):
        
        # Initial Parameters
        self.handles = {} # dictionary of handles per layer
        self.title = title
        self.tensor_to_PIL_image = transforms.ToPILImage()

    def draw(self, inputs, labels, outputs):

        # Setup figure
        self.figure = plt.figure(self.title)
        plt.axis('off')
        self.figure.canvas.manager.set_window_title(self.title)
        self.figure.set_size_inches(8,6)
        plt.suptitle(self.title)
        plt.legend(loc='best')

        inputs = inputs
        batch_size,_,_,_ = list(inputs.shape)

        output_probabilities = F.softmax(outputs, dim=1).tolist()

        predicted_labels = []
        for probability in output_probabilities:
            predicted_labels.append(np.argmax(probability))
        
        random_idxs = random.sample(list(range(batch_size)), k=5*5)  # amostra random de 25 imagens

        for plot_idx, image_idx in enumerate(random_idxs, start=1):

            label = labels[image_idx]  # label real da imagem
            predicted_label = predicted_labels[image_idx]  # label mais provável para a imagem

            # Verificar sucesso da 'prediction'
            success = True if (label.data.item() == predicted_label) else False

            # Get images
            image_t = inputs[image_idx,:,:,:]
            image_PIL = self.tensor_to_PIL_image(image_t)

            # Define a 5x5 subplot matrix
            ax = self.figure.add_subplot(5,5,plot_idx)
            plt.imshow(image_PIL)
            ax.xaxis.set_ticklabels([])
            ax.yaxis.set_ticklabels([])
            ax.xaxis.set_ticks([])
            ax.yaxis.set_ticks([])

            color = 'green' if success else 'red'  # Color of the title
            title = self.getTitle(label.data.item())  # Get title for the image
            title += ' ' + str(image_idx)

            ax.set_xlabel(title, color=color)

        # Draw Plot
        plt.draw()

        # Wait key
        key = plt.waitforbuttonpress(3)  # 0.05
        if not plt.fignum_exists(1):
            print('Terminating')
            exit(0)

    def getTitle(self, label):
        
        if label == 0:
            title = 'apple'
        elif label == 1:
            title = 'ball'
        elif label == 2:
            title = 'banana'
        elif label == 3:
            title = 'bell_pepper'
        elif label == 4:
            title = 'binder'
        elif label == 5:
            title = 'bowl'
        elif label == 6:
            title = 'calculator'
        elif label == 7:
            title = 'camera'
        elif label == 8:
            title = 'cap'
        elif label == 9:
            title = 'cell_phone'
        elif label == 10:
            title = 'cereal_box'
        elif label == 11:
            title = 'coffee_mug'
        elif label == 12:
            title = 'comb'
        elif label == 13:
            title = 'dry_battery'
        elif label == 14:
            title = 'flashlight'
        elif label == 15:
            title = 'food_bag'
        elif label == 16:
            title = 'food_box'
        elif label == 17:
            title = 'food_can'
        elif label == 18:
            title = 'food_cup'
        elif label == 19:
            title = 'food_jar'
        elif label == 20:
            title = 'garlic'
        elif label == 21:
            title = 'glue_stick'
        elif label == 22:
            title = 'greens'
        elif label == 23:
            title = 'hand_towel'
        elif label == 24:
            title = 'instant_noodles'
        elif label == 25:
            title = 'keyboard'
        elif label == 26:
            title = 'kleenex'
        elif label == 27:
            title = 'lemon'
        elif label == 28:
            title = 'lightbulb'
        elif label == 29:
            title = 'lime'
        elif label == 30:
            title = 'marker'
        elif label == 31:
            title = 'mushroom'
        elif label == 32:
            title = 'notebook'
        elif label == 33:
            title = 'onion'
        elif label == 34:
            title = 'orange'
        elif label == 35:
            title = 'peach'
        elif label == 36:
            title = 'pear'
        elif label == 37:
            title = 'pitcher'
        elif label == 38:
            title = 'plate'
        elif label == 39:
            title = 'pliers'
        elif label == 40:
            title = 'potato'
        elif label == 41:
            title = 'rubber_eraser'
        elif label == 42:
            title = 'scissors'
        elif label == 43:
            title = 'shampoo'
        elif label == 44:
            title = 'soda_can'
        elif label == 45:
            title = 'sponge'
        elif label == 46:
            title = 'stapler'
        elif label == 47:
            title = 'tomato'
        elif label == 48:
            title = 'toothbrush'
        elif label == 49:
            title = 'toothpaste'
        elif label == 50:
            title = 'water_bottle'
        else:
            raise ValueError('Unknown class')
        
        return title  # Return correct title for the image