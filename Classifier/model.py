#!/usr/bin/env python3


#-----------------
# Imports
#-----------------
from torch import nn


class Model(nn.Module):

    def __init__(self):

        super().__init__()

        # bx3x224x224 input images
        self.layer1 = nn.Sequential(
            # 3 input channels, 16 output depth, padding and stride
            nn.Conv2d(3,16,kernel_size=3, padding=0,stride=2),
            # normalizes the batch data setting the average to 0 and std to 1
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.MaxPool2d(2) # similar to image pyrdown, reduces size
        )

        self.layer2 = nn.Sequential(
            nn.Conv2d(16,32, kernel_size=3, padding=0, stride=2),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2)
            )
        
        self.layer3 = nn.Sequential(
            nn.Conv2d(32,64, kernel_size=3, padding=0, stride=2),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )
        
        self.fc1 = nn.Linear(3*3*64,10)
        self.dropout = nn.Dropout(0.5)
        self.fc2 = nn.Linear(10,51)
        self.relu = nn.ReLU()

    def forward(self,x):
        
        out = self.layer1(x)
        out = self.layer2(out)
        out = self.layer3(out)
        out = out.view(out.size(0),-1) # flatten to keep batch dimension and compact all others into the second dimension
        out = self.relu(self.fc1(out))
        out = self.fc2(out)

        return out