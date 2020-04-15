import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import model
import mimoMPC

#####################
# TODO:
#  x Sende modeltilstanden fra simulatoren og helt ned til objective function
#  x Kopiere U_optimal --> U_guess slik at den begynner å lete der den slapp sist.
#  - Lage progress callback



#%% TIME PARAMETRIZATION
start = 0
stop = 2000
dt = 0.1
ns = int((stop-start)/dt)+1
time = np.linspace(start,stop,ns)

# Definging SETPOINT
SP = np.array([15 if t < 500 else
               20 for t in time])

U = time * 0
turb = time * 0

prediction_horizion = 200
predTime = np.linspace(0,prediction_horizion,int(prediction_horizion/dt)+1)

# Define Objects
obj_processModel = model.secDegModel(dt)
obj_mpc = mimoMPC.mpc(dt = dt, pred_horizion_length = prediction_horizion)

#%% MAIN LOOP
for k in range(len(time)):
    u_k = obj_mpc.u_opt[0]
    U[k] = u_k
    turb[k] = obj_processModel.run(u_k)
    obj_mpc.run(SP[k],turb[k])
    
    plt.figure(1)
    plt.title("From MAIN")
    plt.plot(time[:k],U[:k],label="controler output")
    plt.plot(time[:],SP[:],label="Setpunkt Turb")
    
    plt.plot(time[:k],turb[:k],label="Turb (REAL)")
    plt.legend()
    plt.grid()
    plt.show()
    print("u_k:",u_k," k:",k," time:",int(k*dt))
    