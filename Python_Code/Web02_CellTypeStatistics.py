'''
Cell Type的数据统计
'''
### 根据94个区域统计 ###
import BasicFunction as BF
import numpy as np
import os
import csv

### 推荐深度数据 ###
# 使用axon 长度 （长度比例的问题在于，存在一些丰富长度的次要区域会被忽视，所以不适用）
with open("..\\Data\\Reco_Dataset_Cell.csv", "r") as f:
    reader = csv.reader(f)
    Data=np.array(list(reader))
    f.close()
'''
class Result:
    def __init__(self):
        self.name = ''
        self.axon_length = 0
        self.dendrite_length = 0
        self.soma_num = 0
        self.target = ''
        self.source = ''


### 某个cell type 内可以统计的量 ###
celltype='385'
result = Result()
result.name = BF.getregionname([celltype], 1)[0]
# soma数量 axon总长度 dendrite总长度
temp = Data[np.where(Data[:, 0] == celltype)[0], :]
result.axon_length = np.sum(temp[:, 3].astype(np.float64))
result.dendrite_length = np.sum(temp[:, 4].astype(np.float64))
result.soma_num = len(set(temp[:, 5]))

# axon dendrite 投射前五个区域（两个饼图）
projection_list = []
for x in Data:
    if x[1] + '_' + x[2][0:3] not in projection_list:
        projection_list.append(x[1] + '_' + x[2][0:3])
projetion_length = np.zeros([len(projection_list), 2])

for x in temp:
    t = projection_list.index(x[1] + '_' + x[2][0:3])
    projetion_length[t, 0] = projetion_length[t, 0] + x[3].astype(np.float64)
    projetion_length[t, 1] = projetion_length[t, 1] + x[4].astype(np.float64)

# 前十的名称和对应长度
projection_name = BF.getregionname(projection_list, 'side1')
temp = np.c_[projetion_length, np.array(projection_name)]
axon_rank = temp[np.argsort(-projetion_length[:, 0]), :]
dendrite_rank = temp[np.argsort(-projetion_length[:, 1]), :]

if axon_rank[0, 2] == result.name + '_Ips':
    result.target = axon_rank[1, 2]
else:
    result.target = axon_rank[0, 2]
result.source = dendrite_rank[0, 2]

sector_graph = []
for i in range(0, 5):
    sector_graph.append([np.floor(axon_rank[i,0].astype(np.float64)), str(axon_rank[i,2]), np.floor(dendrite_rank[i,0].astype(np.float64)), str(dendrite_rank[i,2])])
sector_graph.append([ np.floor(result.axon_length - np.sum(axon_rank[0:5,0].astype(np.float64))), 'Others', np.floor(result.axon_length - np.sum(dendrite_rank[0:5,0].astype(np.float64))), 'Others'])
axon_name = list(axon_rank[0:5, 2])
axon_name.append('Others')
dendrite_name = list(dendrite_rank[0:5, 2])
dendrite_name.append('Others')
'''
### 某个cell type 构建热力图（即为矩阵）

threshold=100/25 #有效连接阈值
path="..\\Other Information\\Soma_region_and_location.xls"
area_data = BF.read_xlsx(path,'Sheet1')
del area_data[0]
area_data=np.array(area_data)
### 94个区域的信息特征
## 删除Error_Data内的soma
for filename in os.listdir('..\\Error_Data\\'):
    temp=filename.split('_cul')
    temp=temp[0]
    t=np.where(area_data[:,0]==temp)
    area_data=np.delete(area_data,t,axis = 0)




### 遍历94个区域 区域内特征包括同侧和异侧 每个区域内聚类，得到motif ###
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(font_scale=0.6)
import pandas as pd
import scipy.cluster.hierarchy as sch
import math
from sklearn.cluster import KMeans
from sklearn import metrics
import rpy2.robjects as robjects
sns.set()
motif_projmap={} #映射图
motif_projfreq={} #映射图频率
motif_count=[] # 每个区域最终统计的motif的数量

a_t='VPM'# 当前区域名称
soma_list=[]
for x in area_data:
    if x[4]==a_t:
        soma_list.append(x[0].tolist())


 # 根据soma_list Data构建对应的投射序列
projection_list=[]
for x in soma_list:
    t = np.where(Data[:,5]==x)
    temp= Data[t,1:3].tolist()
    temp=temp[0]
    for k in temp:
        projection_list.append(k[0]+'_'+k[1][0:3])
projection_list=list(set(projection_list))

# 构建二维矩阵
heat_value=np.zeros((len(soma_list),len(projection_list))) 
for i in range(0,len(soma_list)):
    t = np.where(Data[:,5]==soma_list[i])
    temp= Data[t,1:3].tolist()
    t_value=Data[t,3].astype(np.float64)
    t_value=t_value[0]
    temp=temp[0]
    for k in range(0,len(temp)):
        heat_value[i,projection_list.index(temp[k][0]+'_'+temp[k][1][0:3])]=t_value[k]


# 阈值筛选
for i in range(0,np.size(heat_value,0)):
    for j in range(0,np.size(heat_value,1)):
        if heat_value[i,j]!=0 and heat_value[i,j]<threshold:
            heat_value[i,j]=0
soma_label=[]
proj_label=[]

if len(soma_list)<20: #丢掉数量少的区域
    print('too less soma')
    heat_map=heat_value
    t2=[]
    for i in range(0,np.size(heat_map,1)):
        if np.sum(heat_map[:,i]) > np.shape(heat_map,0):
                t2.append(i)
                proj_label.append(projection_list[i])
    heat_map=heat_map[:,tuple(t2)]
    # 取log
    for i in range(0,np.size(heat_map,0)):
        for j in range(0,np.size(heat_map,1)):
                heat_map[i,j]=np.log(heat_map[i,j]*100+1)
    proj_label=BF.getregionname(proj_label,'side1')
    soma_label=soma_list
else:
    # 剔除数值小的行列 3std
    mean_t=np.mean(np.sum(heat_value, axis=1))
    std_t=np.std(np.sum(heat_value, axis=1))
    t1=[]
    for i in range(0,np.size(heat_value,0)):
        if np.sum(heat_value[i,:]) > (mean_t + 1*std_t):
                t1.append(i)
                soma_label.append(soma_list[i])
    
    heat_map=heat_value[tuple(t1),:]
    t2=[]
    for i in range(0,np.size(heat_map,1)):
        if np.sum(heat_map[:,i]) > len(t1):
                t2.append(i)
                proj_label.append(projection_list[i])
    heat_map=heat_map[:,tuple(t2)]
    
    # ## 归一化 x/total length
    # for i in range(0,len(heat_map)):
    #     heat_map[i,:]=heat_map[i,:]/np.sum(heat_map[i,:])
    
    # 取log
    for i in range(0,np.size(heat_map,0)):
        for j in range(0,np.size(heat_map,1)):
                heat_map[i,j]=np.log(heat_map[i,j]*100+1)
    proj_label=BF.getregionname(proj_label,'side1')
    
    import scipy
    import scipy.cluster.hierarchy as sch
    from scipy.cluster.vq import vq,kmeans,whiten
    import numpy as np
    import matplotlib.pylab as plt
    data1=heat_map
    data2=heat_map.T
    #1. 层次聚类
    #生成点与点之间的距离矩阵,这里用的欧氏距离:
    disMat = sch.distance.pdist(data1,'euclidean') 
    #进行层次聚类:
    Z=sch.linkage(disMat,method='average') 
    #根据linkage matrix Z得到聚类结果:
    cluster = sch.fcluster(Z, t=1, criterion='inconsistent')
    #2. k-means聚类
    #将原始数据做归一化处理
    data=whiten(data1)
    centroid=kmeans(data,max(cluster))[0]  
    label_row=vq(data,centroid)[0] 
    
    disMat = sch.distance.pdist(data2,'euclidean') 
    Z=sch.linkage(disMat,method='average') 
    cluster = sch.fcluster(Z, t=1, criterion='inconsistent')
    data=whiten(data2)
    centroid=kmeans(data,max(cluster))[0]  
    label_col=vq(data,centroid)[0] 
    
    # 排序
    t1=np.argsort(label_col[:])
    t2=np.argsort(label_row[:])
    heat_map=heat_map[:,t1]
    heat_map=heat_map[t2,:]
    
    temp=[]
    for x in t1:
        temp.append(proj_label[x])
    proj_label=temp
    
    temp=[]
    for x in t2:
        temp.append(soma_label[x])
    soma_label=temp
    label_col=label_col[t1]
    label_row=label_row[t2]
    # sns.heatmap(heat_map,xticklabels=proj_label,yticklabels=soma_label)
    np.max(heat_map)