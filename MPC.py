def objectiveFunction(x,*arg):
    # Importing needed modules
    import model
    
    # Unpacking Testing Values for U
    U_test = x
    # Unpacking Values Sendt Throw Arguments
    dt_test = arg[0]
    
    # Defining Model Arrays
    time_test = arg[1]
    SP_test = arg[1]
    Y_test = SP_test * 1
    
    # Defining parameters for the testing model
    timeDelay_test = 10
    initDelayValue_test = 0
    K_test = 4
    Tc1_test = 30
    Tc2_test = 60
    
    # Defining Model Object
    obj_model_test = model.secDegModel(dt = dt_test,
                                      K = K_test,
                                      Tc1 = Tc1_test,
                                      Tc2 = Tc2_test,
                                      timeDelay = timeDelay_test,
                                      )
    
    ###########################################
    #|||||||||||||||||||||||||||||||||||||||||#
    #     Testing Values for U on Model       #
    #|||||||||||||||||||||||||||||||||||||||||#
    ###########################################


    # Running simulation of "real" model function
    for k in range(len(time_test)):
        Y_test[k] = obj_model_test.run(u_k = U_test) 

    #      DONE SIMULATING "REALSYSTEM"       #
    #|||||||||||||||||||||||||||||||||||||||||#
    plt.figure()
    #plt.plot(time_test,SP_test)
    plt.plot(time_test,Y_test)
    plt.grid()
    plt.show()
    error = np.sum(abs(SP_test-Y_test))
    return error

class MPC:
    def __init__(self, dt, pred_horizion_length, NumberOfBlocks):
        import model
        from scipy.optimize import minimize
        # Defining values
        self.pred_horizion_length = pred_horizion_length # [Sec]
        self.NS_pred_horizion = int(pred_horizion_length/dt)+1 # Numer Of samples In Pred Horizion
        self.NumberOfBlocks = NumberOfBlocks # [stk]
        self.initial_guess = 0
        self.Setpoint = 0
        # Defining Arrays
        self.pred_horizion_array = np.linspace(0,pred_horizion_length,NS_pred_horizion)
        self.U_guess = [initial_guess for i in range(NumberOfBlocks)]
        
        ################
        # Initiating modelobject to be simulated
        self.obj_model_test = model.secDegModel(dt)
        
        
        return
    
    def run(self):
        self.arg_guess = (SP,self.pred_horizion)
        solution_guess = minimize(objectiveFunction,U_guess,arg_guess, method = "SLSQP")
        self.x_opt = solution_guess
        return self.x_opt

if __name__ == "__main__":
    import model
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.optimize import minimize
    start = 0
    stop = 10
    dt = 0.1
    ns = int((stop-start)/dt)+1
    
    time = np.linspace(start,stop,ns)
    Y = time * 0
    
    obj_mpc = MPC