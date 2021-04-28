import numpy as np 
import matplotlib.pyplot as plt


step_loss_history = np.load('result/step_B.npy')
epoch_loss_history = np.load('result/epoch_B.npy')

history = np.load('result/history_Au20.npy')


plt.figure()
plt.plot(np.array(step_loss_history))
plt.xlabel('step')
plt.ylabel('loss')
plt.show()

plt.figure()
plt.plot(np.array(epoch_loss_history))
plt.xlabel('epoch')
plt.ylabel('loss')
plt.show()


plt.figure()
plt.plot(np.array(history))
plt.xlabel('gen')
plt.ylabel('min Energy')
plt.show()