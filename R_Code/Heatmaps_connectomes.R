library(heatmaply)
library(igraph)
library(nat)
library(splineTimeR)
library(ggpubr)

al <- read.csv('connection_axonlength.csv', skip = 1, row.names = 2)
al$X <- NULL
al <- as.matrix(al)
# heatmaply(log(al+1))

colnames(al) <- gsub("Ips", "ipsi", colnames(al))
colnames(al) <- gsub("Con", "contra", colnames(al))
rownames(al) <- paste0(rownames(al),"_ipsi")

hemi <- read.csv('normalized_connection_strength.csv', header=F)[1,-1]
cs <- read.csv('normalized_connection_strength.csv', skip = 1, row.names = 1)
names(cs) <- paste0(names(cs),"_", hemi)
names(cs) <- gsub(".1", "", names(cs))
cs <- as.matrix(cs)
cs <- cs[rownames(cs) %in% rownames(al) | rownames(cs) %in% substring(colnames(al),1,nchar(colnames(al))-5),]
# heatmaply(log(cs+1))

rownames(cs) <- paste0(rownames(cs),"_ipsi")

cs2 <- cs
for(i in rownames(cs)){
  print(i)
  if(i %in% rownames(al)){
    cs2[i,] <- al[i,]
  }
}
al <- cs2
# cs2[rownames(cs) %in% rownames(al),] <- al[rownames(cs),]

# duplicate ipsilateral projections to generate contralateral side
contraal <- al
rownames(contraal) <- gsub("ipsi","contra",rownames(contraal))
# select only projections from the contralateral side receiving inputs from the regions in the mesoscopic data
contraal <- contraal[rownames(contraal) %in% colnames(cs),]
colnames(contraal) <- gsub("ipsi","CONTRA",colnames(contraal))
colnames(contraal) <- gsub("contra","ipsi",colnames(contraal))
colnames(contraal) <- gsub("CONTRA","contra",colnames(contraal))
contraal[,grep("ipsi", colnames(contraal))] <- 0

contracs <- cs
rownames(contracs) <- gsub("ipsi","contra",rownames(contracs))
contracs <- contracs[rownames(contracs) %in% colnames(cs),]
colnames(contracs) <- gsub("ipsi","CONTRA",colnames(contracs))
colnames(contracs) <- gsub("contra","ipsi",colnames(contracs))
colnames(contracs) <- gsub("CONTRA","contra",colnames(contracs))
# contracs <- contracs[,grep("contra", colnames(contracs))]
contracs[,grep("ipsi", colnames(contracs))] <- 0

al <- rbind(al,contraal)
cs <- rbind(cs,contracs)

al <- log(al+1)
cs <- log(cs*100+1)

d <- dim(al)
cn <- colnames(al)
al <- al[, colSums(al != 0) > 0]
al_sq <- rbind(al, matrix(0, diff(d), ncol(al), dimnames = list(cn[(d[1]+1):d[2]])))

d <- dim(cs)
cn <- colnames(cs)
cs <- cs[, colSums(cs != 0) > 0]
cs_sq <- rbind(cs, matrix(0, diff(d), ncol(cs), dimnames = list(cn[(d[1]+1):d[2]])))

alg <- graph_from_adjacency_matrix(al_sq)
cdg <- graph_from_adjacency_matrix(cs_sq)

# plot(alg,layout=layout_with_fr)
# regnet<-watts.strogatz.game(dim=1, size=length(V(cdg)), nei=10, p=0, loops=FALSE, multiple=FALSE)
randg <- erdos.renyi.game(length(V(cdg)), gsize(cdg)/100, type = "gnm")
# randg <- watts.strogatz.game(1, length(V(cdg)), 1, 1, loops = FALSE, multiple = FALSE)
swg <- watts.strogatz.game(1, length(V(cdg)), 1, 0.35, loops = FALSE, multiple = FALSE)


d <- degree.distribution(alg)
dmeso <- degree.distribution(cdg)
drand <- degree.distribution(randg)
dsw <- degree.distribution(swg)
# 
plot(d,log = 'xy', xlab = 'Degree d', ylab = 'p(d)', main = 'Degree distribution in log-log scale ')

dfplot <- data.frame(Degree=1:length(d),Frequency=d)
dfmeso <- data.frame(Degree=1:length(dmeso),Frequency=dmeso)
dfrand <- data.frame(Degree=1:length(drand),Frequency=drand)
dfsw <- data.frame(Degree=1:length(dsw),Frequency=dsw)
ggplot(dfplot,aes(x=Degree,y=Frequency, color="Single Neuron Connectivity",shape="Single Neuron Connectivity")) + 
  geom_point() +
  geom_point(data=dfmeso,aes(x=Degree,y=Frequency,color="Mesoscopic Connectivity",shape="Mesoscopic Connectivity")) + 
  geom_line(data=dfrand,aes(x=Degree,y=Frequency,color="Random Network",shape="Random Network")) +  
  geom_line(data=dfsw,aes(x=Degree,y=Frequency,color="Small-World Network",shape="Small-World Network")) + 
  scale_x_log10() +
  scale_y_log10() +
  theme_pubr() +
  theme(legend.position="right") 


barplot(motifs(cdg)[2:16])
barplot(motifs(alg)[2:16])

# networkProperties(cdg)
# 
# 
# # List of degrees
# d.histogram <- igraph::degree.distribution(randg)
# 
# # Let's count the frequencies of each degree
# # d.histogram <- as.data.frame(table(d))
# 
# # Need to convert the first column to numbers, otherwise
# # the log-log thing will not work (that's fair...)
# d.histogram[,1] <- as.numeric(d.histogram[,1])
# 
# # Now, plot it!
# ggplot(d.histogram, aes(x = d, y = Freq)) +
#   geom_point() +
#   scale_x_continuous("Degree\n(nodes with this amount of connections)",
#                      breaks = c(1, 3, 10, 30, 100, 300),
#                      trans = "log10") +
#   scale_y_continuous("Frequency\n(how many of them)",
#                      breaks = c(1, 3, 10, 30, 100, 300, 1000),
#                      trans = "log10") +
#   ggtitle("Degree Distribution (log-log)")



####### Layout on brain

# ccf <- read.im3d("annotation_25.nrrd")
# ccf[ccf>1] <- 255
# ccf2d <- projection(ccf,projdim="y",projfun="mean")
# save(ccf2d,file='ccf2d.Rdata')
load('ccf2d.Rdata')

df <- read.csv("Location_on_half_side.csv",header=T)
vlabs <- data.frame(labs=vertex_attr(alg, "name"))
vlabs$Abbreviation <-  sapply(strsplit(vlabs$labs,'_'), "[", 1)
vlabs$Side <-  sapply(strsplit(vlabs$labs,'_'), "[", 2)
dfcoords <- merge(df,vlabs,by="Abbreviation",all.y=T,sort=F)
dfcoords[dfcoords$Side=="contra",]$x <- max(df$x,na.rm=T) - (dfcoords[dfcoords$Side=="contra",]$x - max(df$x,na.rm=T))
# dfcoords$z <- rev(dfcoords$z)
dfcoords[is.na(dfcoords$x),]$x <- length(ccf2d[1,])
dfcoords[is.na(dfcoords$z),]$z <- length(ccf2d[,1])

dfcoords <- dfcoords[match(vlabs$labs,dfcoords$labs),]

meta <- data.frame("name" = vlabs$labs, 
                   "lon" = dfcoords$x, 
                   "lat" = dfcoords$z)

# g <- graph.data.frame(df, directed = TRUE, vertices = meta)

lo <- layout.norm(as.matrix(meta[,2:3]))
# 
# plot.igraph(alg, 
#             layout = lo,
#             rescale = F, 
#             edge.curved = F, 
#             edge.arrow.size = 0.2,
#             vertex.size = 5,
#             label.size = 20,
#             label.cex = 0.1)
# 
# plot.igraph(alg,
#             layout = layout_with_fr,
#             rescale = F,
#             edge.curved = F,
#             edge.arrow.size = 0.2,
#             vertex.size = 5,
#             label.size = 20,
#             label.cex = 0.1)
# 
# plot.igraph(alg, 
#             layout = layout_with_lgl,
#             rescale = F, 
#             edge.curved = F, 
#             edge.arrow.size = 0.2,
#             vertex.size = 5,
#             label.size = 20,
#             label.cex = 0.1)

#Choose your favorite algorithm to find communities.  The algorithm below is great for large networks but only works with undirected graphs
c_g <- fastgreedy.community(simplify(as.undirected(cdg)),weights = E(cdg)$weight)
# c_g <- label.propagation.community(as.undirected(cdg))
# c_g <- edge.betweenness.community(cdg)
#Collapse the graph by communities.  This insight is due to this post http://stackoverflow.com/questions/35000554/collapsing-graph-by-clusters-in-igraph/35000823#35000823
res_g <- simplify(contract(cdg, membership(c_g)))
plot.igraph(res_g, 
            layout = layout_with_fr,
            rescale = T, 
            edge.curved = F, 
            edge.arrow.size = 0.2,
            vertex.size = 5,
            label.size = 20,
            label.cex = 0.1)


ceb <- cluster_edge_betweenness(alg) 

dendPlot(ceb, mode="hclust")
plot(ceb, alg) 