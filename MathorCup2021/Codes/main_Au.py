import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 

import torch
from torch import nn
from torch import optim
from torch.utils.data import DataLoader
from torch.utils.data import Dataset
from torch.utils.data import TensorDataset

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

import config
from net import Net

X = pd.read_csv('Au20.csv')
Y = pd.read_csv('AuE.csv')

MAX_X, MAX_Y, MAX_Z = X.max(axis = 0)
MIN_X, MIN_Y, MIN_Z = X.min(axis = 0)
print(MAX_X,MAX_Y,MAX_Z)
print(MIN_X,MIN_Y,MIN_Z)

standard = StandardScaler()
standard2 = StandardScaler()
standard.fit(X)
X = standard.transform(X)
standard2.fit(Y)
Y = standard2.transform(Y)

X = X.reshape((998, -1))

X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size = config.TEST_SIZE, random_state = config.RANDOM_SEED)
print(X_train.shape)
print(Y_train.shape)

X_train = torch.from_numpy(X_train)
X_test = torch.from_numpy(X_test)
Y_train = torch.from_numpy(Y_train)
Y_test = torch.from_numpy(Y_test)

device = 'cuda' if torch.cuda.is_available() else 'cpu'
dataset_train = TensorDataset(X_train, Y_train)

train_iter = DataLoader(dataset_train, batch_size= config.BATCH_SIZE, shuffle= True)

net = Net()
net.to(device)
print(net)

loss_func = nn.MSELoss()
optimizer = optim.SGD(net.parameters(), lr= config.LR, weight_decay= config.WD)
scheduler = optim.lr_scheduler.StepLR(optimizer,step_size=100,gamma = 0.8)

net.train()
step_loss_history = []
epoch_loss_history = []
for epoch in range(config.EPOCH_NUM):
    epoch_loss = 0
    for step,(batch_x, batch_y) in enumerate(train_iter):
        batch_x = batch_x.float().to(device)
        batch_y = batch_y.float().to(device)
        out = net(batch_x)
        step_loss = loss_func(out, batch_y)
        epoch_loss += step_loss.item()
        step_loss_history.append(step_loss.item() / config.BATCH_SIZE)
        
        #if (step + 1) % 1 == 0:
            #print('epoch: %d, step: %d, step_loss: %f' %(epoch + 1, step + 1, step_loss.item()))
        optimizer.zero_grad()
        step_loss.backward()
        optimizer.step()
  
    scheduler.step()
    epoch_loss /= len(dataset_train)
    epoch_loss_history.append(epoch_loss)
    if (epoch + 1) % config.STEP == 0:
        print('epoch: %d, epoch_loss: %f' %(epoch + 1, epoch_loss))



torch.save(net, 'result/net4.pkl')
np.save('result/step_loss_history.npy', step_loss_history)
np.save('result/epoch_loss_history.npy', epoch_loss_history)


dataset_test = TensorDataset(X_test, Y_test)
test_iter = DataLoader(dataset_test, batch_size= config.BATCH_SIZE, shuffle= False)

net.eval()
for step,(batch_x, batch_y) in enumerate(test_iter):
    batch_x = batch_x.float().to(device)
    batch_y = batch_y.float().to(device)
    out = net(batch_x)
    step_loss = loss_func(out, batch_y)
    epoch_loss += step_loss.item()
    step_loss_history.append(step_loss.item() / config.BATCH_SIZE)
    print('step: %d, step_loss: %f' %(step + 1, step_loss.item() / config.BATCH_SIZE))
        
epoch_loss /= len(dataset_test)
print('test_loss: %f' %(epoch_loss))