#绘画热力图
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(font_scale=3.5)
#sns.set()
import csv
import math
#导入id name对照表
structure_map=[]
with open("..\\Data\\Dataset_Structure.csv") as f:
    reader = csv.reader(f)
    name_map=list(reader)
    id_list=[];
    for x in name_map:
        id_list.append(x[0])
        t=[]
        temp=x[1].split('/')
        del temp[0]
        del temp[-1]
        for k in temp:
            t.append(k)
        structure_map.append(t)

# 读入文件
#path="..\\Heatmap_Data\\Heatmap_depth_7.csv"
path="..\\Heatmap_Data_cor_tha\\Heatmap_depth_7_cor_tha.csv"
with open(path) as file_object:
    reader = csv.reader(file_object)
    pair_map=list(reader)
    x_label=[]
    y_label=[]
    file_object.close()
    for x in pair_map:
        x_label.append(x[0])
        y_label.append(x[1])
  
    x_label=list(set(x_label))
    y_label=list(set(y_label))
    heat_value=np.zeros((len(x_label),len(y_label)))         
    for x in pair_map:
         heat_value[x_label.index(x[0])][y_label.index(x[1])]=math.log(float(x[4])+0.0001)#Axons
#        heat_value[x_label.index(x[0])][y_label.index(x[1])]=float(x[4])#Axons

# y轴区域筛选
y_t=np.sum(heat_value,axis=0)
y_list=[]
for i in range(0,len(y_t)):
    if y_t[i]<=20:
        y_list.append(i)
heat_value=np.delete(heat_value,y_list,axis=1)
y_list.reverse()
for i in y_list: 
    del(y_label[i])

# 匹配soma数量
with open("..\\Data\\Data_Statistics.csv") as f:
    reader = csv.reader(f)
    num_map=np.array(list(reader))
    num_list=list(map(str,num_map[:,0]))
    f.close()

# 构建namelist 名称可以修改为简写
x_name=[]
y_name=[]
x_count=[]
y_count=[]
for x in x_label:
    x_count.append(int(num_map[num_list.index(x),1]))
    x_name.append(name_map[id_list.index(x)][3]+" ("+num_map[num_list.index(x),1]+")") 
for x in y_label:
    y_count.append(int(num_map[num_list.index(x),1]))
    y_name.append(name_map[id_list.index(x)][3]+" ("+num_map[num_list.index(x),1]+")")
# 数量筛选
id_t=[]
for i in range(0,len(x_count)):
    if x_count[i]>=20:
        id_t.append(i)

print("soma region x count:")
print(x_count)
print("projection region y count:")
print(y_count)
heat_value=np.array(heat_value)
x_name=np.array(x_name)

# 画图
#sns_plot = sns.heatmap(heat_value)
sns_plot = sns.clustermap(data=heat_value[id_t],
                          xticklabels=y_name,yticklabels=x_name[id_t],
                          )

plt.show()

'''
## 对于CTX/TH区域的结果
# 读入文件
path="..\\Heatmap_Data_cor_tha\\Heatmap_depth_8_cor_tha.csv"
with open(path) as file_object:
    reader = csv.reader(file_object)
    pair_map=list(reader)
    x_label=[]
    y_label=[]
    file_object.close()
    for x in pair_map:
        if structure_map[id_list.index(x[0])][4]=='549': #选择区域
            x_label.append(x[0])
            y_label.append(x[1])
    
    x_label=list(set(x_label))
    y_label=list(set(y_label))
    heat_value=np.zeros((len(x_label),len(y_label)))         
    for x in pair_map:
        if structure_map[id_list.index(x[0])][4]=='549': #选择区域
            heat_value[x_label.index(x[0])][y_label.index(x[1])]=math.log(float(x[4])+0.0001)#Axons
#        heat_value[x_label.index(x[0])][y_label.index(x[1])]=float(x[4])#Axons
         

# y轴区域筛选
y_t=np.sum(heat_value,axis=0)
y_list=[]
for i in range(0,len(y_t)):
    if y_t[i]<=50:
        y_list.append(i)
heat_value=np.delete(heat_value,y_list,axis=1)
y_list.reverse()
for i in y_list: 
    del(y_label[i])

# 匹配soma数量
with open("..\\Data\\Data_Statistics.csv") as f:
    reader = csv.reader(f)
    num_map=np.array(list(reader))
    num_list=list(map(str,num_map[:,0]))
    f.close()

# 构建namelist
x_name=[]
y_name=[]
x_count=[]
y_count=[]
for x in x_label:
    x_count.append(int(num_map[num_list.index(x),1]))
    x_name.append(name_map[id_list.index(x)][2]+" ("+num_map[num_list.index(x),1]+")")
for x in y_label:
    y_count.append(int(num_map[num_list.index(x),1]))
    y_name.append(name_map[id_list.index(x)][2]+" ("+num_map[num_list.index(x),1]+")")
    
# 数量筛选
id_t=[]
for i in range(0,len(x_count)):
    if x_count[i]>=20:
        id_t.append(i)

print("soma region x count:")
print(x_count)
print("projection region y count:")
print(y_count)
heat_value=np.array(heat_value)
x_name=np.array(x_name)
#sns_plot = sns.heatmap(heat_value)
sns_plot = sns.clustermap(heat_value[id_t],xticklabels=y_name,yticklabels=x_name[id_t],col_cluster=False)
# fig.savefig("heatmap.pdf", bbox_inches='tight') # 减少边缘空白
plt.show()
'''