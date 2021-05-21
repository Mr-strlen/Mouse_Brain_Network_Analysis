#  脑网络分析可视化系统

欲济无舟楫，端居耻圣明？   
舟楫人才系统，为您的职业发展，保驾护航。

## 技术架构

- 基于Flask框架
- 前端：HTML+CSS+JS 
- 数据库：SQLAlchemy+MySQL(orm封装)
- 版本控制：Git
- 可视化图表：Echarts, Layui, x-admin模板

## 效果演示
[完整功能演示录屏](./image/vedio record.mp4)
- 所有神经元基本信息
<img src="./images/01.png" alt="img"/>  
- 单个神经元形态
<img src="./images/02.png" alt="img"/>  
- 单个神经元统计信息
<img src="./images/03.png" alt="img"/>  
- 单个神经元投射路径
<img src="./images/04.png" alt="img"/>  
- 所有神经元统计结果
<img src="./images/05.png" alt="img"/>  
- 所有细胞类型基本信息
<img src="./images/06.png" alt="img"/>  
- 单个细胞类型内神经元轴突分布热力图
<img src="./images/07.png" alt="img"/>  
- 单个细胞类型的统计结果
<img src="./images/08.png" alt="img"/>  
- 脑网络可视化
<img src="./images/09.png" alt="img"/>  
- 网络分析结果
<img src="./images/10.png" alt="img"/>  

## 数据
使用单细胞形态重构数据，一部分来自Janelia Campus在19年发布的1000个神经元数据[1]，另一部分来自Allen Center发布的1708个神经元数据[2]。  
[1] Winnubst J, Bas E, Ferreira T A, et al. Reconstruction of 1,000 projection neurons reveals new cell types and organization of long-range connectivity in the mouse brain[J]. Cell, 2019, 179(1):268-281. 
[2] Wang Y, Xie P, Gong H, et al. Complete single neuron reconstruction reveals morphological diversity in molecularly defined claustral and cortical neuron types[J]. BioRxiv, 2019:675280.

## 其他
感谢Linus，谢芃老师在系统开发中作为模拟甲方提供的需求意见；感谢熊峰学长对神经元数据库和神经元投射路径相关知识的介绍；感谢王博学长和赵作翰同学在前端开发上的指导。