def objectiveFunction(u_guess,*arg):
    # Importing needed modules
    import model
    import numpy as np
    import matplotlib.pyplot as plt
    import pickle
    
    # Unpacking Testing Values for U
    U_test = u_guess
    # Unpacking Values Sendt Throw Arguments
    dt_test = arg[0]
    setpoint_test = arg[1]
    pred_horizion_length_test = arg[2]
    initStateValue_test = arg[3]
    initDelayValue_test = arg[4]
    # Defining Model Arrays
    NS_pred_horizion_test = int(pred_horizion_length_test/dt_test)+1
    pred_horizion_array_test = np.linspace(0, pred_horizion_length_test, NS_pred_horizion_test)
    SP_array_test = np.zeros(NS_pred_horizion_test) + setpoint_test
    Y_array_test = np.zeros(NS_pred_horizion_test)
    U_array_test = np.zeros(NS_pred_horizion_test)
    
    #%% SISO
    # Defining parameters for the testing model
    timeDelay_test = 0
    K_test = 4
    Tc1_test = 10
    Tc2_test = 40
    
    # Defining Model Object
    obj_model_test = model.secDegModel(dt = dt_test,
                                      K = K_test,
                                      Tc1 = Tc1_test,
                                      Tc2 = Tc2_test,
                                      timeDelay = timeDelay_test,
                                      initStateValue = initStateValue_test,
                                      initDelayValue = initDelayValue_test,
                                      offset = 6
                                      )
                               
    #%% MIMO
       
    
    ###########################################
    #|||||||||||||||||||||||||||||||||||||||||#
    #%%     Testing Values for U on Model     #
    #|||||||||||||||||||||||||||||||||||||||||#
    ###########################################

    # Diffing blocks
    # Assign all values for u_guess into eacual spaced in U_array test
    N_blocks_u = len(u_guess)  # Number of blocks of control signal
    N_samples_in_blocks = int(np.ceil(NS_pred_horizion_test/N_blocks_u))  # Number of samples in each control block
    
    U_array_test = np.array([np.zeros(N_samples_in_blocks) + u_guess for u_guess in u_guess])
    U_array_test = np.concatenate(U_array_test)
    U_array_test = U_array_test[:NS_pred_horizion_test]

    # Running simulation of "real" model function
    for k in range(NS_pred_horizion_test):
        # Y_array_test[k] = obj_model_test.run(u_k = 0) 
        Y_array_test[k] = obj_model_test.run(u_k = U_array_test[k]) 


    #|||||||||||||||||||||||||||||||||||||||||#
    #%%       PLOTTING THE SIMULATION         #
    #|||||||||||||||||||||||||||||||||||||||||#
    
    plt.figure(2)
    plt.title(f"U:{U_array_test[::1000]} \nY:{Y_array_test[::1000]} \nSP:{U_array_test[::1000]} \nerror:{5} \nFrom OBJ.FUNK")
    plt.plot(pred_horizion_array_test,U_array_test,label="input")
    plt.plot(pred_horizion_array_test,SP_array_test,label="setpoint")
    plt.plot(pred_horizion_array_test,Y_array_test,label="Output")
    plt.legend()
    plt.grid()
    plt.show()
    
    #|||||||||||||||||||||||||||||||||||||||||#
    #%%       Dumping array to file        #
    #|||||||||||||||||||||||||||||||||||||||||#
    with open('predArray.data',"wb") as datafile:
        pickle.dump((pred_horizion_array_test, U_array_test, Y_array_test, SP_array_test), datafile)
    datafile.close()
        
    #|||||||||||||||||||||||||||||||||||||||||#
    #%%    calculating objective equation     #
    #|||||||||||||||||||||||||||||||||||||||||#
    
    modelError = np.sum(SP_array_test-Y_array_test)
    J = modelError
    return J



#%% RUNNING CODE
if __name__ == "__main__":
    import numpy as np
   # import matplotlib.pyplot as plt
    start = 0
    stop = 10
    dt = 0.1
    ns = int((stop-start)/dt)+1
    
    time = np.linspace(start,stop,ns)
    Y = time * 0
    
    # objectiveFunction(U,      dt, SP, PredTime, initStateValue, initDelayValue)
    objectiveFunction([1],0.1,2,  100,      0,              0)