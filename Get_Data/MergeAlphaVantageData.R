# This script merges over 1.800 data files
# into one file.

setwd("G:/My Drive/SPECIALE/R")
library(xts)
library(dplyr)

# List the Files in a Directory/Folder: https://stat.ethz.ch/R-manual/R-devel/library/base/html/list.files.html
fileNames <- list.files(path = "G:/My Drive/SPECIALE/R/ETFs/", all.files = FALSE, full.names = FALSE)

# Creating variable stockTickers and rearranging the dataset, so that it's
# ready for kmeans clustering

stockTickers <- fileNames

for(i in 1:length(stockTickers)) {
  stockTickers[i] <- substr(stockTickers[i], 1, nchar(stockTickers[i])-4)
}

save(stockTickers, file="ETFtickers.rda")

load(file = as.character(fileNames[1]))
load(file = as.character(fileNames[2]))

ALTS <- ALTS[,5:6]
ALTY <- ALTY[,5:6]


dataset <- merge(ALTS,ALTY, #https://stackoverflow.com/questions/9083907/how-to-call-an-object-with-the-character-variable-of-the-same-name
      all = TRUE,
      fill = NA,
      suffixes = NULL,
      join = "outer",
      retside = TRUE,
      retclass = "xts",
      tzone = NULL,
      drop=NULL,
      check.names=NULL)

#length(fileNames)
for(i in 3:length(fileNames)) {
  load(file = as.character(fileNames[i]))
  newdata <- get(stockTickers[i])
  newdata <- newdata[,5:6]
  dataset <- merge(dataset,newdata, 
                   all = TRUE,
                   fill = NA,
                   suffixes = NULL,
                   join = "outer",
                   retside = TRUE,
                   retclass = "xts",
                   tzone = NULL,
                   drop=NULL,
                   check.names=NULL)
  print(paste("i = ", i, sep=""))
  rm(list = c(stockTickers[i])) # https://stackoverflow.com/questions/11624885/remove-multiple-objects-with-rm
}

# save(dataset, file="ETFdata.rda")