## 整合所有文件 生成Dataset_Soma和Dataset_Cell 但是这里没有区分左右部分

#刷新 Structure文件
import os
import BasicFunction as BF
os.system("python 01RegionStructureCreat.py")
'''
def MergeTxt(filepath,outfile):
    k = open(filepath+outfile, 'a+')
    for parent, dirnames, filenames in os.walk(filepath):
        for filepath in filenames:
            txtPath = os.path.join(parent, filepath) # txtpath就是所有文件夹的路
            f = open(txtPath)
            k.write(f.read()+"\n")
    k.close()
    print("finished")
#1. 所有以线段为单位的原始数据整合
MergeTxt("..\\Out\\","..\\Dataset.txt")
'''
#2. 以某个细胞内包含所有区域及其轴突，树突长度的整合 soma_region_id | region_id | axon length type=2 | dendrite length type=3,4
import csv
import shutil
shutil.rmtree("..\\Error_Data")
os.mkdir("..\\Error_Data")  #问题文件

struct_list=[]
with open("..\\Data\\Dataset_Structure.csv", "r") as f1:
    reader = csv.reader(f1)
    result = list(reader)
    for x in result:
        struct_list.append(x[0])
    f1.close()
f2=open('..\\Data\\Dataset_Structure.csv','a',newline='')
csv_writer = csv.writer(f2)
add_set=[] # 其他没有匹配到的区域

empty=[]
empty_t=[]
path = "..\\Out"
for root,dirs,files in os.walk(path,topdown=True):
    for name in files:
        with open(os.path.join(root,name)) as file_object:
            temp=name.split('.')
            temp=temp[0][0:-4]
            contents = file_object.readlines()
            id_set=[];
            file_object.close()
            
            # 移除soma失配或在区域外的神经元
            if (contents[0].split(','))[-4]=='0' or (contents[0].split(','))[-4]=='-1':
                 shutil.move(os.path.join(root,name), "..\\Error_Data\\")
                 print(name)
                 continue
            linecount=0
            # Dataset_Soma 计算
            for x in contents:
                linecount=linecount+1
                t1=x.split(',')
                id_set.append(int(t1[-4]))
                if int(t1[-5])== -1 and linecount<=10: #存在一些分支不在主干上，所以必须为前面几行
                    if t1[-4] not in struct_list: #不在结构记录中的神经元
                        print(t1[-4])
                        empty_t.append([t1[-4],temp,t1[-4]])
                        add_set.append(t1[-4])
                        print(name)
                    else:
                        empty_t.append([t1[-4],temp,result[struct_list.index(t1[-4])][-1]])
            
            # Dataset_Cell 计算    
            id_set=list(set(id_set))
            #构建长度统计
            count_list=[];
            for i in range(0,len(id_set)):
                count_list.append([0,0])
            for x in contents:
                t1=x.split(',')
                t=id_set.index(int(t1[-4]))
                if t1[1]=='2':
                    count_list[t][0]=count_list[t][0]+float(t1[-3]);
                elif t1[1]=='3' or t1[1]=='4':
                    count_list[t][1]=count_list[t][1]+float(t1[-3]);
            t1=contents[0].split(',')
            for i in range(0,len(id_set)):
                empty.append([t1[-4],str(id_set[i]),str(count_list[i][0]),str(count_list[i][1]),temp])


# 添加没有匹配到的区域
add_set=list(set(add_set))
for rows in add_set:
    csv_writer.writerow([rows,"/"+rows+"/","Add Areas "+rows,"Add Areas "+rows,1])
f2.close()


with open("..\\Data\\Dataset_Cell.csv","w+",newline='') as f:
    csv_writer = csv.writer(f)
    for rows in empty:
        csv_writer.writerow(rows)
    f.close()


#3. soma对应区域id soma_region_id | soma_id | depth | soma_areas(cell type)
import numpy as np
path="..\\Other Information\\Soma_region_and_location.xls"
#path="E:\\Vaa3D\\Other Information\\Soma_region_and_location.xlsx"
area_list = BF.read_xlsx(path,'Sheet1')
del area_list[0]
area_list=np.array(area_list)
area_name=area_list[:,0].tolist()
for i in range(0,len(empty_t)):
    if empty_t[i][1] in area_name:
        empty_t[i].append(str(area_list[area_name.index(empty_t[i][1]),4]))
    else:
        print(result[i][1]+' not find')

endstr='\n'
with open("..\\Data\\Dataset_Soma.csv","w+",newline='') as f:
    csv_writer = csv.writer(f)
    for rows in empty_t:
        csv_writer.writerow(rows)
    f.close()