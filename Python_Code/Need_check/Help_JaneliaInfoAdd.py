## Janelia数据集的基本信息补充到Selected_Regions文件中

import BasicFunction as BF
import numpy as np
import csv
# 读取深度推荐列表
diskname=BF.get_disklist()
path=diskname+"\\Vaa3D\\Other Information\\Selected_Regions.xlsx"
#path="E:\\Vaa3D\\Other Information\\Soma_region_and_location.xlsx"
area_list = BF.read_xlsx(path,'Sheet1')
del area_list[0]
area_list=np.array(area_list)
area_list=area_list.tolist()
# 构建层次图
match_list=[]
structure_map=[]
with open("..\\Data\\Dataset_Structure.csv", "r") as f2:
    reader = csv.reader(f2)
    Structure = list(reader)
    f2.close()
    for x in Structure:
        t=[];
        match_list.append(x[0])
        temp=x[1].split('/')
        del temp[0]
        del temp[-1]
        for k in temp:
            t.append(k)
        structure_map.append(t)

#整合所有文件
import os
info_list=[]
path = "..\\Out"
for root,dirs,files in os.walk(path,topdown=True):
    for name in files:
        if name[0]!='A': #选择所有Janelia数据集数据
            print(name)
            continue
        with open(os.path.join(root,name)) as file_object:
            contents = file_object.readlines()
            file_object.close()
            while contents[0][0]=='#':
                del contents[0]
        temp=name.split('.')
        temp=temp[0].split('_')
        t1=contents[0].split( )
        # 修改区域id
        area_id=match_list.index(t1[-2])
        for k in area_list:
            if int(k[1])>int(Structure[area_id][-1]):
                continue
            if structure_map[area_id][int(k[1])-1]==k[0]:
                t1[-2]=str(k[0])
                t_name=k[2]
                break
        info_list.append([temp[0],int(t1[-2]),t_name])

with open("..\\Data\\Add_Info_Janelia.csv","w+",newline='') as f:
    csv_writer = csv.writer(f)
    for rows in info_list:
        csv_writer.writerow(rows)
    f.close()