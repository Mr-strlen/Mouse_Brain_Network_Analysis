###### Read nrrd and plot 2d projection
# ccf <- read.nrrd("annotation_25.nrrd")
ccf <- read.im3d("..\\Other Information\\annotation_25.nrrd")
ccf[ccf>1] <- 255
ccf2d <- projection(ccf,projdim="y",projfun="mean")
rotate <- function(x) t(apply(x, 2, rev))

png("Brain.png",width = 12, height = 12, units = 'in', res = 300)
par(bg="transparent")
image(rotate(rotate(rotate(ccf2d))),col=gray.colors(max(ccf2d),start = 1, end = 0.65),axes=F)
dev.off()

library(igraph)
graph <- read.graph("..\\Python_Code\\igraph_map",format="gml")

require(igraph)
require(Cairo)

df <- read.csv("Localtion on half side.csv",header=T)
vlabs <- data.frame(labs=vertex_attr(graph, "label"))
vlabs$Abbreviation <-  sapply(strsplit(vlabs$labs,'_'), "[", 1)
vlabs$Side <-  sapply(strsplit(vlabs$labs,'_'), "[", 2)
dfcoords <- merge(df,vlabs,by="Abbreviation",all.y=T,sort=F)
dfcoords[dfcoords$Side=="Con",]$x <- max(df$x,na.rm=T) - (dfcoords[dfcoords$Side=="Con",]$x - max(df$x,na.rm=T))
# dfcoords$z <- rev(dfcoords$z)
dfcoords[is.na(dfcoords$x),]$x <- length(ccf2d[1,])
dfcoords[is.na(dfcoords$z),]$z <- length(ccf2d[,1])

dfcoords <- dfcoords[match(vlabs$labs,dfcoords$labs),]

meta <- data.frame("name" = vlabs$labs, 
                   "lon" = dfcoords$x, 
                   "lat" = dfcoords$z)

# g <- graph.data.frame(df, directed = TRUE, vertices = meta)

lo <- layout.norm(as.matrix(meta[,2:3]))

png("Network.png",width = 12, height = 12, units = 'in', res = 300)
par(bg="transparent")
plot.igraph(graph, 
            layout = lo,
            rescale = F, 
            edge.curved = F, 
            edge.arrow.size = 1.5,
            vertex.size = 5,
            label.size = 20,
            label.cex = 0.1)

dev.off()

## Read in image background
library('png')
net.img = readPNG("Network.png")
img.3 =readPNG("Brain.png")

## Create empty plot
plot(0, type = 'n', axes = FALSE, ann = FALSE, 
     xlim=c(0,1), ylim=c(0,1))

## Now add two images,  first the background, then the network overlay
rasterImage(img.3, xleft=-0.1, xright=1.1, ybottom=-0.1, ytop=1.1)
rasterImage(net.img,  xleft=-0.1, xright=1.1, ybottom=-0.1, ytop=1.1)

#Overlay in maps
# library(maps)
# library(geosphere)

# map("state", col="grey20", fill=TRUE, bg="black", lwd=0.1)

# Add a point on the map for each airport:
# points(x=airports$longitude, y=airports$latitude, pch=19,
       # cex=airports$Visits/80, col="orange")
# col.1 <- adjustcolor("orange red", alpha=0.4)
# col.2 <- adjustcolor("orange", alpha=0.4)
# edge.pal <- colorRampPalette(c(col.1, col.2), alpha = TRUE)
# edge.col <- edge.pal(100)

# for(i in 1:nrow(flights)) {
#   node1 <- airports[airports$ID == flights[i,]$Source,]
#   node2 <- airports[airports$ID == flights[i,]$Target,]
#   arc <- gcIntermediate( c(node1[1,]$longitude, node1[1,]$latitude),
#                          c(node2[1,]$longitude, node2[1,]$latitude),
#                          n=1000, addStartEnd=TRUE )
#   edge.ind <- round(100*flights[i,]$Freq / max(flights$Freq))
#   lines(arc, col=edge.col[edge.ind], lwd=edge.ind/30)
# }


library(RcppCNPy)
# 
ccfmap <- npyLoad("ShadowMap.npy")
image(ccfmap)
# 
# # install devtools if required
if (!requireNamespace("devtools")) install.packages("devtools")
# # then install nat
devtools::install_github("natverse/nat")
# 
library(nat)
# 
# 
library(natverse)
library(dendroextras)
# 
# # install
if (!require("devtools")) install.packages("devtools")
devtools::install_github("natverse/mouselightr")
# # use 
library(mouselightr)
# 
# # set working directory to location of this file
# try(setwd(dirname(attr(body(function() {}),'srcfile')$filename)))
# 
# ## First we can quickly just plot the outer mesh for the brain
# outline = mouselight_read_brain(type = "outline")
# plot3d(outline, col = "pink", alpha = 0.3)
# 
# ## This is cool, but maybe what we really want are its sub-divisions.
# # mousebrain = mouselight_read_brain(type = "brain_areas")
# clear3d()
# plot3d(mousebrain)
# save(mousebrain,file="mouselight_brain.rda")
# 
# 
# ## We can download all of these neurons, and their meta-data
# ### Typically two tracings, and axon and a dendrite, per neuron
# mlns = mouselight_read_neurons(ndf$tracing.id, meta = TRUE)
# 
# ## Let's read in all the amygdalal neurons
# ### Since each
# in.amyg = mouselight_nodes_in_region(mlns, brain.areas = amygdala.codes, labels = NULL)
# amyg.ids = names(in.amyg)[in.amyg>0]
# amyg.neurons = mlns[amyg.ids]
# 
# ## And plot!
# plot3d(amyg.neurons)
