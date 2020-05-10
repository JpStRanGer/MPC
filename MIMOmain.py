import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import model
import mimoMPC
import pickle
import time as TIME
import uuid
import mimoFunctions
import modelparameters

video = True
PlotNumber = 0

#####################
# TODO:
#  x Sende modeltilstanden fra simulatoren og helt ned til objective function
#  x Kopiere U_optimal --> U_guess slik at den begynner å lete der den slapp sist.
#  - Lage progress callback

UniqPlotId = str(uuid.uuid1())


#%% TIME PARAMETRIZATION
start = 0
stop = 800 # minuts
dt = 10
ns = int((stop-start)/dt)+1
time = np.linspace(start,stop,ns)

# Definging SETPOINT
SP = np.array([10 if t < 100 else
               15 if t < 600 else
               6 for t in time])


#|||||||||||||||||||||||||||||||||||||||||#
#%%         Defining input arrays         #
#|||||||||||||||||||||||||||||||||||||||||#
###########################################

# =============================================================================
# # DEFINING INPUT ARRAYS
# =============================================================================
U_PIX = time * 0
U_PAX = time * 0
U_POL = time * 0

# =============================================================================
# # SS/TURB input
# =============================================================================
U_SS = time * 0 + 2 * np.sin(2*np.pi*time/1440) + 20

# =============================================================================
# # FLOW input
# =============================================================================
U_flow = time * 0  + np.sin(2*np.pi*time/11) + 5

# =============================================================================
# # DEFINING INITIAL VALUES
# =============================================================================
U_turb_PIX_INITIAL = [0,0]
U_turb_PAX_INITIAL = [0,0]
U_turb_POL_INITIAL = [0,0]
TurbModelStates = [U_turb_PIX_INITIAL, U_turb_PAX_INITIAL, U_turb_POL_INITIAL, U_SS[0]]

U_alkalinity_PIX_INITIAL = [0,0]
U_alkalinity_PAX_INITIAL = [0,0]
U_alkalinity_POL_INITIAL = [0,0]
alkalinityModelStates = [U_turb_PIX_INITIAL, U_turb_PAX_INITIAL, U_turb_POL_INITIAL, U_SS[0]]

U_phosphate_PIX_INITIAL = [3,3]
U_phosphate_PAX_INITIAL = [3,3]
U_phosphate_POL_INITIAL = [0,0]
phosphateModelStates = [U_turb_PIX_INITIAL, U_turb_PAX_INITIAL, U_turb_POL_INITIAL, U_SS[0]]

modelStates = {'turb':TurbModelStates, 'alkalinity':alkalinityModelStates, 'phosphate':phosphateModelStates}

# DEFINING OUTPUT ARRAYS
turb = time * 0
alkalinity = time * 0
phosphate = time * 0
phosphate_SP = time *0 + 0.6


#%% MPC PARAMETERIZATION
prediction_horizion = 150
numberOfBlocks = 3
numberOfIntputs = 3
predTime = np.linspace(0,prediction_horizion,int(prediction_horizion/dt)+1)

#%% Define Objects
#obj_processModel = model.mimoMODEL(dt, TurbModelStates, turbParrameters)
obj_processModel = model.mimoMODEL(dt, TurbModelStates, modelparameters.turbParrameters)
obj_alkalinityModel = model.mimoMODEL(dt, alkalinityModelStates, modelparameters.AlkalinityParrameters)
obj_phosphateModel = model.mimoMODEL(dt, phosphateModelStates, modelparameters.phosphateParrameters)
obj_mpc = mimoMPC.mpc(dt = dt, numberOfIntputs = numberOfIntputs, pred_horizion_length = prediction_horizion, numberOfBlocks = numberOfBlocks)

#%% MAIN LOOP
tic = TIME.time()
for k in range(len(time)-1):
    
    if video == True : PlotNumber += 1
    
    
    # controlsignals = [U_PIX[k], U_PAX[k], U_POL[k], U_SS[k]]
    controlsignals = [U_PIX[k], U_PAX[k], U_POL[k], U_SS[k:]]
#    print('from MAIN modelStates',modelStates)
    U_opt = obj_mpc.run(SP[k:], controlsignals, modelStates )
    # U_PIX[k], U_PAX[k], U_POL[k] = U_opt
    U_PIX[k] = U_opt[0] # UNPACKING CONTROLVALUES FOR PIX FROM U_OPT
    U_PAX[k] = U_opt[1] if len(U_opt) >=2 else None # UNPACKING CONTROLVALUES FOR PAX FROM U_OPT
    U_POL[k] = U_opt[2] if len(U_opt) >=3 else None # UNPACKING CONTROLVALUES FOR POL FROM U_OPT
    turb[k], *_ = obj_processModel.run(u_pix = U_PIX[k], 
                                       u_pax = U_PAX[k],
                                       u_pol = U_POL[k],
                                       u_ss = U_SS[k],
                                       u_flow = 0
                                       )
    alkalinity[k], *_ = obj_alkalinityModel.run(u_pix = U_PIX[k], 
                                                u_pax = U_PAX[k],
                                                u_pol = U_POL[k],
                                                u_ss = U_SS[k],
                                                u_flow = 0
                                       )
    phosphate[k], *_ = obj_phosphateModel.run(u_pix = U_PIX[k], 
                                              u_pax = U_PAX[k],
                                              u_pol = U_POL[k],
                                              u_ss = U_SS[k],
                                              u_flow = 0
                                       )
    modelStates = {'turb':obj_processModel.returnStates(), 'alkalinity':obj_alkalinityModel.returnStates(), 'phosphate':obj_phosphateModel.returnStates()}
    
    # LOAD PREDICTED DATA FROM OPTIMALIZATIOR FOR PLOTING
    with open("predArray.data","rb") as datafile2:
        predTime, predTURB, predTURB_SP, predALKALINITY, predPHOSPATE, predPHOSPATE_SP, predPIX, predPAX, predPOL, predSS, predError, avgError = pickle.load(datafile2)
   
    # CALCULATE EXECUTION TIME FROM START
    toc = TIME.time()
    realexeTime = round(toc - tic,0)
    minutsAndSeconds = divmod(realexeTime,60)
    minuts, seconds = minutsAndSeconds
    
    #%% START REALTIME PLOTTING
    title = "Run from MAIN (K:{}, Time: {:0.2f} (min?)".format(k, time[k])
    title += " \n Real execution time: {:02.0f}m:{:02.0f}s".format(*minutsAndSeconds)
    # plt.figure(1,figsize=[10,6])
    # title += " - Pred hori.:{}min, N.Blocks: {} )".format(prediction_horizion, numberOfBlocks)
    # title += "\nturb[k]: {:0.2}, U_PIX[k]: {:0.3}\nPrediction horizion:{}min, N.Blocks: {} )".format(turb[k], U_PIX[k],prediction_horizion, numberOfBlocks)
#    plt.title(title)
#    # plt.title("From MAIN (K:{}, Time: {:0.2f} (min?)\nReal execution time: {:02.0f}m:{:02.0f}s\nturb[k]: {:0.2}, U_PIX[k]: {:0.3}\nPrediction horizion:{}min, N.Blocks: {} )".format(k, time[k], *minutsAndSeconds, turb[k], U_PIX[k],prediction_horizion, numberOfBlocks))
#    
#    plt.plot(time[:k+1], U_PIX[:k+1], 'C0', label="controler PIX")
#    plt.plot(time[:k+1], U_PAX[:k+1], 'C4', label="controler PAX")
#    plt.plot(time[:k+1], U_POL[:k+1], 'C5', label="controler POL")
#    plt.plot(time[:], SP[:], 'C1', label="Setpunkt Turb")
#    plt.plot(time[:k+1], turb[:k+1], 'C2', label="Turb (REAL)")
#    plt.plot(time[:k+1], U_SS[:k+1], 'C3', label="REAL SS inn")
#    plt.plot(time[:k+1], alkalinity[:k+1], 'C6', label="alkalinity")
#    plt.plot(time[:k+1], phosphate[:k+1], 'C7', label="phosphate")
#    plt.plot(time[:k+1], phosphate_SP[:k+1], 'C8', label="Phosphate SP")
#    
#    if k*dt < time[-1]-predTime[-1]:
#        plt.plot(predTime + time[k], predPIX, 'C0--')#, label="Predictied PIX")
#        plt.plot(predTime + time[k], predPAX, 'C4--')#, label="Predictied PAX")
#        plt.plot(predTime + time[k], predPOL, 'C5--')#, label="Predictied POL")
#        plt.plot(predTime + time[k], predTURB_SP, 'C5--')#, label="Predicted Turb SP")
#        plt.plot(predTime + time[k], predTURB, 'C2--')#, label="Predicted Turb")
#        plt.plot(predTime + time[k], predSS, 'C3--')#, label="Predicted SS")
#        plt.plot(predTime + time[k], predALKALINITY, 'C6--')#, label="Pred alkalinity")
#        plt.plot(predTime + time[k], predPHOSPATE, 'C7--')#, label="Pred Phosphate")
#        plt.plot(predTime + time[k], predPHOSPATE_SP, 'C8--')#, label="Pred Phosphate SP")
#    else:
#        predTime = predTime[:(len(time)-k)]
#        plt.plot(predTime + time[k], predPIX[:len(predTime)] , 'C0--')#, label="Predictied PIX")
#        plt.plot(predTime + time[k], predPAX[:len(predTime)] , 'C4--')#, label="Predictied PAX")
#        plt.plot(predTime + time[k], predPOL[:len(predTime)] , 'C5--')#, label="Predictied POL")
#        plt.plot(predTime + time[k], predTURB_SP[:len(predTime)] , 'C5--')#, label="Predicted Turb SP")
#        plt.plot(predTime + time[k], predTURB[:len(predTime)] , 'C2--')#, label="Predicted Turb")
#        plt.plot(predTime + time[k], predSS[:len(predTime)] , 'C3--')#, label="Predicted SS")
#        plt.plot(predTime + time[k], predALKALINITY[:len(predTime)] , 'C6--')#, label="Pred alkalinity")
#        plt.plot(predTime + time[k], predPHOSPATE[:len(predTime)] , 'C7--')#, label="Pred Phosphate")
#        plt.plot(predTime + time[k], predPHOSPATE_SP[:len(predTime)] , 'C8--')#, label="Pred Phosphate SP")
#    
#    leg = plt.legend( bbox_to_anchor = [1.23, 0.7])
#    plt.axvline(x=k*dt, ymin=0, ymax=1, color = 'black')
##    plt.xlim([0,100+k]) 
#    plt.xlim([0,time[-1]])
##    leg = plt.legend( loc = 'upper right')
#    plt.grid()
    
    
    
    
    
    fig, ax = plt.subplots(7,1, constrained_layout=True,sharex=True, figsize=[10,7])
    fig.suptitle(title, fontsize=16)
    
    
    ax[0].set_title('PIX')
    ax[0].plot(time[:k+1], U_PIX[:k+1], 'C0', label="controler PIX")
    ax[0].plot(predTime + time[k], predPIX, 'C0--')#, label="Predictied PIX")
    ax[0].axvline(x=k*dt, ymin=0, ymax=1, color = 'black')
    ax[0].set_xlim([0, time[-1]])
    ax[0].grid(True)
    
    ax[1].set_title('PAX')
    ax[1].plot(time[:k+1], U_PAX[:k+1], 'C4', label="controler PAX")
    ax[1].plot(predTime + time[k], predPAX, 'C4--')#, label="Predictied PIX")
    ax[1].axvline(x=k*dt, ymin=0, ymax=1, color = 'black')
    ax[1].grid(True)
    
    ax[2].set_title('POLYMER')
    ax[2].plot(time[:k+1], U_POL[:k+1], 'C5', label="controler Polymer")
    ax[2].plot(predTime + time[k], predPOL, 'C5--')#, label="Predictied PIX")
    ax[2].axvline(x=k*dt, ymin=0, ymax=1, color = 'black')
    ax[2].grid(True)
    
    ax[3].set_title('Suspended Solids')
    ax[3].plot(time[:k+1], U_SS[:k+1], 'C3', label="REAL SS inn")
    ax[3].plot(predTime + time[k], predSS, 'C3--')#, label="Predicted SS")
    ax[3].axvline(x=k*dt, ymin=0, ymax=1, color = 'black')
    ax[3].grid(True)
    
    ax[4].set_title('Turbidity')
    ax[4].plot(time[:k+1], turb[:k+1], 'C2', label="Turb (REAL)")
    ax[4].plot(predTime + time[k], predTURB, 'C2--')#, label="Predicted Turb")
    ax[4].plot(time[:], SP[:], 'C1', label="Setpunkt Turb")
    ax[4].plot(predTime + time[k], predTURB_SP, 'C5--')#, label="Predicted Turb SP")
    ax[4].axvline(x=k*dt, ymin=0, ymax=1, color = 'black')
    ax[4].grid(True)
    
    ax[5].set_title('Alkalinity')
    ax[5].plot(time[:k+1], alkalinity[:k+1], 'C6', label="alkalinity")
    ax[5].plot(predTime + time[k], predALKALINITY, 'C6--')#, label="Pred alkalinity")
    ax[5].axvline(x=k*dt, ymin=0, ymax=1, color = 'black')
    ax[5].grid(True)
    
    ax[6].set_title('phosphate')
    ax[6].plot(time[:k+1], phosphate[:k+1], 'C7', label="phosphate")
    ax[6].plot(time[:k+1], phosphate_SP[:k+1], 'C8', label="Phosphate SP")
    ax[6].plot(predTime + time[k], predPHOSPATE, 'C7--')#, label="Pred Phosphate")
    ax[6].plot(predTime + time[k], predPHOSPATE_SP, 'C8--')#, label="Pred Phosphate SP")
    ax[6].axvline(x=k*dt, ymin=0, ymax=1, color = 'black')
    ax[6].grid(True)
    
    
    
    
    
    
    
    
    
    
    plt.savefig('plot/Plott '+ UniqPlotId, bbox_inches='tight', dpi=1) if video == False else plt.savefig('plot/framebuffer/frame {:05d}'.format(PlotNumber), bbox_inches='tight')
#    plt.savefig('plot/Plott '+ UniqPlotId) if video == False else plt.savefig('plot/framebuffer/frame {:05d}'.format(PlotNumber))
    plt.show()
    
    print("U_PIX[k]:",U_PIX[k]," k:",k," time:",int(k*dt))
    