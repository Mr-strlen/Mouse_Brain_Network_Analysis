'''
这里使用最基本的关系图构建方式
1. 根据深度调整后Reco_Dataset_Cell，统计出所有连接关系
2. 填充同侧异侧关系
3. 将连接矩阵中所有的零使用mesoscale connectome替换 
4. 得到关系矩阵

矩阵包括：
1. 进行反转前的：
 * 单细胞形态矩阵 connection_map_single.npy
 * 中尺度矩阵 connection_map_middle.npy
 * 组合矩阵 connection_map_combine.npy
2. 反转填充后的：
 * 单细胞形态矩阵 connection_matrix_single.npy
 * 中尺度矩阵 connection_matrix_middle.npy
 * 组合矩阵 connection_matrix_combine.npy
'''

import csv
import numpy as np
import BasicFunction as BF
import matplotlib.pyplot as plt


### 反转前的三个矩阵
## 读取Reco_Dataset_Cell得到映射矩阵 
with open("..\\Data\\Reco_Dataset_Cell.csv", "r") as f:
    reader = csv.reader(f)
    data=np.array(list(reader))
region_list=[]
projection_list=[]
for i in data:
    region_list.append(str(i[0]))
    projection_list.append(str(i[1])+'_'+str(i[2]))
region_list_origin=list(set(region_list)) #原始的soma区域名称
projection_list_origin=list(set(projection_list)) #原始的projection区域名称

# 按照字母序固定行列顺序

projection_list=BF.getregionname(projection_list_origin,'side1')
region_list=BF.getregionname(region_list_origin,1)

region_list_origin=np.array(region_list_origin)[np.argsort(region_list)]
projection_list_origin=np.array(projection_list_origin)[np.argsort(projection_list)]

region_list.sort()
projection_list.sort()

'''
## 填充单细胞形态矩阵 这里很慢
relation_map=np.zeros([len(region_list),len(projection_list)])
relation_count=np.zeros([len(region_list),len(projection_list)]) # 统计每个投射有多少个神经元
for i in range(0,len(region_list)):
    print(i)
    for j in range(0,len(projection_list)):
        t=projection_list_origin[j].split('_')
        r=np.where((data[:,0]==str(region_list_origin[i])) & (data[:,1]==t[0]) & (data[:,2]==t[1]))[0]
        if len(r)>0:
            for k in r:
                relation_map[i,j]=relation_map[i,j]+data[k,3].astype(float)
                relation_count[i,j]=relation_count[i,j]+1
# 求投射的平均
for i in range(0,len(region_list)):
    for j in range(0,len(projection_list)):
        if relation_count[i,j]>0:
            relation_map[i,j]=relation_map[i,j]/relation_count[i,j]
            # 取log(e)(mm+1)
            if relation_map[i,j]>=40: #大于1mm的
                relation_map[i,j]=np.log(relation_map[i,j]/40+1)
            else:
                relation_map[i,j]=0
np.save('.\Save_Data\connection_map_single.npy',relation_map.astype(np.float64))


## 中尺度数据矩阵 paper数据的 brain atlas额外计算
relation_map=np.zeros([len(region_list),len(projection_list)])
with open('./Allen_Data/normalized_connection_strength.csv') as f:
    reader=csv.reader(f)
    data=np.array(list(reader))
    allen_matrix=data[1:,1:].astype(np.float64)
# 构建矩阵
projection_list_allen=[]
for x in list(data[0,1:]):
    projection_list_allen.append(str(x))
region_list_allen=[]
for x in list(data[1:,0]):
    region_list_allen.append(str(x))

# 填充矩阵
for i in range(0,len(region_list)):
    t=region_list[i]
    if t not in region_list_allen:
        print(region_list[i]+' not in lines')
        continue
    line=region_list_allen.index(t)
    for j in range(0, len(projection_list)):
        tt=projection_list[j]
        if tt in projection_list_allen:
            row=projection_list_allen.index(tt)
            relation_map[i,j]=allen_matrix[line,row].astype(np.float64)
        else:
            print(projection_list[j] +' not in rows')
            
np.save('.\Save_Data\connection_map_middle.npy',relation_map.astype(np.float64))
'''

## 组合矩阵
relation_map=np.load('./Save_Data/connection_map_single.npy')
middle_map=np.load('./Save_Data/connection_map_middle_allenbrainaltas.npy')
# 组合矩阵
for i in range(0,len(region_list)):
    for j in range(0, len(projection_list)):
        if relation_map[i,j]==0 and middle_map[i,j]!=0:
            relation_map[i,j]=middle_map[i,j]
np.save('.\Save_Data\connection_map_combine.npy',relation_map.astype(np.float64))



### 构建反转矩阵
projection_list1=BF.getregionname(projection_list_origin,'side1')
region_list1=BF.getregionname(region_list_origin,1)

## 构建反转矩阵
region_list2=[]
projection_list2=[]
for i in range(0,len(region_list1)):
    region_list2.append(region_list1[i]+'_Con')
    region_list1[i]=region_list1[i]+'_Ips'
for x in projection_list1:
    if 'Con' in x:
        projection_list2.append(x.replace('Con','Ips'))
    else:
        projection_list2.append(x.replace('Ips','Con'))

region_list=region_list1+region_list2 #soma区域列表
projection_list=list(set(projection_list1+projection_list2)) # 投射区域列表

region_list.sort()
projection_list.sort()

'''
## 单细胞形态矩阵的反转 
relation_map=np.load('./Save_Data/connection_map_single.npy')
relation_matrix=np.zeros([len(region_list),len(projection_list)])
for i in range(0,len(region_list)):
    print(i)
    line=region_list[i].split('_')
    for j in range(0,len(projection_list)):
        if line[1]=='Ips':
            if projection_list[j] in projection_list1:
                relation_matrix[i,j]=relation_map[region_list1.index(region_list[i]),projection_list1.index(projection_list[j])]
        elif line[1]=='Con':
            if projection_list[j] in projection_list2:
                relation_matrix[i,j]=relation_map[region_list2.index(region_list[i]),projection_list2.index(projection_list[j])]
        else:
            print('no matching error')
np.save('.\Save_Data\connection_matrix_single.npy',relation_matrix.astype(np.float64))


## 中尺度数据的反转 
relation_map=np.load('./Save_Data/connection_map_middle_allenbrainaltas.npy')
relation_matrix=np.zeros([len(region_list),len(projection_list)])
for i in range(0,len(region_list)):
    print(i)
    line=region_list[i].split('_')
    for j in range(0,len(projection_list)):
        if line[1]=='Ips':
            if projection_list[j] in projection_list1:
                relation_matrix[i,j]=relation_map[region_list1.index(region_list[i]),projection_list1.index(projection_list[j])]
        elif line[1]=='Con':
            if projection_list[j] in projection_list2:
                relation_matrix[i,j]=relation_map[region_list2.index(region_list[i]),projection_list2.index(projection_list[j])]
        else:
            print('no matching error')
np.save('.\Save_Data\connection_matrix_middle.npy',relation_matrix.astype(np.float64))

'''
## 组合数据的反转 
relation_map=np.load('./Save_Data/connection_map_combine.npy')
relation_matrix=np.zeros([len(region_list),len(projection_list)])
for i in range(0,len(region_list)):
    print(i)
    line=region_list[i].split('_')
    for j in range(0,len(projection_list)):
        if line[1]=='Ips':
            if projection_list[j] in projection_list1:
                relation_matrix[i,j]=relation_map[region_list1.index(region_list[i]),projection_list1.index(projection_list[j])]
        elif line[1]=='Con':
            if projection_list[j] in projection_list2:
                relation_matrix[i,j]=relation_map[region_list2.index(region_list[i]),projection_list2.index(projection_list[j])]
        else:
            print('no matching error')
np.save('.\Save_Data\connection_matrix_combine.npy',relation_matrix.astype(np.float64))
