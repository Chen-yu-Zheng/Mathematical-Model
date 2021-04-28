import torch
from torch import nn

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(45 * 3, 256),
            nn.ReLU(inplace= True),
            nn.Linear(256, 256),
            nn.ReLU(inplace= True),
            nn.Linear(256, 256),
            nn.ReLU(inplace= True),
            nn.Linear(256, 256),
            nn.ReLU(inplace= True),
            nn.Linear(256,1)
        )
    
    def forward(self, x):
        out = self.fc(x)
        return out
    
