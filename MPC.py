def objectiveFunction(x,*arg):
    # Importing needed modules
    import model
    
    # Unpacking Testing Values for U
    U_test = x
    # Unpacking Values Sendt Throw Arguments
    SP_test = arg[0]
    dt_test = arg[1]
    
    # Defining Model Arrays
    Y_test = arg[0] * 0
    time_test = arg[1]
    
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
    for k in range(len(arg[0])):
        Y_test[k] = obj_model_test.run(u_k = U_test) 

    #      DONE SIMULATING "REALSYSTEM"       #
    #|||||||||||||||||||||||||||||||||||||||||#
    plt.figure()
    plt.plot(time_test,SP_test)
    plt.plot(time_test,Y_test)
    plt.grid()
    plt.show()
    error = np.sum(abs(SP_test-Y_test))
    return error

class MPC:
    def __init__(self, dt):
        import model
        from scipy.optimize import minimize
        
        ################
        # Initiating modelobject to be simulated
        obj_model_test = model.secDegModel(dt)
        
        return

if __name__ == "__main__":
    import model
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.optimize import minimize
    start = 0
    stop = 1000
    dt = 0.1
    ns = int((stop-start)/dt)+1
    
    time = np.linspace(start,stop,ns)
    Y = time * 0


def objectiveFunction(x,*arg):
