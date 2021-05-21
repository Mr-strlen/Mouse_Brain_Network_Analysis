'''
单个神经元的数据统计
'''
'''
import csv
import numpy as np
###  根据区域id list 得到区域名称 ###
def getregionname(id_list,aa):
    # 如果有同侧异侧标记
    side_list=[]
    if 'side' in str(aa):
        for i in range(0,len(id_list)):
            x=id_list[i].split('_')
            side_list.append(x[1])
            x=x[0]
            id_list[i]=x
        aa=int(aa[-1])
        
    name_list=[]
    with open("..\\Data\\Dataset_Structure.csv", "r") as f:
        reader = csv.reader(f)
        struct_data=np.array(list(reader))
        area_list=struct_data[:,0].tolist()
        for i in range(0,len(id_list)):
            t= area_list.index(id_list[i])
            t1=struct_data[t,2+aa].tolist()
            if len(side_list):
                name_list.append(t1+'_'+side_list[i][0:3])
            else:
                name_list.append(t1)
    return name_list

## axon dendrite长度 在不同区域的长度 柱状图 Reco_Dataset_Cell.csv 文件中
neuron_id="17109_1701_x8048_y22277"
with open("..\\Data\\Reco_Dataset_Cell.csv", "r") as f:
    reader = csv.reader(f)
    statistics = np.array(list(reader))
temp=np.where(statistics[:,5]==neuron_id)[0]
temp=statistics[temp,:]
temp = temp[np.argsort(-temp[:,3].astype(np.float64))]
name=[]
for i in range(0,len(temp)):
    name.append(temp[i,1]+'_'+temp[i,2][0:3])
print(getregionname(name,'side1'))
'''

import BasicFunction as BF
# 返回第n层的结构
def path_gen(depth,name,path_list):
    kk=[]
    record='000'
    for x in path_list:
        if len(x)>depth+1 and x[depth]==name and record!=x[depth+1]:
            record=x[depth+1]
            kk.append(path_gen(depth+1,x[depth+1],path_list))
    realname=BF.getregionname([name],1)[0]
    if len(kk)==0:
        temp={'name':realname}
    else:
        temp={'name':realname,'children':kk}
    return temp
## 径向树状图
import json
import csv
import numpy as np
article_info = {}
data = json.loads(json.dumps(article_info))
with open("..\\Data\\Reco_Dataset_Path.csv", "r") as f:
    reader = csv.reader(f)
    path = np.array(list(reader))
with open("..\\Data\\Reco_Dataset_PathLength.csv", "r") as f:
    reader = csv.reader(f)
    length = list(reader)
neuron_id='17109_1701_x8048_y22277'
t=np.where(path[:,1]==neuron_id)[0]
neuron_path=path[t,0]
neuron_length=[]
for i in range(0,len(length)):
    if path[i][-1]==neuron_id:
        neuron_length.append(length[i][0:-1])
data_temp={}
# 构建树结构
threshold=1000
path_list=[]
for i in range(0,len(neuron_path)):
    # 删除总长度不到threshold的投射分支
    if np.sum(np.array(neuron_length[i]).astype(float)) > threshold:
        temp=neuron_path[i].split('<-')
        temp.reverse()
        path_list.append(temp)
cc=path_gen(0,path_list[0][0],path_list)

article = json.dumps(cc, ensure_ascii=False)
print(article)
'''
# 单个神经元形态的降采样 生成降采样文件
import BasicFunction as BF
import numpy as np
import csv
# 读取深度推荐列表
path="..\\Other Information\\Selected_Regions.xls"
#path="E:\\Vaa3D\\Other Information\\Soma_region_and_location.xls"
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


import os
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
            
        # 修改区域id
        for i in range(0,len(contents)):
            t1=contents[i]
            area_id=match_list.index(t1[7])
            for k in area_list:
                if int(k[1])>int(Structure[area_id][-1]):
                    continue
                if structure_map[area_id][int(k[1])-1]==k[0]:
                    contents[i][7]=str(k[0])
                    break
        
        ## 计算downsample结构
        cut_mark=np.zeros([len(contents),2]) #标记要被删除的列
        len_step=10
        for t1 in contents:
            if t1[10]=='0': #叶子节点 开始回溯区域
                cut_mark[int(t1[0])-1,0]=1
                cut_length=0 # 步长长度统计
                t2=t1
                parent=t2[6]
                child=t2[0]
                while True:
                    # downsample长度判断
                    cut_length=cut_length+float(t2[8])
                    if cut_length>len_step or int(t2[10])>1: #超过步长或者为分支结点
                        cut_length=0
                        cut_mark[int(t2[0])-1,0]=1
                        parent=t2[0]
                        contents[int(child)-1][6]=parent
                        child=t2[0]
                    if t2[6]=='-1': # 不能写在while，否则最后一次无法判断 
                        break
                    t2=contents[int(t2[6])-1]
                    if t2[0]==t1[0]: #出现循环
                        print('warning circle: ')
                        print(t1)
                        break
                               
            if t1[6]=='-1': # 根节点不删除
                cut_mark[int(t1[0])-1,0]=1
        count=1
        for i in range(0,len(cut_mark)):
            if cut_mark[i,0]==1:
                cut_mark[i,1]=count
                count=count+1
        for i in range(0,len(cut_mark)):
            if cut_mark[i,0]==1:
                contents[i][0]=str(int(cut_mark[i,1]))
                if contents[i][6]!='-1':
                    contents[i][6]=str(int(cut_mark[int(contents[i][6])-1,1]))
        
        for i in range(len(cut_mark)-1,-1,-1): #倒序删除
            if cut_mark[i,0]!=1:
                del contents[i]
        
        with open("..\\Out_Downsample\\"+temp+"_downsample.csv","w+",newline='') as f:
            csv_writer = csv.writer(f)
            for rows in contents:
                csv_writer.writerow(rows)
            f.close()
'''

        
            


