## TODO: define the convolutional neural network architecture

import torch
import torch.nn as nn
import torch.nn.functional as F
# can use the below import should you choose to initialize the weights of your Net
import torch.nn.init as I


class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        
        ## TODO: Define all the layers of this CNN, the only requirements are:
        ## 1. This network takes in a square (same width and height), grayscale image as input
        ## 2. It ends with a linear layer that represents the keypoints
        ## it's suggested that you make this last layer output 136 values, 2 for each of the 68 keypoint (x, y) pairs
        
        # As an example, you've been given a convolutional layer, which you may (but don't have to) change:
        # 1 input image channel (grayscale), 32 output channels/feature maps, 5x5 square convolution kernel
        self.conv1 = nn.Conv2d(1, 32, 5)
        
        # output size = (w-f)/s +1 = (224-5)/1 + 1 = 220
        
        self.pool = nn.MaxPool2d(2,2) # 220/2 = 110
        
        # output for one tensor image = (32, 110, 110)
        
        # Second Conv layer: (32, 64, 3)
        self.conv2 = nn.Conv2d(32, 64, 3)
        
        # output size = (W-f)/S + 1 = (110-3)/1 + 1 = 108
        
        self.pool2 = nn.MaxPool2d(2,2) # 108/2 = 54
        # output Tensor for one image = (64, 54, 54)
        
        # Third Conv layer: (64, 128, 3)
        self.conv3 = nn.Conv2d(64, 128, 3)
        
        # output size = (54-3)/1 +1 = 52
        self.pool3 = nn.MaxPool2d(2,2) # 52 / 2 = 26
        #output Tensor for one image = (128, 26, 26)
        
        # Fourth Conv layer (128, 256, 3)
        self.conv4 = nn.Conv2d(128, 256, 3)
        
        # output size = (26-3)/1 +1 = 24
        self.pool4 = nn.MaxPool2d(2,2) # 24/2 = 12
        #output Tensor for one image = (256, 12, 12)
        
        # Fifth conv layer (256, 512, 1)
        self.conv5 = nn.Conv2d(256, 512, 1)
        
        #output size = (W-F)/S +1 = (12-1)/1 +1 = 12
        self.pool5 = nn.MaxPool2d(2,2) # 12/2
        # output Tensor for one image = (512, 6, 6)
        
        # Fully Connected Layers
        self.fc1 = nn.Linear(512*6*6, 1024)
        self.fc2 = nn.Linear(1024, 136)  # 136 keypoints , which is 68 keypoints each for (x, y)
        
        
        ## Note that among the layers to add, consider including:
        # maxpooling layers, multiple conv layers, fully-connected layers, and other layers (such as dropout or batch normalization) to avoid overfitting
        self.drop1 = nn.Dropout(p = 0.10)
        self.drop2 = nn.Dropout(p = 0.20)
        self.drop3 = nn.Dropout(p = 0.25)
        self.drop4 = nn.Dropout(p = 0.28)
        self.drop5 = nn.Dropout(p = 0.30)
        self.drop6 = nn.Dropout(p = 0.45)

        
    def forward(self, x):
        ## TODO: Define the feedforward behavior of this model
        ## x is the input image and, as an example, here you may choose to include a pool/conv step:
        ## x = self.pool(F.relu(self.conv1(x)))
        
        x = self.pool(F.relu(self.conv1(x)))
        x = self.drop1(x)
        x = self.pool2(F.relu(self.conv2(x)))
        x = self.drop2(x)
        x = self.pool3(F.relu(self.conv3(x)))
        x = self.drop3(x)
        x = self.pool4(F.relu(self.conv4(x)))
        x = self.drop4(x)
        x = self.pool5(F.relu(self.conv5(x)))
        x = self.drop5(x)
        
        # flatten input vectors
        x = x.view(x.size(0), -1)
        x = self.drop6(F.relu(self.fc1(x)))
        x = self.fc2(x)
        
        # a modified x, having gone through all the layers of your model, should be returned
        return x
