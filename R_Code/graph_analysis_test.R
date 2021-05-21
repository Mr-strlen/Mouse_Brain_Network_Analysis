library(igraph)
library(dplyr)
library(heatmaply)
library(reshape2)
library(devtools)
install_github('wjrl/RBioFabric',  username='wjrl')
library(RBioFabric)

df <- read.csv("../Data/Dataset_Cell.csv",sep = " ",header=F)
soma <- read.csv("../Data/Dataset_Soma.csv",sep = " ",header=F)

df <- rename(df, Cell_id=V1)
df <- rename(df, PReg_id=V2)
df <- rename(df, axon=V3)
df <- rename(df, dendrite=V4)

soma <- rename(soma, Cell_id=V1)
soma <- rename(soma, SReg_id=V2)

df <- merge(df,soma, by="Cell_id")
plot(density(df$axon))

dfm <- df[,c(2,3,5)]

## Heatmap
#################################################################
maxon <- acast(dfm,SReg_id~PReg_id,value.var="axon",fun.aggregate=mean)
maxon <- log(maxon)
maxon[is.na(maxon)] <- 0
maxon[is.infinite(maxon)] <- 0

heatmaply(maxon,xlab="Presynaptic Region",ylab="Postsynaptic Region")

## Graph
################################################################
dfmg <- data.frame(SReg_id=dfm$SReg_id,PReg_id=dfm$PReg_id,axon=log(dfm$axon))
dfmg$axon[is.infinite(dfmg$axon)] <- 0 
dfmg <- aggregate(dfmg, by=list(dfmg$SReg_id,dfmg$PReg_id), FUN = mean)

df.g <- graph.data.frame(d = dfmg, directed = T)

plot.igraph(df.g,vertex.size=2,edge.arrow.size=0.1,vertex.label=NA,layout=layout.lgl)

plot(df.g,layout=layout_with_lgl(df.g),margin = -.5)
plot(df.g,layout=layout_with_fr(df.g))
plot(df.g,layout.reingold.tilford(df.g, circular=T))
# bioFabric(df.g)

library(HiveR)

gD <- simplify(df.g) 
gAdj <- get.adjacency(gD, type = "upper", edges = FALSE, names = TRUE, sparse = FALSE)
hive1 <- adj2HPD(gAdj, type = "2D")

# plot(simplify(df.g), vertex.size= 0.01,
#      edge.arrow.size=0.001,
#      vertex.label.cex = 0.75,
#      vertex.label.color = "black"  ,
#      vertex.frame.color = adjustcolor("white", alpha.f = 0),
#      vertex.color = adjustcolor("white", alpha.f = 0),
#      edge.color=adjustcolor(1, alpha.f = 0.15),
#      display.isolates=FALSE,
#      vertex.label=ifelse(page_rank(df.g)$vector > 0.1 ,
#                          "important nodes", NA))
