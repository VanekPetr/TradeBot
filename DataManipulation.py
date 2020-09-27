"""
Functions for Data Manipulation
"""

# LIBRARY
#-------------------------------------------------------------------------
import pandas as pd
import numpy as np
import sys

# Function which loads the data from .csv file
#-------------------------------------------------------------------------
def loadData(name):
    #READ THE .CSV DATA FILE
    df_adj = pd.read_csv("Data/" + name + ".csv",index_col=0)
    df_adj.index = pd.to_datetime(df_adj.index, dayfirst=True)

    #Save the name of the adjusted price columns
    df_columns_adj=df_adj.columns[df_adj.columns.str.endswith('Adjusted')]
    #Overwrite the old df_adj dataframe with only the adjusted price
    df_adj = df_adj[df_columns_adj]
    #Save the names of the ETFs and set as the columns names
    ETF_names = []

    for i in range(len(df_columns_adj)):
        ETF_names.append(df_columns_adj[i].split(".")[0])
    
    df_adj.columns = ETF_names       
    #Now we have to calculate the returns dataframe
    df_ret = df_adj/df_adj.shift(1)-1
    df_ret = df_ret.resample("W-WED").agg(lambda x: (x+1).prod()-1)

    #Downloaded the dataset from here: 
    #https://www.investing.com/currencies/eur-usd
    df_USDEUR=pd.read_csv("Data/USD_EUR.csv", index_col=0)
    #Change the index to datetime
    df_USDEUR.index = pd.to_datetime(df_USDEUR.index)
    df_USDEUR = df_USDEUR.sort_index()
    #The Change % column is an object, we need to change 
    #that to int and add two zeros in front of each number.
    df_USDEUR["Change %"]=df_USDEUR["Change %"].str.split('%').str[0].tolist()
    df_USDEUR["Change %"]=df_USDEUR["Change %"].astype("float64")
    df_USDEUR["Change %"] = df_USDEUR["Change %"]*0.01
    #Calculate the cumulative weekly return on USDEUR
    df_USDEUR_weekly = df_USDEUR["Change %"].resample("W-WED").agg(lambda x: (x+1).prod()-1)
    #Join the dataframes together
    df_ret=df_ret.join(df_USDEUR_weekly) 
    #And finally we want to calculate the EUR returns for the indexes.
    for i in range(0, df_ret.shape[1]-1):
        df_ret.iloc[:,i]=(df_ret.iloc[:,i]+1)*(df_ret["Change %"]+1)-1
    #Drop the change % column from the dataframe.
    df_ret = df_ret.drop(columns=["Change %"])
    #Drop all NaN rows
    df_ret = df_ret.dropna(axis=0, how='all')
    return(df_ret)

# Due Diligence of our data
#-------------------------------------------------------------------------
def dueDiligence(ourData):
    df_old=pd.read_csv("Data/out-ETFRet.csv", index_col=0)
    df_ret = ourData.loc[:,ourData.columns.isin(list(df_old.columns))]
    startdate = "17-09-2014" 
    enddate = "05-05-2020" 
    df_ret = df_ret[df_ret.index < enddate]
    df_ret = df_ret[df_ret.index > startdate]
    return(df_ret)

# Function which compounds 4-week returns
#-------------------------------------------------------------------------    
def compoundRet(ourData,nTrainWeeks):
    nPeriods = (ourData.shape[0]-nTrainWeeks)/4
    if nPeriods % 1 != 0: sys.exit("ERROR: Change number of nTrainWeeks")
    else: 
        ret = np.empty((int(nPeriods),ourData.shape[1]))
        for p in range(int(nPeriods)):
            for t in range(4*p+nTrainWeeks+1,4*(p+1)+nTrainWeeks+1):
                if t == 4*p+nTrainWeeks+1:
                    ret[p,:] = 1 + ourData.iloc[t-1,:]
                else:
                    ret[p,:] = (1+ourData.iloc[t-1,:])*ret[p,:]
            ret[p,:] = ret[p,:]-1
    
        df = pd.DataFrame(ret, columns = ourData.columns) 
    return(df)
    
    
    
    
    
    
    
    
    
    
    
    
    