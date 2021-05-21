## 画图 辅助描述

import os
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import BasicFunction as BF
import numpy as np
import SimpleITK as sitk
import math
import csv
from mpl_toolkits.mplot3d import Axes3D
'''
## 单个细胞不同颜色
color_dic=dict()
fig = plt.figure()
point=[[],[],[]]
ax = fig.gca(projection='3d')
path = "..\\Out_Downsample"
for root,dirs,files in os.walk(path,topdown=True):
    #files=files[2:3]
    #print("文件◎",os.path.join(root,name))
    for name in files[0:1]:
        print(name)
        with open(os.path.join(root,name)) as file_object:
            reader = csv.reader(file_object)
            contents=list(reader)
            file_object.close()
            id_set=[]
            # 建立颜色区域dic
            for t1 in contents:
                id_set.append(t1[7])
            id_set=list(set(id_set))
            for x in id_set:
                if x not in color_dic.keys():
                    color_dic[x]=BF.randomcolor()
            

            #整体图像
            for t1 in contents:
                del t1[9:11]
                t1=list(map(float,t1))
                if int(t1[6])!=-1:
                    t2=contents[int(t1[6])-1]
                    del t2[9:11]
                    color_id=t2[7]
                    t2=list(map(float,t2))
                    x=[t1[2],t2[2]]
                    y=[t1[3],t2[3]]
                    z=[t1[4],t2[4]]
                    ax.plot(x, y, z, color_dic[color_id])
#plt.show()
'''
## 降采样结果对比
color_dic={'3': '#EDB120', '2': '#77AC30', '1': '#A2142F'}
fig = plt.figure()
point=[[],[],[]]
ax1 = fig.add_subplot(1, 2, 1, projection='3d')
ax2 = fig.add_subplot(1, 2, 2, projection='3d')
#原始图
with open('..\\Out\\18453_3225_x17398_y19713_cul.csv') as file_object:
    reader = csv.reader(file_object)
    contents=list(reader)
    file_object.close()
    id_set=[]
    # 建立颜色区域dic
    for t1 in contents:
        id_set.append(t1[1])
    id_set=list(set(id_set))
    for x in id_set:
        if x not in color_dic.keys():
            color_dic[x]=BF.randomcolor()
    #整体图像
    for t1 in contents:
        del t1[9:11]
        t1=list(map(float,t1))
        if int(t1[6])!=-1:
            t2=contents[int(t1[6])-1]
            del t2[9:11]
            color_id=t2[1]
            t2=list(map(float,t2))
            x=[t1[2],t2[2]]
            y=[t1[3],t2[3]]
            z=[t1[4],t2[4]]
            ax1.plot(x, y, z, color_dic[color_id])

# 降采样
with open('..\\Out_Downsample\\18453_3225_x17398_y19713_downsample.csv') as file_object:
    reader = csv.reader(file_object)
    contents=list(reader)
    file_object.close()
    id_set=[]
    # 建立颜色区域dic
    for t1 in contents:
        id_set.append(t1[1])
    id_set=list(set(id_set))
    for x in id_set:
        if x not in color_dic.keys():
            print(x)
            color_dic[x]=BF.randomcolor()
    
    #整体图像
    for t1 in contents:
        del t1[9:11]
        t1=list(map(float,t1))
        if int(t1[6])!=-1:
            t2=contents[int(t1[6])-1]
            del t2[9:11]
            color_id=t2[1]
            t2=list(map(float,t2))
            x=[t1[2],t2[2]]
            y=[t1[3],t2[3]]
            z=[t1[4],t2[4]]
            ax2.plot(x, y, z, color_dic[color_id])
#plt.show()

'''
## 单个细胞 按照每个叶子结点的序列去画

data=[]
path = "..\\Out_Downsample"
for root,dirs,files in os.walk(path,topdown=True):
    for name in files[0:1]:
        with open(os.path.join(root,name)) as file_object:
            reader = csv.reader(file_object)
            contents=list(reader)
        draw_mark=np.zeros([len(contents),1])
        #寻找叶子结点
        for n in contents:
            if n[10]=='0':
                data_temp=[]
                t1=n
                while True:
                    if draw_mark[int(t1[0])-1]==1:
                        break;
                    data_temp.append([float(t1[2]),float(t1[3]),float(t1[4])])
                    draw_mark[int(t1[0])-1]=1
                    if t1[6]=='-1':
                        break
                    t1=contents[int(t1[6])-1]
                data.append(data_temp)
'''                    
'''
## 全脑散点图
xs=[[],[],[],[]]
ys=[[],[],[],[]]
zs=[[],[],[],[]]
c_list=[[],[],[],[]]
with open("..\\Data\\Dataset_Structure.csv", "r") as f:
    reader = csv.reader(f)
    structure_info = np.array(list(reader))
    f.close()
    
pair_list=list(map(str,structure_info[:,0]))
img = sitk.ReadImage('..\\Data\\annotation_25.nrrd')
imarray=sitk.GetArrayViewFromImage(img)
pair_color=dict()
for x in pair_list:
    pair_color[x]=BF.randomcolor()
size=np.shape(imarray)
fig = plt.figure()

# plot(221)
for i in range(1,int(size[0]/2)):
    for j in range(int(size[1]/2),size[1]-1):
        for k in range(1,size[2]-1):
            if imarray[i,j,k]!=imarray[i+1,j,k] or imarray[i,j,k]!=imarray[i,j+1,k] or imarray[i,j,k]!=imarray[i,j,k+1]:
                xs[0].append(i)
                ys[0].append(j)
                zs[0].append(k)
                c_list[0].append(pair_color[str(imarray[i,j,k])])
ax = fig.add_subplot(221, projection='3d')
ax.scatter(xs[0], ys[0], zs[0],c=c_list[0])  

# plot(222)
for i in range(int(size[0]/2),size[0]-1):
    for j in range(int(size[1]/2),size[1]-1):
        for k in range(1,size[2]-1):
            if imarray[i,j,k]!=imarray[i+1,j,k] or imarray[i,j,k]!=imarray[i,j+1,k] or imarray[i,j,k]!=imarray[i,j,k+1]:
                xs[1].append(i)
                ys[1].append(j)
                zs[1].append(k)
                c_list[1].append(pair_color[str(imarray[i,j,k])])
ax = fig.add_subplot(222, projection='3d')
ax.scatter(xs[1], ys[1], zs[1],c=c_list[1])

# plot(223)
for i in range(1,int(size[0]/2)):
    for j in range(1,int(size[1]/2)):
        for k in range(1,size[2]-1):
            if imarray[i,j,k]!=imarray[i+1,j,k] or imarray[i,j,k]!=imarray[i,j+1,k] or imarray[i,j,k]!=imarray[i,j,k+1]:
                xs[2].append(i)
                ys[2].append(j)
                zs[2].append(k)
                c_list[2].append(pair_color[str(imarray[i,j,k])])
ax = fig.add_subplot(223, projection='3d')
ax.scatter(xs[2], ys[2], zs[2],c=c_list[2])

# plot(224)
for i in range(int(size[0]/2),size[0]-1):
    for j in range(1,int(size[1]/2)):
        for k in range(1,size[2]-1):
            if imarray[i,j,k]!=imarray[i+1,j,k] or imarray[i,j,k]!=imarray[i,j+1,k] or imarray[i,j,k]!=imarray[i,j,k+1]:
                xs[3].append(i)
                ys[3].append(j)
                zs[3].append(k)
                c_list[3].append(pair_color[str(imarray[i,j,k])])
ax = fig.add_subplot(224, projection='3d')
ax.scatter(xs[3], ys[3], zs[3],c=c_list[3])

plt.show()
'''

'''
## 指定n个细胞生成对应swc文件 并将不同投射区域用不同颜色标记 在Vaa3d中画图
path=['..\\Out\\17109_1701_x8048_y22277_cul.txt',
      '..\\Out\\17109_1801_x6698_y12550_cul.txt']
region_set=[]
for pp in path:
    with open(pp) as f:
        contents = f.readlines()
        print(len(contents))
        f.close()
        for i in range(0,len(contents)):
            temp=contents[i].split( )
            region_set.append(temp[-3])
region_set=list(set(region_set))
color_set=dict()
for i in range(0,len(region_set)):
    color_set[region_set[i]]=str(i)
    
for pp in path:
    empty=['##n type x y z r parent']
    with open(pp) as f:
        contents = f.readlines()
        f.close()
        for x in contents:
            temp=x.split( )
            empty.append(temp[1]+' '+color_set[temp[-3]]+' '+ temp[3]+' '+temp[4]+' '+temp[5]+' '+temp[6]+' '+temp[7])

    t=pp.split('.')
    t=t[2].split('\\')
    endstr = '\n'
    with open(".\\"+t[-1]+"_change.swc","w+") as f:
        f.write(endstr.join(empty))
        f.close()
'''


'''
import shutil
for pp in path:
    shutil.copy('F:\\Vaa3D\\Data\\1708_registered_model\\'+pp+'.semi_r.swc','.\\plotdata\\')
'''
'''
# CTX-TH通路连接
path=['18453_3456_x24161_y6646',
      '18455_00124']
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

color_dic=dict()
for i in range(1,3):
    for j in range(1,5):
        color_dic[i,j]=BF.randomcolor()
count=0
for pp in path:
    count=count+1
    with open('..\\Out\\'+pp+'_cul.txt') as f:
        contents = f.readlines()
        print(len(contents))
        f.close()
        for x in contents:
            t1=x.split( )
            del t1[0]
            t1=list(map(float,t1))
            if int(t1[-3])!=-1:
                t2=contents[int(t1[-3])-1].split( )
                del t2[0]
                t2=list(map(float,t2))
                x=[t1[2],t2[2]]
                y=[t1[3],t2[3]]
                z=[t1[4],t2[4]]
                ax.plot(x, y, z, color_dic[count,int(t2[1])],linewidth='2')
plt.show()
'''


