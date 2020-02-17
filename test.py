import numpy as np
from scipy.optimize import minimize, rosen, rosen_der

def callback(x):
    #fobj = rosen(x)
    #history.append(fobj)
    history.append(x)

def Function(x):
    # Defining time range and resulution
    start = 0
    stop = 1000
    dt = 0.1
    ns = int((stop-start)/dt+1)
    time = np.linspace(start,stop,ns)
    
    SP_test = 2
    U = np.array([x[0] for t in time])

    ###########################################
    #|||||||||||||||||||||||||||||||||||||||||#
    #     SIMULATION OF "REAL" SYSTEM         #
    #|||||||||||||||||||||||||||||||||||||||||#
    ###########################################

    #PARAMETERS
    timeDelay = 10
    initDelayValue = 0
    K = 4
    Tc1 = 30
    Tc2 = 60

    # Running simulation of "real" model function
    y1 = np.zeros(len(U))
    y2 = np.zeros(len(U))
    timeDelay = max(timeDelay,1)
    timeDelayArrayLength = int(round(timeDelay/dt)) + 1
    delay_array = np.zeros(timeDelayArrayLength)+initDelayValue
    #Simulation loop:
    for k in range(1,len(U)):
        #Timedelay calculation
        u_out = delay_array[-1]
        delay_array[1:] = delay_array[0:-1]
        delay_array[0] = U[k]
        
        #Model calculation
        u_out *= K
        y1[k] = (((dt)/(Tc1+dt))*u_out) + ((Tc1/(Tc1+dt))*y1[k-1])
        y2[k] = (((dt)/(Tc2+dt))*y1[k]) + ((Tc2/(Tc2+dt))*y2[k-1])

    #      DONE SIMULATING "REALSYSTEM"       #
    #|||||||||||||||||||||||||||||||||||||||||#
    
    error = np.sum(abs(SP_test-Y_test))
    return error

history = []
x0 = [1.3, 0.7, 0.8, 1.9, 1.2]


print("history: ",history)
solution_guess = minimize(function,
                          U_guess,
                          callback= None,
                          method = "SLSQP")
print("result: ",result)
for i in history:
    print("history: ",i)