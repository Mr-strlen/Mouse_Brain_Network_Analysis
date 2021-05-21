## 按照推荐深度和同侧异侧重新构建每个神经元内的投射长度统计
## Warning 此部分计算时间较长
import BasicFunction as BF
import numpy as np
import csv
# 读取深度推荐列表
path="..\\Other Information\\Selected_Regions.xls"
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
empty=[] # 单个神经元调整深度统计文件
empty_p=[]# 单个神经元投射路径
empty_l=[]# 单个神经元内部不同投射的长度
path = "..\\Out"
for root,dirs,files in os.walk(path,topdown=True):
    for name in files:
        print(name)
        with open(os.path.join(root,name)) as file_object:
            temp=name.split('.')
            temp=temp[0][0:-4]
            reader = csv.reader(file_object)
            contents=list(reader)
            file_object.close()
            id_set=[];
            
            # 确定soma位置
            for i in range(0,120): #AA0754_cul 要到118行
                t1=contents[i]
                if t1[6]=='-1':
                    soma_side=t1[9]
                    break
            
            # 统计匹配组
            for i in range(0,len(contents)):
                t1=contents[i]
                # 修改区域id
                area_id=match_list.index(t1[7])
                for k in area_list:
                    if int(k[1])>int(Structure[area_id][-1]):
                        continue
                    if structure_map[area_id][int(k[1])-1]==k[0]:
                        t1[-4]=str(k[0])
                        contents[i][7]=str(k[0])
                        break
                # 判断同侧异侧关系
                temp_side=t1[9]
                if soma_side==temp_side:
                    side_judge='Ipsilateral'
                elif temp_side=='Out_side':
                    side_judge='Out_side'
                else:
                    side_judge='Contralateral'
                id_set.append(t1[7]+'_'+side_judge)

            # Dataset_Cell 计算    
            id_set=list(set(id_set))

            #构建长度统计
            count_list=[];
            for i in range(0,len(id_set)):
                count_list.append([0,0])
            
            for t1 in contents:
                area_id=match_list.index(t1[-4])
                # 判断同侧异侧关系
                temp_side=t1[9]
                if soma_side==temp_side:
                    side_judge='Ipsilateral'
                elif temp_side=='Out_side':
                    side_judge='Out_side'
                else:
                    side_judge='Contralateral'
                
                t=id_set.index(t1[7]+'_'+side_judge)
                if t1[1]=='2':
                    count_list[t][0]=count_list[t][0]+float(t1[-3]);
                elif t1[1]=='3' or t1[1]=='4':
                    count_list[t][1]=count_list[t][1]+float(t1[-3]);
            t1=contents[0]
            for i in range(0,len(id_set)):
                id_set_t=id_set[i].split('_')
                empty.append([t1[7],id_set_t[0],id_set_t[1],str(count_list[i][0]),str(count_list[i][1]),temp])
             
            ## 遍历叶子节点，生成跨区域分支结构
            region_path=[]
            path_length=[]
            for t1 in contents:
                if t1[10]=='0': #叶子节点 开始回溯区域
                    temp_path=[t1[7]]
                    temp_length=[0.0]
                    cut_length=0 # 步长长度统计
                    t2=t1
                    while t2[6]!='-1':
                        # 跨区域路径判断
                        if temp_path[-1]!=t2[7]:
                            temp_path.append(t2[7])
                            temp_length.append(0.0)
                        temp_length[-1]=temp_length[-1]+float(t2[8])
                        t2=contents[int(t2[6])-1]

                        if t2[0]==t1[0]: #出现循环
                            print('warning circle: ')
                            print(t1)
                            break
                    path_length.append(temp_length)
                    region_path.append("<-".join(temp_path))
                    region_path_set=list(set(region_path))
                
            path_length_set=[]
            # 叠加长度
            for i in region_path_set:
                t=list(np.where(np.array(region_path)==i)[0])
                tt=[]
                for k in t:
                    tt.append(path_length[k])
                path_length_set.append(list(np.sum(np.array(tt),axis=0)))
            # 写入统计文件
            for i in range(0,len(region_path_set)):
                empty_p.append([region_path_set[i],temp])
                path_length_set[i].append(temp)
                empty_l.append(path_length_set[i][0:-1])
            

with open("..\\Data\\Reco_Dataset_Cell.csv","w+",newline='') as f:
    csv_writer = csv.writer(f)
    for rows in empty:
        csv_writer.writerow(rows)
    f.close()

with open("..\\Data\\Reco_Dataset_Path.csv","w+",newline='') as f:
    csv_writer = csv.writer(f)
    for rows in empty_p:
        csv_writer.writerow(rows)
    f.close()

with open("..\\Data\\Reco_Dataset_PathLength.csv","w+",newline='') as f:
    csv_writer = csv.writer(f)
    for rows in empty_l:
        csv_writer.writerow(rows)
    f.close()
