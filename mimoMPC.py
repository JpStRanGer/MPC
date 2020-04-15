import numpy as np
import mimoFunctions
from scipy.optimize import minimize
import model

class mpc:
    def __init__(self, dt, pred_horizion_length, numberOfIntputs, numberOfBlocks = 2  ):
        # Defining values
        self.dt = dt
        self.pred_horizion_length = pred_horizion_length # [Sec]
        self.setpoint = 1
        # self.u_opt = [2,2,4,3,2],[0,0,0,0,0]
        self.u_opt = [[0 for block in range(numberOfBlocks)] for input in range(numberOfIntputs)]
        self.numberOfBlocks = numberOfBlocks
        self.numberOfInputs = len(self.u_opt)
        return
    
    def run(self, SP, state, RUN_PLOT = 0):
        import numpy as np
        #import mimoFunctions
        from scipy.optimize import minimize
        self.RUN_PLOT = RUN_PLOT
        # values to be tested
        U_guess = self.u_opt
        # ORGANISE VALUES
        self.initStateValue_test = state
        self.initDelayValue_test = state
        # values that should be sendt as arguments trough the optimizer
        self.setpoint =  SP
        arg_guess = (self.dt, 
                     self.setpoint, 
                     self.pred_horizion_length,
                     self.initStateValue_test,
                     self.numberOfBlocks,
                     self.RUN_PLOT
                     )
        self.ub = 0
        self.lb = 20
        # self.u_bounds = [(self.ub,self.lb) for x in range(len(U_guess))]
        self.u_bounds = [(self.ub,self.lb) for x in range(np.size(self.u_opt))]
        # Run Optimizer
        self.solution_guess = minimize(mimoFunctions.objectiveFunction,
                                      U_guess,
                                      arg_guess,
                                      bounds = self.u_bounds,
                                      callback= None,
                                      method = "SLSQP")
        # Save Optimal solution
        self.u_opt = np.reshape(self.solution_guess.x,[self.numberOfInputs,-1]) # make the array back to 2 dim (rows seperating inputs)
        print("\n\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/")
        print("self.numberOfInputs: ",self.numberOfInputs)
        print("self.solution_guess.x[0]: ",self.solution_guess.x[0])
        print("self.solution_guess:\n ",self.solution_guess.x)
        print("self.u_opt: ",self.u_opt)
        print("RETURNING OUT OF MPC: ",np.transpose(self.u_opt)[0])
        print("\n\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/")
        
        # Returning the first optimal control output from every control variable
        return np.transpose(self.u_opt)[0]
    
###################################################################
# CODE BELOW THIS LINE IS ONLY FOR ISOLATED TESTING THE CODE ABOVE
###################################################################
if __name__ == "__main__":
    from scipy.optimize import minimize
    import numpy as np
    import pickle
    import matplotlib.pyplot as plt
    import time as TIME
    
    start = 0
    stop = 1000
    dt = 0.1
    ns = int((stop-start)/dt)+1
    
    # DEFINING ARRAYS
    time = np.linspace(start,stop,ns)
    Y = time * 0
    
    
    #objectiveFunction(1,0.1,2,200)
    obj_mpc = mpc(dt = dt, numberOfIntputs = 1, pred_horizion_length = 180)
    
    
    tic = TIME.time()
    result = obj_mpc.run(SP = 15, state = [100,30,3] , RUN_PLOT = 1)
    toc = TIME.time()
    exeTime = toc - tic
    
    print("\n##################  OPTIMAL VALUES ##################\n",result,"\n######################################################\n")
    
    with open("predArray.data","rb") as datafile2:
        predArrays = pickle.load(datafile2)

    predTime, predTURB, predSP, predPIX, predSS, predError, avgError = predArrays
    
    fig, ax = plt.subplots(nrows=2,ncols=1, figsize = [10,10])
    fig.suptitle("From mimoMPC.py\ntotal Error: {:0.2f} Average Error: {:0.2}\ntime of one prediction: ".format(predError,avgError) + str(exeTime))#
    fig.tight_layout(pad=10, w_pad=0, h_pad=2.5)
    ax[0].set_title("Inputs")
    ax[0].set_ylabel('L/s')
    ax[0].set_xlabel('min')
    ax[0].plot(predTime, predPIX, linewidth=1, label='Predicted PIX')
    ax[0].plot(predTime, predSS, linewidth=1, label='Predicted SS')
    ax[1].set_title("Outputs")
    ax[1].set_ylabel('Turb (FTU)')
    ax[1].set_ylim([0,30])
    ax[1].plot(predTime, predTURB,'g-', linewidth=1, label='Predicted TURB')
    ax[1].plot(predTime, predSP,'r-', linewidth=1, label='Setpoint TURB')
    
    for i in ax: i.grid(),i.legend()
    # plt.legend()
    
    print("predArrays",len(predArrays[0]))
    
    
    
    
    
    
    