
class mpc:
    def __init__(self, dt, pred_horizion_length, NumberOfBlocks):
        import model
        # Defining values
        self.dt = dt
        self.pred_horizion_length = pred_horizion_length # [Sec]
        self.NumberOfBlocks = NumberOfBlocks # [stk]
        self.setpoint = 1
        self.u_opt = 0
        # Defining Arrays
        self.initial_guess = 0
        self.U_guess = [None for i in range(NumberOfBlocks)]
        
        ################
        # Initiating modelobject to be simulated
        self.obj_model_test = model.secDegModel(dt = self.dt,
                                      K = 4,
                                      Tc1 = 30,
                                      Tc2 = 60,
                                      timeDelay = 50,
                                      initStateValue = 0,
                                      initDelayValue = 0
                                      )
        return
    
    def run(self, SP, state):
        import functions
        from scipy.optimize import minimize
        # values to be tested
        U_guess = self.u_opt
        # values that should be sendt as arguments trough the optimizer
        self.setpoint =  SP
        arg_guess = ( self.dt, self.setpoint, self.pred_horizion_length, state, self.obj_model_test)
        self.solution_guess = minimize(functions.objectiveFunction_TEST,
                                  U_guess,
                                  arg_guess,
                                  callback= None,
                                  method = "SLSQP")
        self.u_opt = self.solution_guess.x[0]
        return self.u_opt
    
    def showPred(self):
        return

if __name__ == "__main__":
    from scipy.optimize import minimize
    import numpy as np
    # import matplotlib.pyplot as plt
    start = 0
    stop = 10
    dt = 0.1
    ns = int((stop-start)/dt)+1
    
    time = np.linspace(start,stop,ns)
    Y = time * 0
    
    
    #objectiveFunction(1,0.1,2,200)
    
    obj_mpc = mpc(dt = dt, pred_horizion_length = 300, NumberOfBlocks = 3)
    print("obj_mpc.u_opt ",obj_mpc.u_opt)
    print("obj_mpc.run(3)",obj_mpc.run(2,3))
    print("obj_mpc.u_opt ",obj_mpc.u_opt)