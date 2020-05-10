###########################################
#|||||||||||||||||||||||||||||||||||||||||#
#     IMPORT ALL NEEDED LIBS.             #
#|||||||||||||||||||||||||||||||||||||||||#
###########################################
import numpy as np
import matplotlib.pyplot as plt
# Loading optimization module
from scipy import optimize
import time as TIME
import datetime



###########################################
#|||||||||||||||||||||||||||||||||||||||||#
#       DEFINING SIMULATION SETUPS        #
#       TIME SPAN                         #
#       NUMBER OF VALUES                  #
#       INPUT ARRAYS                      #
#       ETC.                              #
#|||||||||||||||||||||||||||||||||||||||||#
###########################################

start = 0
stop = 800
dt = 0.1
ns = int((stop-start)/dt + 1) 
time = np.linspace(start,stop,ns)
print("len(time): ",len(time),"stk\ntime[-1]: ",time[-1],"\ndt: ",dt,"s\nns: ",ns)

# Defining In/Out-putArrays
U = np.ones(len(time))
U[int(200/dt):] = 0
U[int(400/dt):int(500/dt)] = np.linspace(0,0.5,int(100/dt))
U[int(500/dt):int(600/dt)] = np.linspace(0.5,0,int(100/dt))


###########################################
#|||||||||||||||||||||||||||||||||||||||||#
#     SIMULATION OF "REAL" SYSTEM         #
#|||||||||||||||||||||||||||||||||||||||||#
###########################################
Y = np.zeros(len(time))
Y2 = np.zeros(len(time))

#PARAMETERS
timeDelay = 10
initDelayValue = 0
K = 2
Tc1 = 30
Tc2 = 60
# Timedelay parameters 
timeDelayArrayLength = int(round(timeDelay/dt)) + 1
delay_array = np.zeros(timeDelayArrayLength)+initDelayValue

# Running simulation of "real" model function
for k in range(1,len(time)):
        #Timedelay calculation
        u_out = delay_array[-1]
        delay_array[1:] = delay_array[0:-1]
        delay_array[0] = U[k]
        
        #Model calculation
        u_out *= K
        Y[k] = (((dt*K)/(Tc1+dt))*u_out) + ((Tc1/(Tc1+dt))*Y[k-1])        
        #Model calculation
        Y2[k] = (((dt)/(Tc2+dt))*Y[k]) + ((Tc2/(Tc2+dt))*Y2[k-1])

#      DONE SIMULATING "REALSYSTEM"       #
#|||||||||||||||||||||||||||||||||||||||||#

###########################################
#|||||||||||||||||||||||||||||||||||||||||#
#     Defining the objective function     #
#|||||||||||||||||||||||||||||||||||||||||#
###########################################
def ObjectiveFunction(x, *args):
    
    tic_test = TIME.time()
    global odc
    
    # KNOWN ARRAYS & VARIABLES
    U_test_array = args[0]
    Y_referece = args[1]
    avg_time_list = args[2]
        
    #PARAMETERS
    K_test = x[0]
    delayTime_test = x[1]
    Tc1_test = x[2]
    Tc2_test = x[3]
    
    # TESTING ARRAYS
    y_test_array = np.zeros(len(U_test_array))
    y2_test_array = np.zeros(len(U_test_array))
    
    # Timedelay parameters 
    timeDelayArrayLength_test = max(int(delayTime_test/dt) + 1,1)
    delay_array_test = np.zeros(timeDelayArrayLength_test)+initDelayValue
    
    # Running model functions
    for k in range(1,len(time)):
        #Timedelay calculation
        u_opt_out = delay_array_test[-1]
        delay_array_test[1:] = delay_array_test[0:-1]
        delay_array_test[0] = U_test_array[k]
        
        #Model calculation
        u_opt_out *= K_test 
        y_test_array[k] = (((dt)/(Tc1_test + dt)) * u_opt_out) + ((Tc1_test/(Tc1_test + dt))*y_test_array[k-1])
        y2_test_array[k] = (((dt)/(Tc2_test + dt)) * y_test_array[k]) + ((Tc2_test/(Tc2_test + dt))*y2_test_array[k-1])
    
    #calculatin error
    error_array = abs(Y_referece-y2_test_array) # calculating error using vector subtracion and getting an array with one error value for every timestep
    error_value = error_array.sum() # Cal
    
    #####################################
    #  CALCULATING TIME INFORMATION     #
    #  Just for information while       #
    #  optimization excecution          #
    #####################################
    toc_test = TIME.time()
    time_since_start = int(toc_test - tic)
    time_since_start = str(datetime.timedelta(seconds=time_since_start))
    total_runtime = (toc_test - tic_test)*(tot_iter) + 30 # 30 is added since "fine tuning" takes longer time 
    
    #Calculate average time of one execution
    if odc < len(avg_time_list):
        avg_time_list[odc:] = total_runtime
    avg_runtime = int(sum(avg_time_list)/len(avg_time_list))
    med_runtime = datetime.timedelta(seconds = int(np.median(avg_time_list)))
    total_runtime = str(datetime.timedelta(seconds = avg_runtime))

    print(f"""\r Time: {time_since_start}/{total_runtime}  median:{med_runtime} - K_opt = {float(x[0]):.2f}, TimeDelay_opt = {float(x[1]):.2f}, Tc1_opt = {float(x[2]):.2f}, Tc2_opt = {float(x[3]):.2f}\r         """,
          end="",
          flush=True )
    odc += 1
    
    #####################################
    #     RETURN OBJECTIVE VALUE        #
    return error_value
    #####################################

###########################################
#|||||||||||||||||||||||||||||||||||||||||#
#            USING BRUTEFORCE             #
#|||||||||||||||||||||||||||||||||||||||||#
#                                         #   
#   * All parrameters are defined in      #
#     slices, one for each parremter      #
#     where each slice is defined as      #
#     (where to start, where to stop and  #
#      how big the jump should be)        #
#   * Then all slices are stored in to    #
#     one tuple, called ranges. this is   #
#     then put as a parrameter to the     #
#     optimization algorithem.            #
#   * All arrays and variables that is    #
#     not intended to be changed is       #
#     stored in to a tuple called args    #
#     and used the same way as ranges     #
#                                         #
#|||||||||||||||||||||||||||||||||||||||||#
###########################################
# odc is a global variable used to count how manny executions the optimization algorithem does
odc = 0
# avg_time_list is a list for storing the time om each execution, to later be calculated the average execution time
avg_time_list = np.array([ 0 for i in range(250)])

param1_start, param1_stop, param1_jump = 0,4,0.5  # parameter #1 = K
param2_start, param2_stop, param2_jump = 8,12,0.5 # parameter #2 = timedelay
param3_start, param3_stop, param3_jump = 3,7,0.5  # parameter #3 = Tc1
param4_start, param4_stop, param4_jump = 3,7,0.5  # parameter #4 = Tc2
tot_iter = ((param1_stop-param1_start) / param1_jump*
            (param2_stop-param2_start) / param2_jump*
            (param3_stop-param3_start) / param3_jump*
            (param4_stop-param4_start)/param4_jump)

ranges = (slice(param1_start,param1_stop,param1_jump), # parameter #1 = K
          slice(param2_start,param2_stop,param2_jump), # parameter #2 = timedelay
          slice(param3_start,param3_stop,param3_jump), # parameter #3 = Tc1
          slice(param4_start,param4_stop,param4_jump)) # parameter #4 = Tc2

# Arrays to be sendt in to the optimizer
args = (U,Y2,avg_time_list)



tic = TIME.time() # starting timer befor optimization, to check how long time it takes
optimizedResult = optimize.brute(ObjectiveFunction, ranges, args, full_output = False)
toc = TIME.time() # Ending the timer when optimization is finished

# FOUND OPTIMAL PARAMETERS
K_opt = optimizedResult[0]
delayTime_opt = optimizedResult[1]
Tc1_opt = optimizedResult[2]
Tc2_opt = optimizedResult[3]

#K_opt = 0.21654856845621
#delayTime_opt = 0.21654856845621
#Tc1_opt = 0.21654856845621
#Tc2_opt = 0.21654856845621

#          DONE BRUTEFORCEING             #
#|||||||||||||||||||||||||||||||||||||||||#


# CALCULATING TOTAL EXECUTION TIME
total_exe_time = toc-tic
total_exe_time = str(datetime.timedelta(seconds=int(total_exe_time)))
print()
print()
print(f"Total runtime: {total_exe_time} ->")
print(f"    K = {K:.2f},\t    TimeDelay = {timeDelay}, \t     Tc1 = {Tc1:.2f}, \t     Tc2 = {Tc2:.2f}")
print(f"K_opt = {K_opt:.2f}, \tTimeDelay_opt = {delayTime_opt:.2f},\t Tc1_opt = {Tc1_opt:.2f},\t Tc2_opt = {Tc1_opt:.2f}")

Y_opt = np.zeros(len(time))
Y2_opt = np.zeros(len(time))


#####################################
#|||||||||||||||||||||||||||||||||||#
#     PLOTING OPTIMAL SOLUTION      #
#|||||||||||||||||||||||||||||||||||#
#####################################
#Timedelay parameters 
timeDelayArrayLength_opt = int(round(delayTime_opt/dt)) + 1
delay_array_opt = np.zeros(timeDelayArrayLength_opt)+initDelayValue


# Running OPTIMAL PARAMERER-model function

for k in range(1,len(time)):
        #Timedelay calculation
        u_out = delay_array_opt[-1]
        delay_array_opt[1:] = delay_array_opt[0:-1]
        delay_array_opt[0] = U[k]
        
        #Model calculation
        u_out*=K_opt
        Y_opt[k] = (((dt)/(Tc1_opt + dt)) * u_out) + ((Tc1_opt/(Tc1_opt + dt))*Y_opt[k-1])
        Y2_opt[k] = (((dt)/(Tc2_opt + dt)) *  Y_opt[k]) + ((Tc2_opt/(Tc2_opt + dt))*Y2_opt[k-1])
        

plt.figure(figsize=[16,8])
plt.title(f"K:{K}[{K_opt:.2f}], Tc1:{Tc1} [{Tc1_opt:.2f}], Tc2:{Tc2} [{Tc2_opt:.2f}], timedelay:{timeDelay} [{delayTime_opt:.2f}]")
plt.plot(time,U,label="U")
#plt.plot(time,Y,"--",label="Y (first order)")
plt.plot(time,Y2,"--",label="Y2 (second order)")
plt.plot(time,Y2_opt,"",label="Y_opt (optimized solution)")
plt.xlabel("Time (sec)")
plt.ylabel("")
plt.grid(True)
plt.legend()
plt.show()