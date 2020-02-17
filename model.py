class secDegModel:
    def __init__(self, dt, K =1, Tc1 = 4, Tc2 = 4, timeDelay = 10, initStateValue = 0, initDelayValue = 0):
        # Import Needed Modules
        
        # Define objects
        self._obj_delay = timedelay(timeDelay = timeDelay, dt = dt, initDelayValue = initDelayValue)
        #self._obj_delay = timedelay(timeDelay,dt)
        # Define Model Parameters
        self._dt = dt
        self._K = K
        self._Tc1 = Tc1
        self._Tc2 = Tc2
        # Define State Variables
        self._y1_k = initStateValue
        self._y2_k = initStateValue
        
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
    
    def setState(self,NewState):
        self._y1_k = NewState
        self._y2_k = NewState
        return None
    
    

class timedelay:
    def __init__(self, timeDelay, dt, initDelayValue = 0):
        # Import Needed Modules
        import numpy as np
        # Define Timedelay Variables
        self._timeDelay = timeDelay
        self._N_Delay_samples = max(int(timeDelay/dt)+1,1)
        self._initDelayValue = initDelayValue
        self._timeDelay = timeDelay
        self._timeDelayArrayLength = int(round(timeDelay/dt)+ 1) 
        self._delay_array = np.zeros(self._timeDelayArrayLength)+initDelayValue
        
    def run(self, U):
        #Timedelay calculation
        u_out = self._delay_array[-1]
        self._delay_array[1:] = self._delay_array[0:-1]
        self._delay_array[0] = U
        return u_out
    
if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt
    
    obj_delay = timedelay(timeDelay=11,dt=0.1,initDelayValue=3)
    obj_delay.run(10)
    
    print("_delay_array:",obj_delay._delay_array)
    
    start = 0
    stop = 300
    dt = 0.1
    ns = int((stop-start)/dt)+1
    time = np.linspace(start,stop,ns)
    
    
    obj_model = secDegModel(dt = dt,
                            K =4,
                            Tc1 = 30,
                            Tc2 = 60,
                            timeDelay = 50,
                            initStateValue = 3,
                            initDelayValue = 0
                            )
    Y = time * 0
    for k in range(len(time)):
        Y[k] = obj_model.run(0.28658928)
    plt.plot(time,Y)
    plt.grid()
    
    
    