import torch
import numpy as np 
from net import Net
import config
import sys
import matplotlib.pyplot as plt

def getaff(xyz, net):
    means = np.array([config.MEAN_X, config.MEAN_Y, config.MEAN_Z]).reshape((1,-1))
    stds = np.array([config.STD_X, config.STD_Y, config.STD_Z]).reshape((1,-1))

    xyz = xyz.reshape((xyz.shape[0],-1,3))
    xyz = (xyz - means) / stds
    xyz = torch.from_numpy(xyz).float()
    E = np.zeros((xyz.shape[0], 1))

    for j in range(xyz.shape[0]):
        e = 0
        for i in range(13):
            atom = xyz[j]
            atom_slice = atom[i : i + 20]
            e += net(atom_slice.view(1,-1)).item()
        e /= 13
        E[j] = e 
    return -E

def getden(group):
    density = np.zeros((group.shape[0], 1))
    for i in range(group.shape[0]):
        d = np.zeros((group.shape[0], 1))
        for j in range(group.shape[0]):
            d[j] = np.sqrt(np.sum((group[i] - group[j]) ** 2))
            if d[j] < config.detas:
                d[j] = 1
            else:
                d[j] = 0
        density[i] = np.sum(d) / group.shape[0]

    return density

def main():
    device = 'cpu'
    net = torch.load('result/net_Au.pkl')
    net.to(device)
    net.eval()

    maxs = np.array([config.MAX_X, config.MAX_Y, config.MAX_Z]).reshape((1,-1))
    mins = np.array([config.MIN_X, config.MIN_Y, config.MIN_Z]).reshape((1,-1))
    dxyz = maxs - mins
    group = np.random.rand(config.NP, config.Dim).reshape((config.NP, -1, 3))
    '''
    print(means)
    print(stds)
    print(dxyz)
    print(mins)
    '''
    group = np.random.rand(config.NP, config.Dim).reshape((config.NP,-1,3)) * dxyz + mins
    group = group.reshape(config.NP, -1)
    affinity = getaff(group, net)
    #print(affinity)
    density = getden(group)
    #print(density)
    sim = config.alpha * affinity - config.beta * density
    index_sort = np.argsort(sim, axis= 0)[::-1].squeeze()
    group_sort = group[index_sort]
    #print(group_sort)

    history = []
    for gen in range(1, config.G + 1):
        deta_x = config.Deta_X / gen
        deta_y = config.Deta_Y / gen
        deta_z = config.Deta_Z / gen

        group_select = np.zeros((int(config.NP / 2), config.Dim))
        aff_select = np.zeros((int(config.NP / 2), 1))
        den_select = np.zeros((int(config.NP / 2), 1))
        sim_select = np.zeros((int(config.NP / 2), 1))

        group_new = np.zeros((int(config.NP / 2), config.Dim))
        aff_new = np.zeros((int(config.NP / 2), 1))
        den_new = np.zeros((int(config.NP / 2), 1))
        sim_new = np.zeros((int(config.NP / 2), 1))

        for i in range(int(config.NP / 2)):
            antibody = group_sort[i].reshape(1,-1)
            antibody_cloned = np.repeat(antibody, config.N_CLONE, axis= 0)
            #print(antibody_cloned.shape)

            for j in range(1, config.N_CLONE):
                for dim in range(config.Dim):
                    if np.random.rand() < config.P_Var:
                        if (dim + 1) % 3 == 1:
                            antibody_cloned[j][dim] += (np.random.rand() - 0.5) * deta_x
                            if antibody_cloned[j][dim] < config.MIN_X or antibody_cloned[j][dim] > config.MAX_X:
                                antibody_cloned[j][dim] = config.MIN_X + np.random.rand() * (config.MAX_X - config.MIN_X)

                        elif (dim + 1) % 3 == 2:
                            antibody_cloned[j][dim] += (np.random.rand() - 0.5) * deta_y
                            if antibody_cloned[j][dim] < config.MIN_Y or antibody_cloned[j][dim] > config.MAX_Y:
                                antibody_cloned[j][dim] = config.MIN_Y + np.random.rand() * (config.MAX_X - config.MIN_Y)

                        else:
                            antibody_cloned[j][dim] += (np.random.rand() - 0.5) * deta_z
                            if antibody_cloned[j][dim] < config.MIN_Z or antibody_cloned[j][dim] > config.MAX_Z:
                                antibody_cloned[j][dim] = config.MIN_Z + np.random.rand() * (config.MAX_Z - config.MIN_Z)

            aff_clone = getaff(antibody_cloned, net)
            argmax_aff_clone = np.argmax(aff_clone, axis= 0)
            aff_select[i][0] = np.max(aff_clone, axis= 0)
            group_select[i] = antibody_cloned[argmax_aff_clone]
            #print(aff_clone)
            #print(aff_select[0])

        den_select = getden(group_select)
        sim_select = config.alpha * aff_select - config.beta * den_select
        #print(sim_select.shape)

        group_new = np.random.rand(int(config.NP/2), config.Dim).reshape((int(config.NP/2),-1,3)) * dxyz + mins
        group_new = group_new.reshape(int(config.NP/2), -1)
        aff_new = getaff(group_new, net)
        den_new = getden(group_new)
        sim_new = config.alpha * aff_new - config.beta * den_new
        #print(sim_new.shape)
        #print(group_select.shape)
        #print(group_new.shape)

        group = np.vstack((group_select, group_new))
        sim = np.vstack((sim_select, sim_new))
        index_sort = np.argsort(sim, axis= 0)[::-1].squeeze()
        group_sort = group[index_sort]
        history.append(-1 * getaff(group_sort[0].reshape(1,-1), net)[0][0] * config.STD_E + config.MEAN_E)

        if (gen + 1) % 20 == 0:
            print(history[gen-1])
    
    best = group_sort[0]
    np.save('result/best_Au.npy', best)
    history = np.array(history)
    np.save('result/history.npy', history)

    plt.figure()
    plt.xlabel('epoch')
    plt.ylabel('minE')
    plt.plot(history)
    plt.show()

if __name__ == '__main__':
    main()