def objectiveFunction(x,*arg):
    # Importing needed modules
    import model
    import numpy as np
    import matplotlib.pyplot as plt
    # Unpacking Testing Values for U
    U_test = x
    # Unpacking Values Sendt Throw Arguments
    dt_test = arg[0]
    setpoint_test = arg[1]
    pred_horizion_length_test = arg[2]
    initStateValue_test = arg[3]
    # Defining Model Arrays
    NS_pred_horizion_test = int(pred_horizion_length_test/dt_test)+1
    pred_horizion_array_test = np.linspace(0, pred_horizion_length_test, NS_pred_horizion_test)
    SP_array_test = np.zeros(NS_pred_horizion_test) + setpoint_test
    Y_array_test = SP_array_test * 0
    
    # Defining parameters for the testing model
    timeDelay_test = 50
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
                                      initStateValue = initStateValue_test,
                                      initDelayValue = initDelayValue_test
                                      )
                                      
    
    ###########################################
    #|||||||||||||||||||||||||||||||||||||||||#
    #     Testing Values for U on Model       #
    #|||||||||||||||||||||||||||||||||||||||||#
    ###########################################


    # Running simulation of "real" model function
    for k in range(NS_pred_horizion_test):
        Y_array_test[k] = obj_model_test.run(u_k = U_test) 

    #      DONE SIMULATING "REALSYSTEM"       #
    #|||||||||||||||||||||||||||||||||||||||||#
#    plt.figure(2)
#    plt.plot(pred_horizion_array_test,SP_array_test,label="setpoint")
#    plt.plot(pred_horizion_array_test,Y_array_test,label="putput")
#    plt.legend()
#    plt.grid()
#    plt.show()
    error = np.sum(abs(SP_array_test-Y_array_test))
    return error

def objectiveFunction_TEST(x,*arg):
    # Importing needed modules
    import numpy as np
    import matplotlib.pyplot as plt
    # Unpacking Testing Values for U
    U_test = x
    # Unpacking Values Sendt Throw Arguments
    dt_test = arg[0]
    setpoint_test = arg[1]
    pred_horizion_length_test = arg[2]
    initStateValue_test = arg[3]
    obj_model_test = arg[4]
    # Defining Model Arrays
    NS_pred_horizion_test = int(pred_horizion_length_test/dt_test)+1
    pred_horizion_array_test = np.linspace(0, pred_horizion_length_test, NS_pred_horizion_test)
    SP_array_test = np.zeros(NS_pred_horizion_test) + setpoint_test
    Y_array_test = SP_array_test * 0
    
    # Defining parameters for the testing model
    timeDelay_test = 50
    initDelayValue_test = 0
    K_test = 4
    Tc1_test = 30
    Tc2_test = 60
    
                                      
    
    ###########################################
    #|||||||||||||||||||||||||||||||||||||||||#
    #     Testing Values for U on Model       #
    #|||||||||||||||||||||||||||||||||||||||||#
    ###########################################

    obj_model_test.setState(initStateValue_test)
    # Running simulation of "real" model function
    for k in range(NS_pred_horizion_test):
        Y_array_test[k] = obj_model_test.run(u_k = U_test) 

    #      DONE SIMULATING "REALSYSTEM"       #
    #|||||||||||||||||||||||||||||||||||||||||#
#    plt.figure(2)
#    plt.plot(pred_horizion_array_test,SP_array_test,label="setpoint")
#    plt.plot(pred_horizion_array_test,Y_array_test,label="putput")
#    plt.legend()
#    plt.grid()
#    plt.show()
    error = np.sum(abs(SP_array_test-Y_array_test))
    return error

if __name__ == "__main__":
    import numpy as np
   # import matplotlib.pyplot as plt
    start = 0
    stop = 10
    dt = 0.1
    ns = int((stop-start)/dt)+1
    
    time = np.linspace(start,stop,ns)
    Y = time * 0
    
    # objectiveFunction(U, dt, SP, PredTime, initStateValue)
    objectiveFunction(0.28658928,0.1,2,300,3)