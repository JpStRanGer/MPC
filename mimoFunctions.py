# Importing needed modules
import model
import numpy as np
import matplotlib.pyplot as plt
import pickle
    
def makePredInputArray(dt, inArray, predTimeLength):
    # Check if the input is an array or a scalar
    if type(inArray) == type(np.array(1)):
        #print('IT IS ARRAY!')
        if len(inArray) < predTimeLength:
            restlength = predTimeLength - len(inArray)
            restArray = np.zeros(restlength) + inArray[-1]
            outArray = np.concatenate((inArray,restArray))

        elif len(inArray) > predTimeLength:
            outArray = inArray[:predTimeLength]

        else:
            outArray = np.zeros(int(predTimeLength/dt))
        
        return outArray
    elif type(inArray) == type(1) or type(inArray) == type(np.int32(1)):
        #print('IT IS SCALAR!')
        outArray = np.zeros(predTimeLength) + inArray
        return outArray
    else:
        print("ERROR: The input is not numpy array or a SCALAR\n",type(inArray),inArray)
        

#%% DEFINING FUNCTION FOR BLOCK-INPUT-ARRAY
def makeblockInputArray(arrayLength, blockValues):
    import numpy as np
    # Diffing blocks
    # Assign all values for u_guess into eacual spaced in U_array test
    N_samples_in_blocks = int(np.ceil(arrayLength/len(blockValues)))  # Number of samples in each control block
    U_array_test = np.array([np.zeros(N_samples_in_blocks) + Values for Values in blockValues])
    U_array_test = np.concatenate(U_array_test)
    return U_array_test[:arrayLength]

#%% DEFINING OBJECTIVE FUNCTION
def objectiveFunction(u_guess,*arg):
    # Importing needed modules
    import model
    import numpy as np
    import matplotlib.pyplot as plt
    import pickle
    
    #%% Unpacking Values Sendt Throw Arguments
    dt_test = arg[0]
    setpoint_test = arg[1]
    pred_horizion_length_test = arg[2]
    initStateValue_test = arg[3]
    N_blocks = arg[4]
    RUN_PLOT = arg[5]
    
    #%% Unpacking Initial Values
    SS_init_test = initStateValue_test[1]
    
    #%% Unpacking Testing Values for U
    u_guess = np.reshape(u_guess,[-1, N_blocks]) # Reshape U_guess into array of rows = inputs, and collums = blocks
    U_blocks_test = u_guess[0]
    
    #%% Defining Model variables
    #%% constants
    NS_pred_horizion_test = int(pred_horizion_length_test/dt_test)+1
    #%% Arrays
    pred_horizion_array_test = np.linspace(0, pred_horizion_length_test, NS_pred_horizion_test)
    SP_array_test = makePredInputArray(dt_test, setpoint_test, NS_pred_horizion_test)
#    SP_array_test = np.zeros(NS_pred_horizion_test) + setpoint_test
    Turb_array_test = np.zeros(NS_pred_horizion_test)
    
                               
    #%% OBJECTS DECLARATIONS      
    obj_MIMOmodel_test = model.mimoMODEL(dt_test, initStateValue_test)
    
    ###########################################
    #|||||||||||||||||||||||||||||||||||||||||#
    #%%         Defining input arrays         #
    #|||||||||||||||||||||||||||||||||||||||||#
    ###########################################
    
    # SS/TURB input
    U_SS_test = np.zeros(len(pred_horizion_array_test)) + 2 * np.sin(2*np.pi*pred_horizion_array_test/600) + SS_init_test
    
    # FLOW input
    U_flow_test = np.zeros(len(pred_horizion_array_test)) + np.sin(2*np.pi*pred_horizion_array_test/10) + 5
    
    ###########################################
    #|||||||||||||||||||||||||||||||||||||||||#
    #%%     Testing Values for U on Model     #
    #|||||||||||||||||||||||||||||||||||||||||#
    ###########################################

    # Defining blocks
    PIX_array_test = makeblockInputArray(arrayLength = NS_pred_horizion_test, blockValues =  U_blocks_test)

    # Running simulation of "real" model function
    for k in range(NS_pred_horizion_test):
        # Turb_array_test[k] = obj_model_test.run(u_k = 0) 
        # Turb_array_test[k] = obj_model_test.run(u_k = PIX_array_test[k]) 
        Turb_array_test[k], *restArray = obj_MIMOmodel_test.run(u_pix = PIX_array_test[k],
                                                                u_pax = 1,
                                                                u_pol = 1,
                                                                u_ss = U_SS_test[k],
                                                                u_flow = U_flow_test[k])
          
    #|||||||||||||||||||||||||||||||||||||||||#
    #%%    calculating objective equation     #
    #|||||||||||||||||||||||||||||||||||||||||#
    modelError = np.sum(abs(SP_array_test-Turb_array_test))
    avgError = np.average(abs(SP_array_test-Turb_array_test))
    J = modelError

    #|||||||||||||||||||||||||||||||||||||||||#
    #%%       PLOTTING THE SIMULATION         #
    #|||||||||||||||||||||||||||||||||||||||||#
    if RUN_PLOT:
        plt.figure(2)
        plt.title("U:{} \nY:{} \nSP:{} \nerror:{:0.2f} \nFrom OBJ.FUNK".format(U_blocks_test, np.average(Turb_array_test), PIX_array_test[-1], modelError))
        plt.plot(pred_horizion_array_test,PIX_array_test,label="input")
        plt.plot(pred_horizion_array_test,SP_array_test,label="TURB setpoint")
        plt.plot(pred_horizion_array_test,Turb_array_test,label="TURB Output")
        plt.plot(pred_horizion_array_test,U_SS_test,label="U_SS_test")
        plt.legend()
        plt.grid()
        plt.show()
    

    
    #|||||||||||||||||||||||||||||||||||||||||#
    #%%       Dumping array to file        #
    #|||||||||||||||||||||||||||||||||||||||||#
    with open('predArray.data',"wb") as datafile:
        pickle.dump((pred_horizion_array_test, Turb_array_test, SP_array_test, PIX_array_test, U_SS_test, modelError, avgError), datafile)
    # datafile.close()
        
    return J


#%% RUNNING CODE
###################################################################
# CODE BELOW THIS LINE IS ONLY FOR ISOLATED TESTING THE CODE ABOVE
###################################################################
if __name__ == "__main__":
    import numpy as np
   # import matplotlib.pyplot as plt
    start = 0
    stop = 10
    dt = 0.1
    ns = int((stop-start)/dt)+1
    
    time = np.linspace(start,stop,ns)
    Y = time * 0
    
    u_guess = [1,5,4,2],[6,7,8,9]
    u_guess = np.concatenate(u_guess)
    #         objectiveFunction(U,            dt,  SP, PredTime, initStateValue, nuber of blocks, RUN_PLOT)
    result =  objectiveFunction(u_guess,      0.1, 2,  100,      [10,10],         4,               1)
    print("RESULTING ERROR: ",result)