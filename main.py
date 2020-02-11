import numpy as np
import matplotlib.pyplot as plt

import model
import MPC

start = 0
stop = 100
dt = 0.1
ns = int((stop-start)/dt)+1
time = np.linspace(start,stop,ns)
sin = time * 0 + np.sin(time)
U = np.array([1 if t < 50 else
              1 for t in time])
Y = np.zeros(len(time))

# Define Objects
obj_processModel = model.secDegModel(dt)
obj_delay = model.timedelay(20,dt)

for k in range(len(time)):
    #Y[k] = obj_delay.run(U[k])
    Y[k] = obj_processModel.run(U[k])


plt.plot(time,U)
plt.plot(time,Y)
#plt.plot(time,sin)
