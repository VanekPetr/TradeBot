"""
Created on Wed Nov 11 15:50:42 2020

@author: Petr Vanek
"""
import numpy as np

from dataAnalyser import analyseData, getStat, finalStat
from dataGraph import plotInteractive, plotOptimization
from MST import MinimumSpanningTree
from Clustering import Cluster, pickCluster
from ScenarioGeneration import MC, BOOT
from CVaRtargets import targetsCVaR
from CVaRmodel import modelCVaR

from pandas_datareader import data


# WHAT TIME PERIOD DO WE WANT WORK WITH?
#------------------------------------------------------------------
startDate = "2015-09-23"
endDate = "2020-09-22"
#thesis dates:  startDate ="2016-07-25" & endDate = "2020-04-30"

tickers = ["BABA", "AAPL", "SPY", "AOA", "IGE", "IXC", "VDE", "IUSB", "ISTB",
           "VCSH", "VT", "VTI", "XBI", "FBT", "PALL", "PGX", "ANGL", "PGF",
           "XMLV", "IGV", "IHI"]

"""
    ----------------------------------------------------------------------
    DATA ANALYTICS AND VISUALISATION 
    ----------------------------------------------------------------------
"""
# DOWNLOAD THE DATA FROM YAHOO DATABASE
#------------------------------------------------------------------
dailyPrices = data.DataReader(tickers, 'yahoo', startDate, endDate)
dailyPrices = dailyPrices["Adj Close"]
    

# ANALYSE THE DATA AND GET WEEKLY RETURNS  
#------------------------------------------------------------------
dataStat, weeklyReturns = analyseData(data = dailyPrices,
                                      startDate = startDate,
                                      endDate = endDate) 
weeklyReturns

# PLOT INTERACTIVE GRAPH
#------------------------------------------------------------------
plotInteractive(data = dataStat,
                start = startDate,
                end = endDate,
                ML = None, MLsubset = None)



"""
    ----------------------------------------------------------------------
    MACHINE LEARNING AND ADVANCED STATISTICAL METHODS
    ----------------------------------------------------------------------
""" 
# DIVIDE DATASET INTO TRAINING AND TESTING PART?
#------------------------------------------------------------------
divide = True

# IF WE DIVIDE DATASET
if divide != False:
    # ONE HALF OF THE DATA, BREAKPOINT IN TRAINING AND TESTING DATASET
    breakPoint = int(np.floor(len(weeklyReturns.index)/2))
    # DEFINITION OF TRAINING AND TESTING DATASETS
    trainDataset = weeklyReturns.iloc[0:breakPoint,:] 
    testDataset = weeklyReturns.iloc[breakPoint:,:] 
    
    dataPlot = getStat(data = trainDataset)
    endTrainDate = str(trainDataset.index.date[-1])
    startTestDate = str(testDataset.index.date[0])
    lenTest = len(testDataset.index)
else: 
    trainDataset = weeklyReturns
    dataPlot = dataStat
    lenTest = 0
    

# RUN THE MINIMUM SPANNING TREE METHOD
#------------------------------------------------------------------
nMST = 1                        # Select how many times run the MST method   
subsetMST_df = trainDataset
for i in range(nMST):
    subsetMST, subsetMST_df, corrMST_avg, PDI_MST = MinimumSpanningTree(subsetMST_df)

    
# PLOT
plotInteractive(data = dataPlot,
                ML = "MST", 
                MLsubset = subsetMST,
                start = startDate,
                end = endTrainDate)
    
 
# RUN THE CLUSTERING METHOD 
#------------------------------------------------------------------
clusters = Cluster(trainDataset,
                   nClusters = 3,
                   dendogram = False)
    
# SELECT ASSETS
subsetCLUST, subsetCLUST_df = pickCluster(data = trainDataset,
                                          stat = dataPlot,
                                          ML = clusters,
                                          nAssets = 3)

# PLOT
plotInteractive(data = dataPlot,
                ML = "Clustering", 
                MLsubset = clusters,
                start = startDate,
                end = endTrainDate)
    
    

"""
    ----------------------------------------------------------------------
    SCENARIO GENERATION
    ----------------------------------------------------------------------
""" 

# THE BOOTSTRAPPING SCENARIO GENERATION 
#------------------------------------------------------------------
# FOR THE MST METHOD
BOOT_sim_MST = BOOT(data = weeklyReturns[subsetMST],    #subsetMST or subsetCLUST
                nSim = 250,                             #number of scenarios per period
                N_test = lenTest) 


# FOR THE CLUSTERING METHOD
BOOT_sim_CLUST = BOOT(data = weeklyReturns[subsetCLUST],#subsetMST or subsetCLUST
                      nSim = 250,
                      N_test = lenTest) 

# THE MONTE CARLO SCENARIO GENERATION 
#------------------------------------------------------------------
# FOR THE MST METHOD
MC_sim_MST = MC(data = subsetMST_df,                    #subsetMST_df or subsetCLUST_df
                nSim = 250,
                N_test = lenTest)    



# FOR THE CLUSTERING METHOD  
MC_sim_CLUST = MC(data = subsetCLUST_df,                #subsetMST_df or subsetCLUST_df
                  nSim = 250,
                  N_test = lenTest)  


"""
    ----------------------------------------------------------------------
    MATHEMATICAL OPTIMIZATION
    ----------------------------------------------------------------------
""" 
# TARGETS GENERATION
#------------------------------------------------------------------
targets, benchmarkPortVal = targetsCVaR(start_date = startDate,
                                        end_date = endDate,
                                        test_date = startTestDate,
                                        benchmark = ["SPY"],   #Credit Suisse Floating Rate
                                        test_index = testDataset.index.date,
                                        budget = 100,
                                        cvar_alpha=0.05) 


# MATHEMATICAL MODELING
#------------------------------------------------------------------
portAllocation, portValue, portCVaR = modelCVaR(testRet = testDataset[subsetMST],
                                                scen = BOOT_sim_MST,
                                                targets = targets,
                                                budget = 100,
                                                cvar_alpha = 0.05,
                                                trans_cost = 0.001,
                                                max_weight = 0.5)

# PLOTTING
#------------------------------------------------------------------
plotOptimization(performance = portValue,
                 performanceBenchmark = benchmarkPortVal,
                 composition = portAllocation)



# STATISTICS
#------------------------------------------------------------------
finalStat(portValue.iloc[0:100]) 
finalStat(benchmarkPortVal.iloc[0:100])
