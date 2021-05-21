list.files()
#try(setwd(dirname(attr(body(function() {}),'srcfile')$filename)))
setwd('D:\\Mrstrlen\\Graduation_Project\\R_Code')
#setwd('D:\\Vaa3D_QPH\\vaa3d_tools\\hackathon\\Graduation_Project\\R_Code')
rm(list=ls())

library(fpc)
library(cluster)
df<-read.csv('..\\Temp\\heat_value.csv', header=F,sep=',')
x<-dim(df)
if(x[1]>20){
  len=20
}else{
  len=x[1]
}
asw <- numeric(len)
for (k in 2:(len-1))
  asw[[k]] <- pam(df, k) $ silinfo $ avg.width
#plot(asw)
k.best <- which.max(asw)
aswt<-pam(df,k.best)
# plot(aswt[["clustering"]])
write.csv(aswt[["clustering"]],"..\\Temp\\Cluster_Result.csv")
