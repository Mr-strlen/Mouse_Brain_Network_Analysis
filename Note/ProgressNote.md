## 进度总结
### 创建区域关系结构文件 RegionStructureCreat
根据mouse.csv生成结构信息文件

### swc文件计算 FileCalculation
#### 思路：
1. 建立每个swc的tree结构（文件本身已经包括）
2. 每条边进行判定，区域以子节点为准：  
* 抛弃思路:
  * 整个边都在某个area内（多两个值）
  * 一部分在，一部分不在   
* 简化模型:  
a. 全部以叶子节点所在区域为准 √ （线段非常的短，计算效率优先）  
b. 认为父节点和子节点不属于同一个区就会有两个结果，这样没考虑区域边界弯曲的问题   
c. 连线逐个像素点判定，这样复杂度太大   
3. 匹配到nrrd空间，获取所在区域id
4. 计算线段长度

### 生成统计文件 长度关系，名称对应表 CombineFiles

### heatmap构建，画图及分析 HeatmapCreat PlotHeatmap
#### 思路
对于给定depth，统计在该depth下的叶子节点和存在子层次的节点（舍弃更低层次存在子层次的节点）  
#### 问题
1. 生成heatmap之后由于缺乏生理学知识，不知道要怎么处理  
（聚类算法采用默认，需要明确其意义）  
例如：对cortex - thalamus进行分析  

2. heatmap计算的count之前有问题，同一个神经元的同一个投影被计算多次  
现在加上神经元Id名称，相当于每个神经元到特定depth下的某个特定区域的投射只会被算为一次了  
然后出现了有个稍微违背尝试的结论，整体上统计的时候，随着depth越大，整体数值越小  
但是如果算平均的话，会发现在变大，这说明，少量的神经元，提供了大量的链接  

3. heatmap计算均值没有剔除count中的0值，已经分别计算了

### 基本信息统计 DataStatistics
包括soma的分布，axon，dendrite的长度分布，差异较大，不知道如何分析  
（针对CTX-TH结构分析）  
这部分不需要花太多精力，在之前数据集介绍的文献中已经说明清楚了  

### 画图 Plot_Cell Plot_Statistics Plot_Structure
* 一个神经元的不同区域使用不同颜色标记，并画出heatmap作为印证  
**(色彩采样网站 diverging and qualitative scales http://colorbrewer2.org)**
* 多个神经元绘制
* 全脑散点图
* soma axon dendrite指定depth指定区域的数量分布
* 层级结构树状图

### 图论分析 PlotGraph
已经构建了基本的图模型，但是不知道是否正确以及要算什么内容和其背后生理意义  
（针对CTX-TH结构分析）
* 计算degree distribution，比较和random graph的差异  
有关边权重的设计，这里使用axon投射长度（其他有群体标记，投射+接收），如何进行筛选



## 问题及注意点：
* 25倍缩放的问题： 统一就好  
* 为什么要做区域的统计，仅是对数据本身介绍，还是存在别的科学意义（样本分布不知道，数据集的偏差问题如何解决）：数据分布统计，之后分析会做数据的筛选
* 定位坐标使用floor  
* 初始id文件为nrrd文件，为uint32类型，如果转换为float，例如变成tif文件，会出现符号错误导致的异常大数值  
* 某些.swc文件中出现了x坐标大于边界值528的情况，这是运动部分的神经元后端连接到脊椎，所以出现的一些超过范围的情况  
* 成像过程中，胶体细胞因为没有做标记所以不会在显微镜中被看到  

### 数据层次过多如何描述
对soma distribution上根据depth做分层做统计  
对不同层级的axon,dendrite的长度做排序，从大到小，将排名靠前的层级标记出来  
对不同层级的heatmap，结合soma distribution，设定阈值做数量筛选  
关注CTX-TH连接，例如，Mop layer5，Ssp layer5  
关系网络画图软件Cytoscape  
图论分析可以针对某一类神经元，例如vpm  
soma region可利用soma数量进行筛选

## 图论分析
CTX-TH 皮层LGd到VISp集中，在LP中则体现不出来，算是一个常识  
随机网络方法 Erdos-Renyi: Graph.Erdos_Renyi() https://rpubs.com/lgadar/generate-graphs  
* motif子图 https://www.slideserve.com/hedy/biological-networks-analysis-degree-distribution-and-network-motifs  

## 仿真模拟 diple
https://github.com/AllenInstitute/dipde/blob/dev/dipde/examples/cortical_column.py  
https://alleninstitute.github.io/dipde/dipde.column.html

## 扩充数据集 http://ml-neuronbrowser.janelia.org/
***
## Vaa3D C++
### 编译过程
1. Boost 需要加到path中，所以可以放在common_lib\include里
2. 写成相对路径
3. \Vaa3D\v3d_external\v3d_main\basic_c_fun\IPMain4NeuronAssembler.h有问题
（4. 需要进行跨平台检验）
### 相关函数
* tif读取 simple_loadimage_wrapper is defined in v3d_interface.h
* 不同区域颜色 neuron_utilities/color_render_ESWC_features
### 辅助函数
* matplotlib-cpp https://github.com/lava/matplotlib-cpp


***
## Python/R语言：
* 聚类热力图 clustermap https://blog.csdn.net/qq_21478261/article/details/107729786  
* 树状图 Pyecharts https://www.cnblogs.com/adam012019/p/11400567.html  
* python和R的转化 https://www.hackerearth.com/blog/developers/how-can-r-users-start-learning-python-for-data-science/
### igraph 图论分析工具
* **官方文档 https://igraph.org/python/doc/tutorial/**
* C文档 (Random graph) https://igraph.org/c/doc/igraph-Generators.html
* R语言样例 (Random graph) https://kateto.net/netscix2016.html  
(degree distribution) https://assemblingnetwork.wordpress.com/2013/06/10/network-basics-with-r-and-igraph-part-ii-of-iii/
#### 样例
* 用Igraph创建关系网络&简单网络分析 https://www.jianshu.com/p/8a7d571653f1
* python-igraph基本用法（一）https://blog.csdn.net/u010758410/article/details/78027037
* 复杂网络分析工具Python+igraph https://www.zhihu.com/people/wang-ya-fei-30-13/posts
* 社区网络分析学习笔记 —— 算法实现及 igraph 介绍 https://zhuanlan.zhihu.com/p/40227203
* python与图论的桥梁——igraph https://zhuanlan.zhihu.com/p/97135627
