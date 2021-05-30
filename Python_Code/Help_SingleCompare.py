'''
单个神经元和中尺度的比较heatmap
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


import matplotlib.pyplot as plt
import seaborn as sns

# 筛选数据比较
compare_list=list(projection_list_origin)
allen_map=np.load('./Save_Data/connection_map_middle.npy')
for i in range(0,len(region_list_origin)): #对于某一个cell type
    heatmap=np.zeros([1,len(projection_list)])
    heatmap[0,:]=allen_map[i,:]
    data_t=data[np.where(data[:,0]==str(region_list_origin[i])),:][0]
    id_set=list(set(data_t[:,5]))
    for j in id_set:
        data_tt=data_t[np.where(data_t[:,5]==str(j)),:][0]
        temp=np.zeros([1,len(projection_list)])
        for x in data_tt:
            if float(x[3])<40:
                continue
            else:
                t=compare_list.index(x[1]+'_'+x[2])
                temp[0,t]=np.log(float(x[3])/40+1)
        if np.sum(temp)>0:
            heatmap=np.r_[heatmap,temp]
    for j in range(len(projection_list)-1,-1,-1):
        if np.sum(heatmap[:,j])>0:
            continue
        else:
            heatmap = np.delete(heatmap, j, axis=1)
    
    name=region_list[i]
    plt.close()
    plt.figure(figsize=(18, 8))
    
    sns_plot = sns.heatmap(heatmap,yticklabels=['middle']+id_set)
    plt.title(name)
    plt.show()
    plt.savefig('./heatmap/'+name+'.jpg')

   