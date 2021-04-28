import numpy as np
import pandas as pd
Au20 = np.load('result/best_B45.npy')
Au20 = Au20.reshape(45,3)
Au20 = pd.DataFrame(Au20, columns= ['x', 'y', 'z'])
Au20.to_csv('best_B45_xyz.csv')