# This script handles downloading up-to-date
# stock-data 7.000 stock ticker from
# Alpha Vantage.

setwd("G:/My Drive/SPECIALE/R")
library(quantmod)


tickers <- read.csv2("MetaDataETF.csv", sep=",", header=TRUE)
library(dplyr)
tickers <- select(tickers, symbol)

# Premium API key is I4V4W8H5M93K8K27
setDefaults(getSymbols.av, api.key="I4V4W8H5M93K8K27")

symbols <- as.vector(tickers$symbol)
length(symbols)
data <- symbols

remove <- -c(81,139,170,197,236,244,347,359,360,411,510,519,571,634,696,705,714,758,856,879,917,1017,1098,1099,1121,1144,1156,1217,1541,1572,1635,1642,1649,1683,1721,1752,1794,1814,1849)
# Remove
# i = 81
# i = 139
# i = 170
# i = 197
# i = 236
# i = 244
# i = 347
# i = 359
# i = 360
# i = 411
# i = 510
# i = 519
# i = 571
# i = 634
# i = 696
# i = 705
# i = 714
# i = 758
# i = 856
# i = 879
# i = 917
# i = 1017
# i = 1098
# i = 1099
# i = 1121
# i = 1144
# i = 1156
# i = 1217
# i = 1541
# i = 1572
# i = 1635
# i = 1642
# i = 1649
# i = 1683
# i = 1721
# i = 1752
# i = 1794
# i = 1814
# i = 1849

match(c("PRN"),data)

data <- data[data!="FINQ"]
data <- data[data!="PRN"]

for(j in 43:63) {
    
      times <- Sys.time()
  
      for(i in (1+30*j):(30*j+30)) {
        
      filename <- as.character(data[i])
      
      #ERROR HANDLING
      possibleError <- tryCatch(
        assign(filename, getSymbols(data[i], src="av", output.size="full", periodicity="daily", adjusted=TRUE, auto.assign=FALSE)),
        error=function(e) e
      )
      if(!inherits(possibleError, "error")) {
        #REAL WORK
        assign(filename, getSymbols(data[i], src="av", output.size="full", periodicity="daily", adjusted=TRUE, auto.assign=FALSE))
        save(list=c(filename), file=paste(paste("ETFs/",filename, sep=""), ".rda", sep=""))
        rm(list=data[i])
      }
     
      else if(inherits(possibleError, "warning")) {
        print(paste("No data: Warning for i = ", i, sep=""))
      }
      else{
        print(paste("No data: Error for i = ", i, sep=""))
      }
      
      # How much time is left?
      print(paste("Percent left:", as.character(round((1 - i/1920)*100),0), "%"))

    }
    
    
    # This is because the API can only take 30 calls per minute.
    if((60 - (Sys.time() - times))>0) {
      sleep <- 60 - (Sys.time() - times)
    } else {
      sleep <- 0
      }
    Sys.sleep(sleep)
    

}

  
for(i in 1921:1926) {
    filename <- as.character(data[i])
    assign(filename, getSymbols(data[i], src="av", output.size="full", periodicity="daily", adjusted=TRUE, auto.assign=FALSE))
    save(list=c(filename), file=paste(paste("ETFs/",filename, sep=""), ".rda", sep=""))
    rm(list=data[i])
}

# Data for 1857 ETFs