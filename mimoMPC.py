class container:
    def __init__(self):
        self.arrayY = None
        self.arrayU = None
        self.arraySP = None
        return None
    def saveArray(self,arrayY,arrayU,arraySP):
        self.arrayY = arrayY
        self.arrayU = arrayU
        self.arraySP = arraySP
        return None
class mpc:
    def __init__(self, dt, pred_horizion_length, initDelayValue_test = 10, initStateValue_test = 2 ):
        import model
        # Defining values
        self.dt = dt
        self.pred_horizion_length = pred_horizion_length # [Sec]
        self.setpoint = 1
        self.u_opt = [0,0,0]
        self.initDelayValue_test = initDelayValue_test
        self.initStateValue_test = initStateValue_test
        self.obj_container = container
        return
    
    def run(self, SP, state):
        import functions
        from scipy.optimize import minimize
        # values to be tested
        U_guess = self.u_opt
        # values that should be sendt as arguments trough the optimizer
        self.setpoint =  SP
        arg_guess = (self.dt, 
                     self.setpoint, 
                     self.pred_horizion_length,
                     self.initStateValue_test,
                     self.initDelayValue_test,
                     )
        self.ub = 10
        self.lb = 20
        self.u_bounds = [(self.ub,self.lb) for x in range(len(U_guess))]
        # Run Optimizer
        self.solution_guess = minimize(functions.objectiveFunction,
                                  U_guess,
                                  arg_guess,
                                  bounds = self.u_bounds,
                                  callback= None,
                                  method = "SLSQP")
        # Save Optimal solution
        self.u_opt = self.solution_guess.x
        print(self.solution_guess.x[0])
        return self.u_opt[0]
    

if __name__ == "__main__":
    from scipy.optimize import minimize
    import numpy as np
    import pickle
    import matplotlib.pyplot as plt
    
    start = 0
    stop = 1000
    dt = 0.1
    ns = int((stop-start)/dt)+1
    
    # DEFINING ARRAYS
    time = np.linspace(start,stop,ns)
    Y = time * 0
    
    
    #objectiveFunction(1,0.1,2,200)
    
    obj_mpc = mpc(dt = dt, pred_horizion_length = 100)
    print("obj_mpc.u_opt ",obj_mpc.u_opt)
    print("obj_mpc.run(3)",obj_mpc.run(3,2))
    print("obj_mpc.u_opt ",obj_mpc.u_opt)
    
    
    with open("predArray.data","rb") as datafile:
        predArrays = pickle.load(datafile)

    predTime, predU, predY, predSP = predArrays
    plt.plot(predTime, predU,'b-',linewidth=2,label='Predicted input')
    plt.plot(predTime, predY,'k-',linewidth=2,label='Predicted output ')
    plt.plot(predTime, predSP,'r-',linewidth=2,label='Setpoint')
    plt.legend()
    
    print(len(predArrays[0]))
    
    
    
    
    
    
    