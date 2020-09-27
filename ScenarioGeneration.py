"""
Scenario Generation Methods
"""

# LIBRARY
#-------------------------------------------------------------------------
import numpy as np
import math 


# THE MONTE CARLO METHOD
#-------------------------------------------------------------------------
def MC(ourData, nTrainWeeks, nSim):
    # SIZE OF OUR DATASET
    nRows = ourData.shape[0]
    nCols = ourData.shape[1]

    # TRAINING DATASET: FIRST 97 WEEKS
    ret_train = ourData.iloc[0:nTrainWeeks,0:nCols]
    # TESTING DATASET
    ret_test = ourData.iloc[nTrainWeeks:nRows,0:nCols]

    ### MONTE CARLO 
    N_test = ret_test.shape[0]
    N_iter = 4
    N_sim = nSim                            #250 scenarios for each period
    N_indices = ret_train.shape[1]

    SIGMA = np.cov(ret_train, rowvar=False)     #The covariance matrix 
    #RHO = np.corrcoef(ret_train, rowvar=False)  #The correlation matrix 
    MU = np.mean(ret_train, axis=0)             #The mean array
    #sd = np.sqrt(np.diagonal(SIGMA))            #The standard deviation
    N_rolls = math.floor((N_test)/N_iter)

    sim = np.zeros((N_test, N_sim, N_indices), dtype=float) #Match GAMS format

    print('-------Simulating Weekly Returns-------') 
    for week in range(N_test):
        sim[week, :, :] = np.random.multivariate_normal(mean = MU,cov = SIGMA,
           size = N_sim)

    monthly_sim = np.zeros((N_rolls, N_sim, N_indices))

    print('-------Computing Monthly Returns-------')
    for roll in range(N_rolls):
        roll_mult = roll*N_iter
        for s in range(N_sim):
            for index in range(N_indices):
                tmp_rets = 1 + sim[roll_mult:(roll_mult + 4), s,index] 
                monthly_sim[roll, s, index] = np.prod(tmp_rets)-1
                
    return(monthly_sim)
     