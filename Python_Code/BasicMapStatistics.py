## 验证矩阵填充的合理性，计算分布是否相同
import csv
import numpy as np
import BasicFunction as BF

## 读取Reco_Dataset_Cell得到映射矩阵 
with open("..\\Data\\Reco_Dataset_Cell.csv", "r") as f:
    reader = csv.reader(f)
    data=np.array(list(reader))
region_list=[]
projection_list=[]
for i in data:
    region_list.append(str(i[0]))
    projection_list.append(str(i[1])+'_'+str(i[2]))
region_list=list(set(region_list))
projection_list=list(set(projection_list))

projection_list=BF.getregionname(projection_list,'side1')
region_list=BF.getregionname(region_list,1)
# 数据转换
relation_map=np.load('.\Save_Data\connection_map.npy')
for i in range(0,np.shape(relation_map)[0]):
    for j in range(0,np.shape(relation_map)[1]):
        if relation_map[i,j]>=40:
            relation_map[i,j]=np.log(relation_map[i,j]/250+1)
        elif relation_map[i,j]==0:
            continue
        else:
            relation_map[i,j]=0


## 统计allen结果
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


## 取出相同的两列数据
map_l=[]
allen_l=[]
for i in range(0,len(region_list)):
    if region_list[i] in region_list_allen:
        for j in range(0,len(projection_list)):
            if projection_list[j] in projection_list_allen:
                if relation_map[i,j]>0:
                    map_l.append(relation_map[i,j].astype(np.float64))
                    t1=region_list_allen.index(region_list[i])
                    t2=projection_list_allen.index(projection_list[j])
                    allen_l.append(allen_matrix[t1,t2].astype(np.float64))

from scipy import stats
sstr = '%-14s mean = %6.4f, variance = %6.4f, skew = %6.4f, kurtosis = %6.4f'
n, (smin, smax), sm, sv, ss, sk = stats.describe(map_l)
print(sstr % ('map:', sm, sv, ss, sk))
n, (smin, smax), sm, sv, ss, sk = stats.describe(allen_l)
print(sstr % ('allen:', sm, sv, ss, sk))

import pandas as pd
df_map=pd.DataFrame(map_l)
print(df_map.describe().T)

df_allen=pd.DataFrame(allen_l)
print(df_allen.describe().T)

'''
stats.kstest(map_l,allen_l)
np.corrcoef(map_l,allen_l)
'''
'''
map_nor=(np.array(map_l)-np.min(map_l))/(np.max(map_l)-np.min(map_l))
allen_nor=(np.array(allen_l)-np.min(allen_l))/(np.max(allen_l)-np.min(allen_l))

import matplotlib.pyplot as plt
fig = plt.figure()
ax11 = fig.add_subplot(1, 2, 1)
n, bins, patches = ax11.hist(map_l,bins=1000)
ax12 = fig.add_subplot(1, 2, 2)
n, bins, patches = ax12.hist(allen_l,bins=1000)
plt.show()
stats.kstest(map_nor,allen_nor)
'''