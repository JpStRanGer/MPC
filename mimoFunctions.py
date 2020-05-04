# Importing needed modules
import model
import numpy as np
import matplotlib.pyplot as plt
import pickle
import modelparameters

def makePredInputArray(dt, inArray, predTimeLength, name):
    # Check if the input is an array or a scalar
    try:
        # if type(inArray) == type(np.array(1)):
        if isinstance(inArray, (np.ndarray)):
            # print('IT IS ARRAY!',name)
            if len(inArray) < predTimeLength:
                restlength = predTimeLength - len(inArray)
                restArray = np.zeros(restlength) + inArray[-1]
                outArray = np.concatenate((inArray,restArray))
    
            elif len(inArray) > predTimeLength:
                outArray = inArray[:predTimeLength]
    
            else:
                outArray = np.zeros(int(predTimeLength/dt)) + inArray
            
            return outArray
        # elif type(inArray) == type(1) or type(inArray) == type(np.int32(1) or type(inArray) == type(np.float64(1.0)) or type(inArray) == float):
        elif isinstance(inArray,(int, float, np.int, np.int8, np.int16, np.int32, np.int64, np.float, np.float64, np.float32, np.float16)):
            # print('IT IS SCALAR!',name)
            outArray = np.zeros(predTimeLength) + inArray
            return outArray
        else:
            print('ERROR 1: making',name)
            print("ERROR: The input is not numpy array or a SCALAR\n",type(inArray),inArray)
            return makePredInputArray(dt, np.int32(inArray), predTimeLength, name)
            raise Exception('exception else')
    except:
            print('ERROR 2: making',name)
            print("except: The input is not numpy array or a SCALAR\n",type(inArray),inArray)
            raise Exception('exception while running '+name)

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
    #%%% UNPACKING
    #%%%% Unpacking Values Sendt Throw Arguments
    dt_test = arg[0]
    setpoint_test = arg[1]
    pred_horizion_length_test = arg[2]
    initControlSignals_test = arg[3]
    TurbInitStateValue_test = arg[4]
    AlkalinityInitStateValue_test = arg[5]
    PhosphateInitStateValue_test = arg[6]
    N_blocks = arg[7]
    RUN_PLOT = arg[8]
    
    
    #%%%% Unpacking Initial Values used for model initisation
    PIX_init_test = initControlSignals_test[0]
    PAX_init_test = initControlSignals_test[1]
    POL_init_test = initControlSignals_test[2]
    SS_init_test = initControlSignals_test[3]
    
    #%%%% Unpacking Testing Values for U
    u_guess = np.reshape(u_guess,[-1, N_blocks]) # Reshape U_guess into array of rows = inputs, and collums = blocks
#    U_PIX_blocks_test = u_guess[0] 
#    U_PAX_blocks_test = u_guess[1]
#    U_POL_blocks_test = u_guess[2]
    U_PIX_blocks_test = u_guess[0]
    U_PAX_blocks_test = u_guess[1] if len(u_guess) >= 2 else U_PIX_blocks_test * 0
    U_POL_blocks_test = u_guess[2] if len(u_guess) >= 3 else U_PIX_blocks_test * 0
    
    #%%% DEFINING MODEL VARIABLES AND ARRAYS
    #%%%% constants
    NS_pred_horizion_test = int(pred_horizion_length_test/dt_test)+1
    #%%%% Arrays
    pred_horizion_array_test = np.linspace(0, pred_horizion_length_test, NS_pred_horizion_test)
    SP_TURB_array_test = makePredInputArray(dt_test, setpoint_test, NS_pred_horizion_test,'SP_TURB_array_test')
    SP_PHOSPHATE_array_test = makePredInputArray(dt_test, 0.6, NS_pred_horizion_test,'SP_PHOSPHATE_array_test')
#    SP_TURB_array_test = np.zeros(NS_pred_horizion_test) + setpoint_test
    Turb_array_test = np.zeros(NS_pred_horizion_test)
    Alkalinity_array_test = np.zeros(NS_pred_horizion_test)
    Phosphate_array_test = np.zeros(NS_pred_horizion_test)
    

    ###########################################
    #|||||||||||||||||||||||||||||||||||||||||#
    #%%         Defining input arrays         #
    #|||||||||||||||||||||||||||||||||||||||||#
    ###########################################
    # SS/TURB input
    U_SS_test = makePredInputArray(dt_test, SS_init_test, NS_pred_horizion_test, 'U_SS_test')
#    U_SS_test = np.zeros(len(pred_horizion_array_test)) + 2 * np.sin(2*np.pi*pred_horizion_array_test/600) + SS_init_test
    
    # FLOW input
    U_flow_test = np.zeros(len(pred_horizion_array_test)) + np.sin(2*np.pi*pred_horizion_array_test/10) + 5
    ###########################################
    #|||||||||||||||||||||||||||||||||||||||||#
    #%%     Testing Values for U on Model     #
    #|||||||||||||||||||||||||||||||||||||||||#
    ###########################################

    # Defining blocks
    PIX_array_test = makeblockInputArray(arrayLength = NS_pred_horizion_test, blockValues =  U_PIX_blocks_test)
    PAX_array_test = makeblockInputArray(arrayLength = NS_pred_horizion_test, blockValues =  U_PAX_blocks_test) if len(u_guess) >= 2 else PIX_array_test * 0
    POL_array_test = makeblockInputArray(arrayLength = NS_pred_horizion_test, blockValues =  U_POL_blocks_test) if len(u_guess) >= 2 else PIX_array_test * 0

    #%% DEFINING MODEL PARAMETERS
    turbParrameters_test = {
        'pix' : {
            'K' : 2,
            'Tc1' : 10,
            'Tc2' : 4,
            'timeDelay' : 0,
            'initDelayValue' : 0,
            'offset' : 0
            },
        'pax' : {
            'K' : 3,
            'Tc1' : 30,
            'Tc2' : 8,
            'timeDelay' : 30,
            'initDelayValue' : 0,
            'offset' : 0
            },
        'pol' : {
            'K' : 0.5,
            'Tc1' : 10,
            'Tc2' : 4,
            'timeDelay' : 60,
            'initDelayValue' : 0,
            'offset' : 0
            },
        }
    AlkalinityParrameters_test = {
        'pix' : {
            'K' : 6,
            'Tc1' : 1,
            'Tc2' : 4,
            'timeDelay' : 0,
            'initDelayValue' : 0,
            'offset' : 0
            },
        'pax' : {
            'K' : 3,
            'Tc1' : 2,
            'Tc2' : 8,
            'timeDelay' : 30,
            'initDelayValue' : 0,
            'offset' : 0
            },
        'pol' : {
            'K' : 0.5,
            'Tc1' : 4,
            'Tc2' : 4,
            'timeDelay' : 60,
            'initDelayValue' : 0,
            'offset' : 0
            },
        }
    phosphateParrameters_test = {
        'pix' : {
            'K' : 0.1,
            'Tc1' : 10,
            'Tc2' : 4,
            'timeDelay' : 0,
            'initDelayValue' : 0,
            'offset' : 0
            },
        'pax' : {
            'K' : 0.2,
            'Tc1' : 30,
            'Tc2' : 8,
            'timeDelay' : 0,
            'initDelayValue' : 0,
            'offset' : 0
            },
        'pol' : {
            'K' : 0.5,
            'Tc1' : 10,
            'Tc2' : 4,
            'timeDelay' : 0,
            'initDelayValue' : 0,
            'offset' : 0
            },
        }
    ###########################################
    #|||||||||||||||||||||||||||||||||||||||||#
    #%% OBJECTS DECLARATIONS      
    #|||||||||||||||||||||||||||||||||||||||||#
    ###########################################
    obj_MIMOmodel_test = model.mimoMODEL(dt_test, 
                                         TurbInitStateValue_test, 
                                         modelparameters.turbParrameters,#turbParrameters_test
                                         )
    obj_Alkalinity_test = model.mimoMODEL(dt_test, 
                                          AlkalinityInitStateValue_test, 
                                          modelparameters.AlkalinityParrameters,#AlkalinityParrameters_test
                                          )
    obj_Phosphate_test = model.mimoMODEL(dt_test, 
                                         PhosphateInitStateValue_test, 
                                         modelparameters.phosphateParrameters,#phosphateParrameters_test
                                         )
    
    # Running simulation of "real" model function
    for k in range(NS_pred_horizion_test):
        #%% simulatin Turbidity
        # Turb_array_test[k] = obj_model_test.run(u_k = 0) 
        # Turb_array_test[k] = obj_model_test.run(u_k = PIX_array_test[k]) 
        Turb_array_test[k], *restArray = obj_MIMOmodel_test.run(u_pix = PIX_array_test[k],
#                                                                u_pax = 0,
#                                                                u_pol = 0,
                                                                u_pax = PAX_array_test[k] if len(u_guess) >= 2 else 0,
                                                                u_pol = POL_array_test[k] if len(u_guess) >= 3 else 0,
                                                                u_ss = U_SS_test[k],
                                                                u_flow = U_flow_test[k])
        #%% simulatin Alkalinity
        Alkalinity_array_test[k], *restArray = obj_Alkalinity_test.run(u_pix = PIX_array_test[k],
#                                                                u_pax = 0,
#                                                                u_pol = 0,
                                                                u_pax = PAX_array_test[k] if len(u_guess) >= 2 else 0,
                                                                u_pol = POL_array_test[k] if len(u_guess) >= 3 else 0,
                                                                u_ss = U_SS_test[k],
                                                                u_flow = U_flow_test[k])
        #%% simulatin Phosphate
        Phosphate_array_test[k], *restArray = obj_Phosphate_test.run(u_pix = PIX_array_test[k],
#                                                                u_pax = 0,
#                                                                u_pol = 0,
                                                                u_pax = PAX_array_test[k] if len(u_guess) >= 2 else 0,
                                                                u_pol = POL_array_test[k] if len(u_guess) >= 3 else 0,
                                                                u_ss = U_SS_test[k],
                                                                u_flow = U_flow_test[k])
        
    #|||||||||||||||||||||||||||||||||||||||||#
    #%%    calculating objective equation     #
    #|||||||||||||||||||||||||||||||||||||||||#
# =============================================================================
# calculating model error
# =============================================================================
    # modelError = np.sum((SP_TURB_array_test-Turb_array_test)**2)
    turbError = np.clip((SP_TURB_array_test-Turb_array_test), 0, np.inf)
    modelError = np.sum(turbError**2)
#     modelError = np.sum(abs(SP_TURB_array_test-Turb_array_test)**2)
    avgError = np.average(abs(SP_TURB_array_test-Turb_array_test))
    
# =============================================================================
# calculating alkalinity
# =============================================================================
    alkalinityError = np.sum((Alkalinity_array_test)**2)
    
# =============================================================================
# calculating phosphate error
# =============================================================================
    phosphateError = np.sum((SP_PHOSPHATE_array_test - Phosphate_array_test)**2)
    
# =============================================================================
# calculating chemical economical cost
# =============================================================================
    paxcost = np.sum(PAX_array_test * 0)**2
    pixcost = np.sum(PIX_array_test * 0)**2
    polcost = np.sum(POL_array_test * 0)**2
# =============================================================================
# Summating all values for J
# =============================================================================
    J = modelError + alkalinityError + phosphateError + paxcost + pixcost + polcost

    #|||||||||||||||||||||||||||||||||||||||||#
    #%%       PLOTTING THE SIMULATION         #
    #|||||||||||||||||||||||||||||||||||||||||#
    if RUN_PLOT:
        plt.figure(2)
        plt.title("U:{} \nY:{} \nSP:{} \nerror:{:0.2f} \nFrom OBJ.FUNK".format(U_PIX_blocks_test, np.average(Turb_array_test), PIX_array_test[-1], modelError))
        plt.plot(pred_horizion_array_test,PIX_array_test,label="input PIX")
        plt.plot(pred_horizion_array_test,PAX_array_test,label="input PAX") if len(u_guess) >= 2 else None
        plt.plot(pred_horizion_array_test,POL_array_test,label="input POL") if len(u_guess) >= 3 else None
        plt.plot(pred_horizion_array_test,SP_TURB_array_test,label="TURB setpoint")
        plt.plot(pred_horizion_array_test,Turb_array_test,label="TURB Output")
        plt.plot(pred_horizion_array_test,Alkalinity_array_test,label="Alkalinity Output")
        plt.plot(pred_horizion_array_test,Phosphate_array_test,label="Phosphate Output")
        plt.plot(pred_horizion_array_test,U_SS_test,label="U_SS_test")
        
        plt.legend(bbox_to_anchor = [1, 1])
        plt.grid()
        plt.show()
    

    
    #|||||||||||||||||||||||||||||||||||||||||#
    #%%       Dumping array to file        #
    #|||||||||||||||||||||||||||||||||||||||||#
    try:
        filename = 'predArray.data'
        with open(filename,"wb") as datafile:
        # with open(r"estdatafile.data","wb") as datafile:
            arrays = (pred_horizion_array_test, 
                      Turb_array_test, 
                      SP_TURB_array_test,
                      Alkalinity_array_test,
                      Phosphate_array_test,
                      SP_PHOSPHATE_array_test,
                      PIX_array_test, 
                      PAX_array_test, 
                      POL_array_test, 
                      U_SS_test, 
                      modelError, 
                      avgError
                      )
            pickle.dump(arrays, datafile)
        # datafile.close()
    except FileNotFoundError as fnf_error:
        print(fnf_error) 
    except:
        print('Could not open',filename)
    return J


#%% RUNNING CODE
###################################################################
# CODE BELOW THIS LINE IS ONLY FOR ISOLATED TESTING THE CODE ABOVE
###################################################################
if __name__ == "__main__":
    import numpy as np
   # import matplotlib.pyplot as plt
    start = 0
    stop = 150
    dt = 0.1
    ns = int((stop-start)/dt)+1
    
    time = np.linspace(start,stop,ns)
    Y = time * 0
    SS_test = np.sin(2*np.pi*time/120)+11
    
    
    
    U_TURB_PIX_INITIAL = [2,2]
    U_TURB_PAX_INITIAL = [0,0]
    U_TURB_POL_INITIAL = [2,2]
    
    U_TURB_PIX_INITIAL = [2,2]
    U_TURB_PAX_INITIAL = [0,0]
    U_TURB_POL_INITIAL = [2,2]
    
    U_TURB_PIX_INITIAL = [2,2]
    U_TURB_PAX_INITIAL = [0,0]
    U_TURB_POL_INITIAL = [2,2]
    
    initControlSignals_test = [U_TURB_PIX_INITIAL, U_TURB_PAX_INITIAL, U_TURB_POL_INITIAL, SS_test]
    
    turbInitStateValue_test = [U_TURB_PIX_INITIAL, U_TURB_PAX_INITIAL, U_TURB_POL_INITIAL, SS_test[0]]
    
    alkalinityInitStateValue_test = [U_TURB_PIX_INITIAL, U_TURB_PAX_INITIAL, U_TURB_POL_INITIAL, SS_test[0]]
    
    phosphateInitStateValue_test = [U_TURB_PIX_INITIAL, U_TURB_PAX_INITIAL, U_TURB_POL_INITIAL, SS_test[0]]
    
    
    
    u_guess = [2,0,8,0.2],[0.6,0.7,0.8,0.9],[0.10,0.11,0.12,0.13]
    u_guess = np.concatenate(u_guess)
    result =  objectiveFunction(u_guess,
                                dt,        # dt
                                2,          # SP
                                100,        # PredTime
                                initControlSignals_test,  # initControlSignals_test
                                turbInitStateValue_test, # initStateValue
                                alkalinityInitStateValue_test, # initStateValue
                                phosphateInitStateValue_test, # initStateValue
                                4,          # number of blocks
                                1           # RUN_PLOT
                                )
    print("RESULTING ERROR: ",result)