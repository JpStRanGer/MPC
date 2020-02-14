 import numpy as np
import matplotlib.pyplot as plt

import model
import MPC

start = 0
stop = 1000
dt = 0.1
ns = int((stop-start)/dt)+1
time = np.linspace(start,stop,ns)

SP = np.array([1 if t < 50 else
               1 for t in time])
U = SP#time * 0
Y = time * 0

# Define Objects
obj_processModel = model.secDegModel(dt)
obj_delay = model.timedelay(20,dt)

for k in range(len(time)):
    
    Y[k] = obj_processModel.run(U[k])

plt.figure()
plt.plot(time,SP)
plt.plot(time,Y)
plt.grid()
plt.show()