class secDegModel:
    def __init__(self, dt, K =1, Tc1 = 4, Tc2 = 4, timeDelay = 10):
        # Import Needed Modules
        
        # Define objects
        self._obj_delay = timedelay(timeDelay,dt)
        # Define Model Parameters
        self._dt = dt
        self._K = K
        self._Tc1 = Tc1
        self._Tc2 = Tc2
        # Define State Variables
        self._y1_k = 0
        self._y2_k = 0
        
    def run(self, u_k):
        dt = self._dt
        K = self._K
        Tc1 = self._Tc1
        Tc2 = self._Tc2
        
        #Model calculation
        u_k = self._obj_delay.run(u_k)
        u_k *= K
        self._y1_k = (((dt)/(Tc1+dt))*u_k) + ((Tc1/(Tc1+dt))*self._y1_k)
        self._y2_k = (((dt)/(Tc2+dt))*self._y1_k) + ((Tc2/(Tc2+dt))*self._y2_k)
        return self._y2_k
    
    

class timedelay:
    def __init__(self, timeDelay, dt, initDelayValue = 0):
        # Import Needed Modules
        import numpy as np
        # Define Timedelay Variables
        self._timeDelay = timeDelay
        self._N_Delay_samples = int(timeDelay/dt)+1
        self._initDelayValue = initDelayValue
        self._timeDelay = max(timeDelay,1)
        self._timeDelayArrayLength = int(round(timeDelay/dt)) + 1
        self._delay_array = np.zeros(self._timeDelayArrayLength)+initDelayValue
        
    def run(self, U):
        #Timedelay calculation
        u_out = self._delay_array[-1]
        self._delay_array[1:] = self._delay_array[0:-1]
        self._delay_array[0] = U
        return u_out