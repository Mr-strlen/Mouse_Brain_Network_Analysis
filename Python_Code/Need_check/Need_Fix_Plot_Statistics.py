import numpy as np
import matplotlib.pyplot as plt
import csv

# 构建结构map
structure_map=[]
with open("..\\Data\\Dataset_Structure.csv", "r") as f:
    reader = csv.reader(f)
    structure_info = list(reader)
    f.close()
    for x in structure_info:
        t=[]
        temp=x[1].split('/')
        del temp[0]
        del temp[-1]
        for k in temp:
            t.append(k)
        structure_map.append(t)


# region_id 和 region_name 匹配信息
with open("..\\Data\\Data_Statistics.csv", "r") as f1:
    reader = csv.reader(f1)
    statistic_info = np.array(list(reader))
    f1.close()

depth=9
'''
# soma distribution 按照指定depth 指定皮层 画分布图
region_count=[]
region_name=[] 
for i in range(0, len(statistic_info)):
    if int(statistic_info[i,-1])==depth and int(statistic_info[i,1])!=0 and (structure_map[i][3]=='688' or structure_map[i][4]=='549'):
        region_name.append(statistic_info[i,-2])
        region_count.append(int(statistic_info[i,1]))
plt.bar(range(0,len(region_name)), height=region_count, tick_label=region_name,alpha=0.8)
plt.show()            
'''

'''
# axon dendrite distribution 按照指定depth 指定皮层 画分布画图
con_axon=np.empty(shape=(0,6))
con_dendrite=np.empty(shape=(0,6))
for i in range(0, len(statistic_info)):
    if int(statistic_info[i,-1])==depth and float(statistic_info[i,2])!=0 and (structure_map[i][3]=='688' or structure_map[i][4]=='549'):
        con_axon=np.row_stack((con_axon, statistic_info[i,:]))
    if int(statistic_info[i,-1])==depth and float(statistic_info[i,3])!=0 and (structure_map[i][3]=='688' or structure_map[i][4]=='549'):
        con_dendrite=np.row_stack((con_dendrite, statistic_info[i,:]))

# 排序
con_axon = con_axon[np.argsort(-con_axon[:,2].astype(np.float64))]
con_dendrite = con_dendrite[np.argsort(-con_dendrite[:,3].astype(np.float64))]

con_count_axon=list(map(float,con_axon[:,2]))
con_name_axon=list(map(str,con_axon[:,-2]))
con_count_dendrite=list(map(float,con_dendrite[:,3]))
con_name_dendrite=list(map(str,con_dendrite[:,-2]))

# 指定depth画 画图
plt.subplot(211)
plt.bar(range(0,len(con_name_axon[0:10])), con_count_axon[0:10], align="center", color="c", label="axon",tick_label=con_name_axon[0:10], alpha=0.5)
plt.legend()
plt.title('Thalamus distribution')
#plt.ylim([0,80000])


plt.subplot(212)
plt.bar(range(0,len(con_name_dendrite[0:10])), con_count_dendrite[0:10], color="b", align="center", label="dendrite",tick_label=con_name_dendrite[0:10], alpha=0.5)        
plt.legend()
plt.show()

#np.corrcoef(con_count_axon,con_count_dendrite)
'''

# 所有axon投射的长度分布
with open("..\\Data\\Dataset_Cell.csv", "r") as f1:
    reader = csv.reader(f1)
    temp_data = np.array(list(reader))
    f1.close()
temp=list(temp_data[:,2].astype(np.float64))
plt.hist(temp,bins=100,range=(0,200))