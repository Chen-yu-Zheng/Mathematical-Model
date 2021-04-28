import torch
import numpy as np 
from net_Au import Net
import configB
import sys
import matplotlib.pyplot as plt

def getaff(xyz, net):
    means = np.array([configB.MEAN_X, configB.MEAN_Y, configB.MEAN_Z]).reshape((1,-1))
    stds = np.array([configB.STD_X, configB.STD_Y, configB.STD_Z]).reshape((1,-1))

    xyz = xyz.reshape((xyz.shape[0],-1,3))
    xyz = (xyz - means) / stds
    xyz = torch.from_numpy(xyz).float()
    E = np.zeros((xyz.shape[0], 1))

    for j in range(xyz.shape[0]):
        atom = xyz[j]
        E[j] = net(atom.view(1,-1)).item()
    return -E

def getden(group):
    density = np.zeros((group.shape[0], 1))
    for i in range(group.shape[0]):
        d = np.zeros((group.shape[0], 1))
        for j in range(group.shape[0]):
            d[j] = np.sqrt(np.sum((group[i] - group[j]) ** 2))
            if d[j] < configB.detas:
                d[j] = 1
            else:
                d[j] = 0
        density[i] = np.sum(d) / group.shape[0]

    return density

def main():
    device = 'cpu'
    net = torch.load('result/net_B.pkl')
    net.to(device)
    net.eval()

    maxs = np.array([configB.MAX_X, configB.MAX_Y, configB.MAX_Z]).reshape((1,-1))
    mins = np.array([configB.MIN_X, configB.MIN_Y, configB.MIN_Z]).reshape((1,-1))
    dxyz = maxs - mins
    group = np.random.rand(configB.NP, configB.Dim).reshape((configB.NP, -1, 3))
    '''
    print(means)
    print(stds)
    print(dxyz)
    print(mins)
    '''
    group = np.random.rand(configB.NP, configB.Dim).reshape((configB.NP,-1,3)) * dxyz + mins
    group = group.reshape(configB.NP, -1)
    affinity = getaff(group, net)
    #print(affinity)
    density = getden(group)
    #print(density)
    sim = configB.alpha * affinity - configB.beta * density
    index_sort = np.argsort(sim, axis= 0)[::-1].squeeze()
    group_sort = group[index_sort]
    #print(group_sort)

    history = []
    for gen in range(1, configB.G + 1):
        deta_x = configB.Deta_X / gen
        deta_y = configB.Deta_Y / gen
        deta_z = configB.Deta_Z / gen

        group_select = np.zeros((int(configB.NP / 2), configB.Dim))
        aff_select = np.zeros((int(configB.NP / 2), 1))
        den_select = np.zeros((int(configB.NP / 2), 1))
        sim_select = np.zeros((int(configB.NP / 2), 1))

        group_new = np.zeros((int(configB.NP / 2), configB.Dim))
        aff_new = np.zeros((int(configB.NP / 2), 1))
        den_new = np.zeros((int(configB.NP / 2), 1))
        sim_new = np.zeros((int(configB.NP / 2), 1))

        for i in range(int(configB.NP / 2)):
            antibody = group_sort[i].reshape(1,-1)
            antibody_cloned = np.repeat(antibody, configB.N_CLONE, axis= 0)
            #print(antibody_cloned.shape)

            for j in range(1, configB.N_CLONE):
                for dim in range(configB.Dim):
                    if np.random.rand() < configB.P_Var:
                        if (dim + 1) % 3 == 1:
                            antibody_cloned[j][dim] += (np.random.rand() - 0.5) * deta_x
                            if antibody_cloned[j][dim] < configB.MIN_X or antibody_cloned[j][dim] > configB.MAX_X:
                                antibody_cloned[j][dim] = configB.MIN_X + np.random.rand() * (configB.MAX_X - configB.MIN_X)

                        elif (dim + 1) % 3 == 2:
                            antibody_cloned[j][dim] += (np.random.rand() - 0.5) * deta_y
                            if antibody_cloned[j][dim] < configB.MIN_Y or antibody_cloned[j][dim] > configB.MAX_Y:
                                antibody_cloned[j][dim] = configB.MIN_Y + np.random.rand() * (configB.MAX_X - configB.MIN_Y)

                        else:
                            antibody_cloned[j][dim] += (np.random.rand() - 0.5) * deta_z
                            if antibody_cloned[j][dim] < configB.MIN_Z or antibody_cloned[j][dim] > configB.MAX_Z:
                                antibody_cloned[j][dim] = configB.MIN_Z + np.random.rand() * (configB.MAX_Z - configB.MIN_Z)

            aff_clone = getaff(antibody_cloned, net)
            argmax_aff_clone = np.argmax(aff_clone, axis= 0)
            aff_select[i][0] = np.max(aff_clone, axis= 0)
            group_select[i] = antibody_cloned[argmax_aff_clone]
            #print(aff_clone)
            #print(aff_select[0])

        den_select = getden(group_select)
        sim_select = configB.alpha * aff_select - configB.beta * den_select
        #print(sim_select.shape)

        group_new = np.random.rand(int(configB.NP/2), configB.Dim).reshape((int(configB.NP/2),-1,3)) * dxyz + mins
        group_new = group_new.reshape(int(configB.NP/2), -1)
        aff_new = getaff(group_new, net)
        den_new = getden(group_new)
        sim_new = configB.alpha * aff_new - configB.beta * den_new
        #print(sim_new.shape)
        #print(group_select.shape)
        #print(group_new.shape)

        group = np.vstack((group_select, group_new))
        sim = np.vstack((sim_select, sim_new))
        index_sort = np.argsort(sim, axis= 0)[::-1].squeeze()
        group_sort = group[index_sort]
        history.append(-1 * getaff(group_sort[0].reshape(1,-1), net)[0][0] * configB.STD_E + configB.MEAN_E)

        if (gen + 1) % 20 == 0:
            print(history[gen-1])
    
    best = group_sort[0]
    np.save('result/best_B45.npy', best)
    history = np.array(history)
    np.save('result/history_B45.npy', history)

    plt.figure()
    plt.xlabel('epoch')
    plt.ylabel('minE')
    plt.plot(history)
    plt.show()

if __name__ == '__main__':
    main()