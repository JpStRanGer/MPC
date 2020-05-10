#%% Second degree class defenition
class secDegModel:
    #%%% secDegModel _init_
    def __init__(self, dt, K, Tc1, Tc2, timeDelay, initStateValue, initDelayValue, offset):
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
        self._y1_k = initStateValue[0] - offset
        self._y2_k = initStateValue[1] - offset
        
        
        
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
        u_k *= -1
        u_k *= K
        self._y1_k -= self.offset
        y1_buf = (((dt)/(Tc1+dt))*u_k) + ((Tc1/(Tc1+dt))*self._y1_k)
#        self._y1_k = (((dt)/(Tc1+dt))*u_k) + ((Tc1/(Tc1+dt))*self._y1_k)
        self._y2_k = (((dt)/(Tc2+dt))*self._y1_k) + ((Tc2/(Tc2+dt))*self._y2_k)
        self._y1_k = y1_buf
        return self._y1_k  + self.offset
        
        
        
#    #%%% secDegModel - RUN
#    def calculateMODEL(self, u_k):
#        dt = self._dt
#        K = self._K
#        Tc1 = self._Tc1
#        Tc2 = self._Tc2
#        
#        #Model calculation
#        if u_k < self.min:
#            u_k = self.min
#        elif u_k > self.max:
#            u_k = self.max
#
##        u_k = self._obj_delay.run(u_k)
##        u_k *= -1 # Inverting input because of turbidity reacts negativ to positive input of chemicals.
##        u_k *= self._K
#        self._y1_k -= self.offset
#        self._y1_k = (((dt)/(Tc1+dt))*u_k) + ((Tc1/(Tc1+dt))*self._y1_k)
#        self._y2_k = (((dt)/(Tc2+dt))*self._y1_k) + ((Tc2/(Tc2+dt))*self._y2_k)
#
#        return self._y2_k  + self.offset
#    
#    def run(self, u_k):
#        
#        if u_k < self.min:
#            u_k = self.min
#        elif u_k > self.max:
#            u_k = self.max
#
#        u_k *= -1 # Inverting input because of turbidity reacts negativ to positive input of chemicals.
#        u_d = self._obj_delay.run(u_k)
#        u_d = self.calculateMODEL(u_d)
#        u_d *= self._K
#        return u_d
        
    #%%% secDegModel - setState
    def setState(self,NewState):
        self._y1_k = NewState
        self._y2_k = NewState
        return None
    
    
#%% timedelay
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
#        print(initDelayValue)
        self._delay_array = np.zeros(self._timeDelayArrayLength) + initDelayValue
        
    def run(self, U):
#        #Timedelay calculation
#        u_out = self._delay_array[-1]
#        self._delay_array[1:] = self._delay_array[0:-1]
#        self._delay_array[0] = U
        u_out = U
        return u_out
    

#%% mimoMODEL
class mimoMODEL:
    def __init__(self, dt, initStateValue, parrameters):
        # Import Needed Modules
#        print('from model - initStateValue',initStateValue)
        # Set initial states
        initStateValuePIX = initStateValue[0]
        initStateValuePAX = initStateValue[1]
        initStateValuePOL = initStateValue[2]
        initDelayValueSS = initStateValue[3]
        # Set initial DelayValue
#        initDelayValuePIX = initDelayValue[0]
#        initDelayValuePAX = initDelayValue[1]
#        initDelayValuePOL = initDelayValue[3]
#        initDelayValueSS = initDelayValue[4]
        
        #unpacking parameters
        
        
        # Define constants
        self.dt = dt
        # Define objects        
        self._objPIX = secDegModel(dt,
                                    # K =2, 
                                    # Tc1 = 10, 
                                    # Tc2 = 4, 
                                    # timeDelay = 10, 
                                    # initStateValue = initStateValuePIX, 
                                    # initDelayValue = 0, 
                                    # offset = 0 
                                    K =parrameters['pix']['K'],
                                    Tc1 = parrameters['pix']['Tc1'], 
                                    Tc2 = parrameters['pix']['Tc2'], 
                                    timeDelay = parrameters['pix']['timeDelay'], 
                                    initStateValue = initStateValuePIX, 
                                    initDelayValue = parrameters['pix']['initDelayValue'], 
                                    offset = parrameters['pix']['offset']
                                   )
        self._objPAX = secDegModel(dt, 
                                   # K =3, 
                                   # Tc1 = 30, 
                                   # Tc2 = 8, 
                                   # timeDelay = 30, 
                                   # initStateValue = initStateValuePAX, 
                                   # initDelayValue = 0, 
                                   # offset = 0
                                    K =parrameters['pax']['K'],
                                    Tc1 = parrameters['pax']['Tc1'], 
                                    Tc2 = parrameters['pax']['Tc2'], 
                                    timeDelay = parrameters['pax']['timeDelay'], 
                                    initStateValue = initStateValuePAX, 
                                    initDelayValue = parrameters['pax']['initDelayValue'], 
                                    offset = parrameters['pax']['offset']
                                   )
        self._objPOL = secDegModel(dt, 
                                   # K =0.5, 
                                   # Tc1 = 10, 
                                   # Tc2 = 4, 
                                   # timeDelay = 60, 
                                   # initStateValue = initStateValuePOL, 
                                   # initDelayValue = 0, 
                                   # offset = 0
                                    K =parrameters['pol']['K'],
                                    Tc1 = parrameters['pol']['Tc1'], 
                                    Tc2 = parrameters['pol']['Tc2'], 
                                    timeDelay = parrameters['pol']['timeDelay'], 
                                    initStateValue = initStateValuePOL, 
                                    initDelayValue = parrameters['pol']['initDelayValue'], 
                                    offset = parrameters['pol']['offset']
                                   )
        self._objSS = timedelay(timeDelay = 0, 
                                dt = self.dt, 
                                initDelayValue = initDelayValueSS
                                )
     
    #%%% RUN FUNCTION
    def run(self, u_pix, u_pax, u_pol, u_ss, u_flow):
    # def run(self, u_pix = -10, u_pax = -20, u_pol = -30, u_ss = -40, u_flow = -50):
        self.pixState = self._objPIX.run(u_pix)
        self.paxState = self._objPAX.run(u_pax)
        self.polState = self._objPOL.run(u_pol)
        self.ssState = self._objSS.run(u_ss)
        self.u_flow = u_flow
        
        self.turbState = self.pixState + self.paxState + self.polState + self.ssState # + self.u_flow
        return self.turbState, self.pixState, self.paxState, self.polState, self.ssState, self.u_flow

    #%%% RETURN STATES FUNCTION
    def returnStates(self):
        return [self._objPIX._y1_k, self._objPIX._y2_k], [self._objPAX._y1_k, self._objPAX._y2_k], [self._objPOL._y1_k, self._objPOL._y2_k], self._objSS._delay_array[0]
        return [self._objPIX._y1_k, self._objPIX._y2_k], [self._objPAX._y1_k, self._objPAX._y2_k], [self._objPOL._y1_k, self._objPOL._y2_k], self._objSS._delay_array[0]
    
###################################################################
#%% CODE BELOW THIS LINE IS ONLY FOR ISOLATED TESTING THE CODE ABOVE
###################################################################
if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt
    import modelparameters
    
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
    # PIX input
    U_pix = np.zeros(len(time))
    U_pix[int(100/dt):] += 1
    U_pix[int(200/dt):] += -1
    
    # PAX input
    U_pax = np.zeros(len(time))
    U_pax[int(300/dt):] += 1
    U_pax[int(400/dt):] += -1
    
    # POL input
    U_pol = np.zeros(len(time))
    U_pol[int(500/dt):] += 1
    U_pol[int(600/dt):] += -1
    
    # SS/TURB input
    U_SS = np.zeros(len(time)) + np.sin(2*np.pi*time/150)*0+10
#    U_SS /= 10
    
    # FLOW input
    U_flow = np.zeros(len(time)) + np.sin(2*np.pi*time/600)
    
    
    Turb_mimo = time * 0
    
    
    U_PIX_INITIAL = [2,2]
    U_PAX_INITIAL = [0,0]
    U_POL_INITIAL = [2,2]
    modelStates = [U_PIX_INITIAL, U_PAX_INITIAL, U_POL_INITIAL, U_SS[0]]
    
    #%% DEFINING MODEL PARAMENTERS
#    turbParrameters = {
#        'pix' : {
#            'K' : 2,
#            'Tc1' : 10,
#            'Tc2' : 4,
#            'timeDelay' : 0,
#            'initDelayValue' : 0,
#            'offset' : 0
#            },
#        'pax' : {
#            'K' : 3,
#            'Tc1' : 30,
#            'Tc2' : 8,
#            'timeDelay' : 30,
#            'initDelayValue' : 0,
#            'offset' : 0
#            },
#        'pol' : {
#            'K' : 0.5,
#            'Tc1' : 10,
#            'Tc2' : 4,
#            'timeDelay' : 60,
#            'initDelayValue' : 0,
#            'offset' : 0
#            },
#        }
    #%%MIMO model
    obj_mimo = mimoMODEL(dt, modelStates, modelparameters.turbParrameters)
    
    
    for k in range(len(time)):
        Turb_mimo[k], Y_pix[k], Y_pax[k], Y_pol[k], Y_ss[k], Y_flow[k] = obj_mimo.run(U_pix[k], U_pax[k], U_pol[k], U_SS[k], U_flow[k])
    
    #%%% MIMO Plotting
    #%%            Plotting arrays
    #|||||||||||||||||||||||||||||||||||||||||#
    ###########################################
    fig, ax = plt.subplots(5,1, constrained_layout=True,sharex=True, figsize=[8,7])
    fig.suptitle('Multivarible model simulation\nInput components', fontsize=16)
    
    ax[0].set_title('PIX')
    ax[0].plot(time,U_pix)
    ax[0].plot(time,Y_pix)
    ax[0].grid(True)
    
    ax[1].set_title('PAX')
    ax[1].plot(time,U_pax)
    ax[1].plot(time,Y_pax)
    ax[1].grid(True)
    
    
    ax[2].set_title('POLYMER')
    ax[2].plot(time,U_pol)
    ax[2].plot(time,Y_pol)
    ax[2].grid(True)
    
    
    ax[3].set_title('SS in')
    ax[3].plot(time,U_SS)
    ax[3].plot(time,Y_ss)
    ax[3].grid(True)
#    
#    ax[4].set_title('flow')
#    ax[4].plot(time,U_flow)
#    ax[4].plot(time,Y_flow)
#    ax[4].grid(True)
    
    ax[4].set_title('Turb')
    ax[4].plot(time, Turb_mimo)
    ax[4].grid(True)
    
    
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
