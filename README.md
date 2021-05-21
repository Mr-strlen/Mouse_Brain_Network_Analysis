# Mouse Brain Network Analysis
希望使用小鼠单细胞形态重构数据，进行脑网络分析，发现一些有趣的结果  
P.S. 这是本人的本科毕设也是研究生的第一个课题
  
## Directory Structure
### C++ Code
Some test code like read .swc files

### Data
Statistics will be used

### FlaskWeb
A visualization system based on Flask

### NetWork Plugin, QPH
A test vaa3d plugin and the plugin to be developed 

### Note
Notes about basic knowledge of neuroscience and project progress

### Other Information
Other information used in this research  

### Python Code, R_Code
the code used for analysis


## Goals
### **20201124**
1. Generate a statistical intermediate file, including the area id and length (note: data deviation caused by decimals)
2. Statistics function (tree data structure of area relationships) (possible interactive interface)
3. Connectivity judgment based on Peters' rule

### **20201130**
1. To introduce label ids, and lower hierarchy (depth) region labels, based on the structure ath
2. Replot heatmap and graph visualization using those
3. Create degree distribution plot
4. Obtain routing efficiency (check definition https://serval.unil.ch/resource/serval:BIB_33A6423F21C5.P001/REF)

### **20201128**
How to combine graph analysis and simulation  
1. propagation speed of signals through the network <-> routing efficiency of the graph
2. oscillations at different frequency bands <-> small-world topology, or we can try to find how specific motifs can be relevant for that
3. Neural complexity (Koenigsberger) <-> specific network topologies may maximize neural complexity
4. Focusing on thalamocortical-cortex dynamics <-> check how does this depend on the structure of the network and check how pathological cases deviate

### **20210126**
* 主要做的事情：  
	1. 在不同的cell types上，统计了每个神经元到不同区域axon投射的长度（这里设置了一个阈值，500um）这样就可以得到一个神经元个数*投射区域个数的二维矩阵
	2. 利用Bayesian Information Criterion (BIC)，SSE(sum of the squared errors，误差平方和)等方法确定聚类个数
	3. 使用K-means聚类，并画出每个类别的热力图，并识别出motif
  
一开始还做了层次聚类的尝试，但是linus觉得这个太复杂了  
层次聚类参考  
https://blog.csdn.net/qq_40527086/article/details/83218513
  
* 个人觉得过程中存在的问题  
  1. 确定分类个数的具体方法
    * BIC没有python的处理包
    * 使用R语言，介绍了很多种方法 https://stackoverflow.com/questions/15376075/cluster-analysis-in-r-determine-the-optimal-number-of-clusters
    * 手肘法、轮廓系数法 https://zhuanlan.zhihu.com/p/51777857
  2. 在得到分类个数的曲线后，如何定量的确定分类个数，目前是使用阈值 80%
  3. 分类使用什么策略 （目前使用kmeans，Kmeans受起始点影响很大，是不稳定的）
  4. 然后对于每个分类的结果，如何去确定连接，目前使用对列求和，然后找出大于3std的列
  5. 目前只在每个cell type上做了分析，linus还希望跨cell types也做分析（这部分目前没做，准备等把前面的方法敲定再执行）
  
* 为什么要做motif分析和后续计划  
根据motif分析结果，将每个motif作为后续网络分析的节点，再做网络分析

#### 对上述问题的解释和补充
1. 同侧和异侧区别 Ipsilateral and contralateral projections 谢老师的paper  
需要在 Reco_dataset_cell 加一列左右的评判结果，之后分析的时候，同侧和异侧作为两个feature单独计算
2. 聚类方法的考虑  
对于不同聚类方法的考虑
https://blog.csdn.net/glodon_mr_chen/article/details/79867268  
有关pvcluste的讨论
3. 确定具体分类数量：每个脑区去看一眼（还包括swc形态学上的差异），使用自动化方法kpam
4. 聚类方式，可以做一些比较：  
  a. 分类数量对结果的影响  
  b. kmeans不稳定的比较  
  c. 不同方法间的佐证  
5. 确定heatmap的结果，除了使用3std的筛选，还可以加上frequenece，作为一种补充（投射到某个区域的概率有多大）大于heatmap整体均值
6. 标准化x/total length或者使用cos，不用欧氏距离

### **20210520**
完成毕业论文和查重工作

## Other Ideas
1. a external interface for python
