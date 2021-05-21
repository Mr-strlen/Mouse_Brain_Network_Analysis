### Vaa3D算法
#### 路径算法变化
2010 graph-augmented deformable model GD  最短路要求覆盖最多，骨架识别
2011 all-path pruning APP 相比GD，取消了复杂的代价函数计算，和非参的优化，使用寻找节点+删除的策略
2013 APP2 三个改进点 GWDT，初始重建，分层修剪

#### 结构贴近算法：
2010 V3D-Neuron 1.0  包括贴近算法+重构算法
2014 3D virtual finger VF A 3D point-pinpointing algorithm (PPA)  CDA1 CDA2 Vaa3D-Neuron2

#### 大图像拼接算法
2014 Vaa3D-TeraFly

#### 之后没有看论文的部分
* Bigneuron
* Blastneuron
* SmartScope2
* TeraVR

#### 问题：
1. 相邻节点划分定义的单位1是什么：像素点
2. 这是不是有点多啊OTZ：不多，是稀疏的
3. 刚才想到的一个问题，按理来说，广度优先，或者这种最大连通图是一个很顺畅的思路，咋会上来先用的是Dijkstra呢，有什么目的么：从神经元胞体间结构分析转换到加入树突的细节分析
4. Dijkstra对形态的忽略？ 三角形/环形（这点在APP2里面换成了prime算法，但是还是不能解决三角形问题）：这就是目前算法的问题


### 神经科学
#### 计算神经科学
Integrate-And-Fire Models  
https://blog.csdn.net/qq_34886403/article/details/75735448

#### 网络神经科学
https://www.sohu.com/a/345884649_741733  
《On the nature and use of models in network neuroscience》  
https://www.nature.com/articles/s41583-018-0038-8  

#### 神经科学定律 https://zhuanlan.zhihu.com/p/19939960
* 赫布理论（Hebb's rule） 学习和记忆、突触可塑性(synaptic plasticity)   
* 韦伯定理（或 感觉阈限定律，Weber's Law) 感知（perception）、五觉（听、看、嗅、尝、触）
* PVA Population Vector Algorithm https://blog.csdn.net/Frankgoogle/article/details/105524794

### CCFv3
#### 艾伦小鼠脑三维图谱  
https://scalablebrainatlas.incf.org/mouse/ABA_v3  
https://atlas.brain-map.org/  
  
1. 模型导入过多了直接爆炸
2. 谢老师给的是映射之后的实际物理参数，可以用来计算实际距离；标准脑是缩小了25倍的数据，所以可以进行观察  
思路：轴突作为输出，树突作为输入（假设的合理性），计算根部的覆盖率，得到一个1708*1708的矩阵，再去观察两两之间的问题
3. 轴突和树突的编号差异
* 1： 胞体
* 2： 轴突
* 3： 树突
* 4： 顶树突
