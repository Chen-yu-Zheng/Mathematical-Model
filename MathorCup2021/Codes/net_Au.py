import torch
from torch import nn

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()

        self.fc = nn.Sequential(
            nn.Linear(60, 128),
            nn.ReLU(inplace= True),
            nn.Dropout(),
            nn.Linear(128, 128),
            nn.ReLU(inplace= True),
            nn.Dropout(),
            nn.Linear(128,1)
        )
    
    def forward(self, x):
        out = self.fc(x)
        return out
    
