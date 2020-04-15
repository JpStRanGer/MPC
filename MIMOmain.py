import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import model
import mimoMPC
import pickle
import time as TIME
import uuid
import mimoFunctions

#####################
# TODO:
#  x Sende modeltilstanden fra simulatoren og helt ned til objective function
#  x Kopiere U_optimal --> U_guess slik at den begynner å lete der den slapp sist.
#  - Lage progress callback

randomPlotNumber = str(uuid.uuid1())

#%% TIME PARAMETRIZATION
start = 0
stop = 750 # minuts
dt = 1
ns = int((stop-start)/dt)+1
time = np.linspace(start,stop,ns)

# Definging SETPOINT
SP = np.array([15 if t < 100 else
               20 if t < 500 else
               25 for t in time])


#|||||||||||||||||||||||||||||||||||||||||#
#%%         Defining input arrays         #
#|||||||||||||||||||||||||||||||||||||||||#
###########################################

# DEFINING INPUT ARRAYS
U_PAX = time * 0
U_PIX = time * 0
U_POL = time * 0
# DEFINING OUTPUT ARRAYS
turb = time * 0

# SS/TURB input
U_SS = time * 0 + 2 * np.sin(2*np.pi*time/600) + 20

# FLOW input
U_flow = time * 0  + np.sin(2*np.pi*time/11) + 5

#%% MPC PARAMETERIZATION
prediction_horizion = 300
numberOfBlocks = 4
numberOfIntputs = 1
predTime = np.linspace(0,prediction_horizion,int(prediction_horizion/dt)+1)

#%% Define Objects
obj_processModel = model.mimoMODEL(dt,[turb[0],U_SS[0]])
obj_mpc = mimoMPC.mpc(dt = dt, numberOfIntputs = numberOfIntputs, pred_horizion_length = prediction_horizion, numberOfBlocks = numberOfBlocks)

#%% MAIN LOOP
tic = TIME.time()
for k in range(len(time)):
    U_opt = obj_mpc.run(SP,[turb[k],U_SS[k]])
    # U_PIX[k], U_PAX[k], U_POL[k] = U_opt
    U_PIX[k] = U_opt[0] # UNPACKING CONTROLVALUES FOR PIX FROM U_OPT
    turb[k], *_ = obj_processModel.run(u_pix = U_PIX[k], 
                                       u_pax = 0,
                                       u_pol = 0,
                                       u_ss = U_SS[k],
                                       u_flow = 0)
    
    # LOAD PREDICTED DATA FROM OPTIMALIZATIOR FOR PLOTING
    with open("predArray.data","rb") as datafile2:
        predTime, predTURB, predSP, predPIX, predSS, predError, avgError = pickle.load(datafile2)
   
    # CALCULATE EXECUTION TIME FROM START
    toc = TIME.time()
    realexeTime = round(toc - tic,0)
    minutsAndSeconds = divmod(realexeTime,60)
    minuts = minutsAndSeconds[0]
    seconds = minutsAndSeconds[1]
    
    #%% START REALTIME PLOTTING
    plt.figure(1)
    plt.title("From MAIN (K:{}, Time: {:0.2f} (min?)\nReal execution time: {:02.0f}m:{:02.0f}s\nturb[k]: {:0.2}, U_PIX[k]: {:0.3}\nPrediction horizion:{}min, N.Blocks: {} )".format(k, time[k], *minutsAndSeconds, turb[k], U_PIX[k],prediction_horizion, numberOfBlocks))
    
    plt.plot(time[:k],U_PIX[:k],label="controler PIX")
    plt.plot(time[:],SP[:],label="Setpunkt Turb")
    plt.plot(time[:k],turb[:k],label="Turb (REAL)")
    plt.plot(time[:k],U_SS[:k],label="REAL SS inn")
    
    plt.plot(predTime + time[k], predPIX, '--', label="Predictied PIX")
    plt.plot(predTime + time[k], predSS, '--', label="Predicted SS")
    plt.plot(predTime + time[k], predSP, '--', label="Predicted SP")
    plt.plot(predTime + time[k], predTURB, '--', label="Predicted Turb")
    
    plt.legend()
    plt.grid()
    plt.savefig('plot/REAL-plott '+randomPlotNumber)
    plt.show()
    
    # ax[1].grid()
    print("U_PIX[k]:",U_PIX[k]," k:",k," time:",int(k*dt))
    