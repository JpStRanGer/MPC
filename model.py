#%% Second degree class defenition
class secDegModel:
    #%%% secDegModel _init_
    def __init__(self, dt, K =1, Tc1 = 30, Tc2 = 60, timeDelay = 10, initStateValue = 0, initDelayValue = 0, offset = 0):
        # Import Needed Modules
        
        # Define objects
        self._obj_delay = timedelay(timeDelay = timeDelay, dt = dt, initDelayValue = initDelayValue)
        #self._obj_delay = timedelay(timeDelay,dt)
        self.min = 0
        self.max = 10
        # Define Model Parameters
        self.offset = offset
        self._dt = dt
        self._K = K
        self._Tc1 = Tc1
        self._Tc2 = Tc2
        # Define State Variables
        self._y1_k = initStateValue - offset
        self._y2_k = initStateValue - offset
    #%%% secDegModel - RUN
    def run(self, u_k):
        dt = self._dt
        K = self._K
        Tc1 = self._Tc1
        Tc2 = self._Tc2
        
        #Model calculation
        if u_k < self.min:
            u_k = self.min
        elif u_k > self.max:
            u_k = self.max

        u_k = self._obj_delay.run(u_k)
        u_k *= -1 # Inverting input because of turbidity reacts negativ to positive input of chemicals.
        u_k *= self._K
        self._y1_k -= self.offset
        self._y1_k = (((dt)/(Tc1+dt))*u_k) + ((Tc1/(Tc1+dt))*self._y1_k)
        self._y2_k = (((dt)/(Tc2+dt))*self._y1_k) + ((Tc2/(Tc2+dt))*self._y2_k)

        return self._y1_k  + self.offset
    
    #%%% secDegModel - setState
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
        self._delay_array = np.zeros(self._timeDelayArrayLength) + initDelayValue
        
    def run(self, U, K = 1):
        #Timedelay calculation
        u_out = self._delay_array[-1]
        self._delay_array[1:] = self._delay_array[0:-1]
        self._delay_array[0] = U
        return u_out
    
class mimoMODEL:
    def __init__(self, dt, initStateValue):
        # Import Needed Modules
        
        # Set initial states
        self.initStateValueTURB = initStateValue[0]
        self.initStateValueSS = initStateValue[1]
        # Define constants
        self.dt = dt
        # Define objects        
        self._objPIX = secDegModel(dt, K =1, Tc1 = 4, Tc2 = 4, timeDelay = 0, initStateValue = 0, initDelayValue = 0, offset = 0)
        self._objPAX = secDegModel(dt, K =1, Tc1 = 4, Tc2 = 4, timeDelay = 0, initStateValue = 0, initDelayValue = 0, offset = 0)
        self._objPOL = secDegModel(dt, K =1, Tc1 = 4, Tc2 = 4, timeDelay = 0, initStateValue = 0, initDelayValue = 0, offset = 0)
        self._objSS = timedelay(timeDelay = 0 , dt = self.dt, initDelayValue = self.initStateValueSS)
        
    def run(self, u_pix, u_pax, u_pol, u_ss, u_flow):
    # def run(self, u_pix = -10, u_pax = -20, u_pol = -30, u_ss = -40, u_flow = -50):
        self.pixState = self._objPIX.run(u_pix)
        self.paxState = self._objPAX.run(u_pax)
        self.polState = self._objPOL.run(u_pol)
        self.ssState = self._objSS.run(u_ss, 4)
        self.u_flow = u_flow
        
        self.turbState = self.pixState + self.paxState + self.polState + self.ssState # + self.u_flow
        return self.turbState, self.pixState, self.paxState, self.polState, self.ssState, self.u_flow

###################################################################
#%% CODE BELOW THIS LINE IS ONLY FOR ISOLATED TESTING THE CODE ABOVE
###################################################################
if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt
    
    start = 0
    stop = 1200
    dt = 0.1
    ns = int((stop-start)/dt)+1
    time = np.linspace(start,stop,ns)
    
    
    # #%% Defining In/Out-putArrays
    # #%%% STATE-ARRAYS
    Y_pix = np.zeros(len(time))
    Y_pax = np.zeros(len(time))
    Y_pol = np.zeros(len(time))
    Y_ss = np.zeros(len(time))
    Y_flow = np.zeros(len(time))
    #%%% SYSTEM INPUT ARRAYS
    # PAX input
    U_pax = np.zeros(len(time))
    U_pax[int(100/dt):] += 1
    U_pax[int(200/dt):] += -1
    
    # PIX input
    U_pix = np.zeros(len(time))
    U_pix[int(300/dt):] += 1
    U_pix[int(400/dt):] += -1
    
    # POL input
    U_pol = np.zeros(len(time))
    U_pol[int(500/dt):] += 1
    U_pol[int(600/dt):] += -1
    
    # SS/TURB input
    U_SS = np.zeros(len(time)) + np.sin(2*np.pi*time/150)
    U_SS /= 10
    
    # FLOW input
    U_flow = np.zeros(len(time)) + np.sin(2*np.pi*time/600)
    
    #%%MIMO model
    obj_mimo = mimoMODEL(dt, [5,U_SS[0]])
    
    
    Turb_mimo = time * 0
    for k in range(len(time)):
        Turb_mimo[k], Y_pix[k], Y_pax[k], Y_pol[k], Y_ss[k], Y_flow[k] = obj_mimo.run(U_pix[k], U_pax[k], U_pol[k], U_SS[k], U_flow[k])
    
    #%%% MIMO Plotting
    #%%            Plotting arrays
    #|||||||||||||||||||||||||||||||||||||||||#
    ###########################################
    fig, ax = plt.subplots(6,1, constrained_layout=True,sharex=True, figsize=[8,7])
    fig.suptitle('Multivarible model simulation\nInput components', fontsize=16)
    
    ax[0].set_title('PAX')
    ax[0].plot(time,U_pax)
    ax[0].plot(time,Y_pax)
    ax[0].grid(True)
    
    ax[1].set_title('PIX')
    ax[1].plot(time,U_pix)
    ax[1].plot(time,Y_pix)
    ax[1].grid(True)
    
    
    ax[2].set_title('POLYMER')
    ax[2].plot(time,U_pol)
    ax[2].plot(time,Y_pol)
    ax[2].grid(True)
    
    
    ax[3].set_title('SS in')
    ax[3].plot(time,U_SS)
    ax[3].plot(time,Y_ss)
    ax[3].grid(True)
    
    ax[4].set_title('flow')
    ax[4].plot(time,U_flow)
    ax[4].plot(time,Y_flow)
    ax[4].grid(True)
    
    ax[5].set_title('Turb')
    ax[5].plot(time, Turb_mimo)
    ax[5].grid(True)
    
    
    #%% SISO model
    
    
    # obj_delay = timedelay(timeDelay=11,dt=0.1,initDelayValue=3)
    # obj_delay.run(10)
    
    # print("_delay_array:",obj_delay._delay_array)
    
    # obj_model = secDegModel(dt = dt,
    #                         K =4,
    #                         Tc1 = 30,
    #                         Tc2 = 60,
    #                         timeDelay = 1000,
    #                         initStateValue = 0,
    #                         initDelayValue = 0,
    #                         offset = 2
    #                         )
    # Y_siso = time * 0
    
    # print("_delay_array:",obj_model._obj_delay._delay_array[:20])
    
    # for k in range(len(time)):
    #     Y_siso[k] = obj_model.run(0)
    # plt.plot(time,Y_siso)
    # plt.grid()
