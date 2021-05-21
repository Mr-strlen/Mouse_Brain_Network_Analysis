import math
import BasicFunction as BF
import os
import SimpleITK as sitk
import csv
import numpy as np

# y轴在nrrd文件中并没有做反转
'''
diskname=BF.get_disklist()
img = sitk.ReadImage(diskname+'\\Vaa3D\\Other Information\\annotation_25.nrrd')
imarray=sitk.GetArrayViewFromImage(img)


with open('17109_1701_x8048_y22277.semi_r.swc') as file_object:
    contents = file_object.readlines()
for i in range(1,len(contents)):
    temp=contents[i].split( )
    t1=list(map(float,temp))
    # areaid=int(imarray[math.floor(t1[4]),math.floor(319-t1[3]),math.floor(t1[2])])
    areaid=int(imarray[math.floor(t1[4]),math.floor(t1[3]),math.floor(t1[2])])
    if areaid==0:
        print(contents[i])
        if int(imarray[math.floor(t1[4])+1,math.floor(t1[3]),math.floor(t1[2])])!=0 or \
            int(imarray[math.floor(t1[4]),math.floor(t1[3])+1,math.floor(t1[2])])!=0 or \
            int(imarray[math.floor(t1[4]),math.floor(t1[3]),math.floor(t1[2])+1])!=0 or \
            int(imarray[math.floor(t1[4])+1,math.floor(t1[3])+1,math.floor(t1[2])])!=0 or \
            int(imarray[math.floor(t1[4])+1,math.floor(t1[3]),math.floor(t1[2])+1])!=0 or \
            int(imarray[math.floor(t1[4]),math.floor(t1[3])+1,math.floor(t1[2])+1])!=0 or \
            int(imarray[math.floor(t1[4])+1,math.floor(t1[3])+1,math.floor(t1[2])+1])!=0:
                print("gu")
'''
'''
endstr = ''
with open('test.swc','w+') as f:
    f.write(endstr.join(contents))
    f.close()
'''
'''
# 统计x y z 最大值，是否和nrrd文件匹配
path = "..\\Out"
empty=[]
maxt=[0,0,0]
for root,dirs,files in os.walk(path,topdown=True):
    for name in files:
        with open(os.path.join(root,name)) as file_object:
            contents = file_object.readlines()
            print(len(contents))
            file_object.close()
            t=name.split('.')
            while contents[0][0]=='#':
                del contents[0]
            for x in contents:
                x=x.strip("\n")
                t1=x.split( )
                if float(t1[3])>maxt[0]:
                    maxt[0]=float(t1[3])
                if float(t1[4])>maxt[1]:
                    maxt[1]=float(t1[4])
                if float(t1[5])>maxt[2]:
                    maxt[2]=float(t1[5])
# [567.74, 319.828, 442.00800000000004]
'''

'''
# 比对推荐深度和统计深度的关系
# 就是所有的细胞区域列表是否都在推荐列表内
import csv
import numpy as np
with open("..\\Data\\Dataset_Structure.csv", "r") as f1:
    reader = csv.reader(f1)
    result = list(reader)
    result=np.array(result)
    f1.close()

diskname=BF.get_disklist()
path="E:\\Vaa3D\\Other Information\\Soma_region_and_location.xlsx"
#path="E:\\Vaa3D\\Other Information\\Soma_region_and_location.xlsx"
area_list_soma = BF.read_xlsx(path,'Sheet1')
del area_list_soma[0]
area_list_soma=np.array(area_list_soma)
area_list_soma=list(set(area_list_soma[:,4].tolist())) #统计深度

path="E:\\Vaa3D\\Other Information\\Selected_Regions.xlsx"
area_list_region = BF.read_xlsx(path,'Sheet1')
del area_list_region[0]
area_list_region=np.array(area_list_region)
area_list_region=list(set(area_list_region[:,2].tolist()))

for x in area_list_soma:
    if x not in area_list_region:
        print(x)
# 只有unknown 不在列表里，这是合理的
'''
import matplotlib.pyplot as plt
## 比对branch和axon分布
with open("..\\Data\\Reco_Dataset_Cell.csv", "r") as f:
    reader = csv.reader(f)
    axon_data =np.array(list(reader))
    f.close()
with open("..\\Data\\Reco_Dataset_Branchnum.csv", "r") as f:
    reader = csv.reader(f)
    branch_data =np.array(list(reader))
    f.close()
axon_list=axon_data[:,4].tolist()
soma_list=list(set(axon_list))
branch_list=branch_data[:,3].tolist()
# 对于特定soma的两个同映射分布
axon_dis=[]
branch_dis=[] 
for i in range(0, len(soma_list)):
    t1=np.where(axon_data[:,4]==soma_list[i])
    td1=axon_data[t1,:]
    td1=td1[0]
    t2=np.where(branch_data[:,3]==soma_list[i])
    td2=branch_data[t2,:]
    td2=td2[0]
    
    d1=[]
    d2=[]
    for x in td2:
        if x[1] in td1[:,1]:
            d1.append(float(td1[np.where(td1[:,1]==x[1]),2]))
            d2.append(float(x[2]))
    for x in d1:
        axon_dis.append(x)
    for x in d2:
        branch_dis.append(x)
    '''
    if len(d1)==0:
        continue
    elif len(d1)==1:
        axon_dis.append(1)
        branch_dis.append(1)
        continue
    for x in d1:
        axon_dis.append((x-min(d1))/(max(d1)-min(d1)))
    for x in d2:
        branch_dis.append((x-min(d2))/(max(d2)-min(d2)))
    '''

axon_dis=np.array(axon_dis)
branch_dis=np.array(branch_dis)
import random
for i in range(0, 100):
    t=random.sample(range(1,len(axon_dis)), 500)
    print(np.corrcoef(axon_dis[t],branch_dis[t]))




