setwd('D:\\ProgramProject\\Graduation_Project\\R_Code')
rm(list=ls())

library(fpc)
library(cluster)
df<-read.csv('..\\Data\\heat_value_VPM.csv', header=F,sep=',')


asw <- numeric(20)
for (k in 2:20)
  asw[[k]] <- pam(df, k) $ silinfo $ avg.width
plot(asw)
k.best <- which.max(asw)
cat("silhouette-optimal number of clusters:", k.best, "\n")
aswt<-pam(df,k.best)
plot(aswt[["clustering"]])
