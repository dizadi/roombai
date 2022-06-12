
import torch
from torch import nn

import torch.nn.functional as F
import math

def weight_init(layers):
    for layer in layers:
        torch.nn.init.kaiming_normal_(layer.weight, nonlinearity='relu')

def reward(distance_traveled, rotation_traveled, sensor_data):
    # reward for moving around more without sensors getting hit
    # reward negative big time for sensors being hit
    pass

class DDQNAgent(nn.Module):
    def __init__(self, state_space, action_space):
        super().__init__(self)
        self._state_space = state_space
        self._action_space = action_space
      
        self.cnn_1 = nn.Conv2d(4, out_channels=32, kernel_size=8, stride=4)
        self.cnn_2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=4, stride=2)
        self.cnn_3 = nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3, stride=1)
        weight_init([self.cnn_1, self.cnn_2, self.cnn_3])

        self.ff_1 = nn.Linear(self.calc_input_layer(), layer_size)
        self.ff_2 = nn.Linear(layer_size, action_size)
        weight_init([self.ff_1])


    def calc_input_layer(self):
        x = torch.zeros(self.input_shape).unsqueeze(0)
        x = self.cnn_1(x)
        x = self.cnn_2(x)
        x = self.cnn_3(x)
        return x.flatten().shape[0]
    
    def forward(self, input):
        """
        
        """
        x = torch.relu(self.cnn_1(input))
        x = torch.relu(self.cnn_2(x))
        x = torch.relu(self.cnn_3(x))
        x = x.view(input.size(0), -1)

        x = torch.relu(self.ff_1(x))
        out = self.ff_2(x)
        
        return out
