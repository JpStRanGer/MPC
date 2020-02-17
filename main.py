import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import model
import MPC

#####################
# TODO:
#  x Sende modeltilstanden fra simulatoren og helt ned til objective function
#  x Kopiere U_optimal --> U_guess slik at den begynner å lete der den slapp sist.
#  - Lage progress callback




start = 0
stop = 1000
dt = 0.1
ns = int((stop-start)/dt)+1
time = np.linspace(start,stop,ns)
SP = np.array([1 if t < 50 else
               1 for t in time])

U = SP#time * 0
turb = time * 0

# Define Objects
obj_processModel = model.secDegModel(dt)
obj_mpc = MPC.mpc(dt = dt, pred_horizion_length = 400, NumberOfBlocks = 3)

#print(obj_mpc.u_opt)
#obj_mpc.run(30)
#print(obj_mpc.u_opt)
#obj_mpc.run(2)
#print(obj_mpc.u_opt)

for k in range(len(time)):
    u_k = obj_mpc.u_opt
    turb[k] = obj_processModel.run(u_k)
    obj_mpc.run(SP[k],turb[k])
    
    plt.figure(1)
    #plt.plot(time,SP,label="Setpunkt Turb")
    
    plt.plot(time,turb,label="Turb (REAL)")
    plt.legend()
    plt.grid()
    plt.show()
#    print(obj_mpc.u_opt)
    print("u_k:",u_k," k:",k," time:",int(k/dt))
    
#    obj_mpc.run(turb[k])