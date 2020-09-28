#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 22:10:50 2020

@author: Petr Vaněk

HOW TO USE IT:
1, Load data from the AlphaVantage by the R code and 
   save it into TradeBot folderex
2, Download USD/EUR rates and save it into folder as USD_EUR.csv
3, Run this code
"""

# LIBRARY
#------------------------------------------------------------------
from DataManipulation import loadData
from DataManipulation import dueDiligence
from DataManipulation import compoundRet
from ScenarioGeneration import MC
from ScenarioGeneration import BOOT
from Targets import cvarTar


###################################################################
###                          MAIN CODE                          ###
###################################################################

# DATA MANIPULATION
#------------------------------------------------------------------
RawData = loadData("ETFdataNewer")      # Load the raw weekly data
WeeklyData = dueDiligence(RawData)      # Due Diligence on raw data
FourWeekRet = compoundRet(WeeklyData,nTrainWeeks = 97)   # 4-week (monthly) returns

# SCENARIO GENERATION
#------------------------------------------------------------------
BOOT_sim = BOOT(WeeklyData, nTrainWeeks = 97, nSim = 250)   # The Bootstrapping Method 
MC_sim = MC(WeeklyData, nTrainWeeks = 97, nSim = 250)       # The Monte Carlo Method
                                                            # Pandas?
# CVaR TARGETS
#------------------------------------------------------------------
CVaR_tarets = cvarTar(FourWeekRet, MC_sim)
                                                           
# CVaR MODEL
#------------------------------------------------------------------ 


# PERFORMANCE MEASURES
#------------------------------------------------------------------ 
# The Performance.py needs to be modified
                                                            
            









