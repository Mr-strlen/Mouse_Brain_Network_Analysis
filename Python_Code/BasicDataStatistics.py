'''
对region/cell type上进行统计
生成数据统计文件 region id | soma num | axon len | dendrite len | region name | depth
没有考虑同侧异侧
'''

import os
import csv

# region_id 和 region_name 匹配信息
pair_list=[]
pair_info=[]
structure_map=[]
with open("..\\Data\\Dataset_Structure.csv", "r") as f:
    reader = csv.reader(f)
    structure_info = list(reader)
    f.close()
    for x in structure_info:
        pair_list.append(x[0])
        pair_info.append([0,0,0])
        t=[]
        temp=x[1].split('/')
        del temp[0]
        del temp[-1]
        for k in temp:
            t.append(k)
        structure_map.append(t)

## 每个region的soma数量
path = "..\\Out"
region_list=[];
for root,dirs,files in os.walk(path,topdown=True):
    for name in files:
        with open(os.path.join(root,name)) as file_object:
            contents = list(csv.reader(file_object))
            temp=contents[0]
            region_list.append(temp[7])
            if temp[7]=='0':
                print(name)
            file_object.close()

region_set=list(set(region_list))
for i in range(0,len(region_set)):
    pair_info[pair_list.index(region_set[i])][0]=region_list.count(region_set[i])
    

# 每个region内长度 自己的+直属的
with open("..\\Data\\Dataset_Cell.csv", "r") as f:
    reader = csv.reader(f)
    con_info = list(reader)
    f.close()
    con_set=[]
    for x in con_info:
        con_set.append(x[1]) 

con_set=list(set(con_set))

for i in range(0,len(con_set)):
    for x in con_info:
        if x[1]==con_set[i]:
            pair_info[pair_list.index(con_set[i])][1]=pair_info[pair_list.index(con_set[i])][1]+float(x[2])
            pair_info[pair_list.index(con_set[i])][2]=pair_info[pair_list.index(con_set[i])][2]+float(x[3])


# 从上往下叠加
for i in range(0,len(pair_info)):
    depth=int(structure_info[i][-1])
    for j in range(0,len(pair_info)):
        if depth<int(structure_info[j][-1]) and structure_map[j][depth-1]==pair_list[i]:
            pair_info[i][0]=pair_info[i][0]+pair_info[j][0]
            pair_info[i][1]=pair_info[i][1]+pair_info[j][1]
            pair_info[i][2]=pair_info[i][2]+pair_info[j][2]


# 整合信息统计
empty=[]
for i in range(0,len(pair_info)):
    x=pair_info[i]
    empty.append([structure_info[i][0],x[0],x[1],x[2],structure_info[i][-2],structure_info[i][-1]])

with open('..\\Data\\Data_Statistics.csv','w+',newline='') as f:
       csv_writer = csv.writer(f)
       for rows in empty:
           csv_writer.writerow(rows)
