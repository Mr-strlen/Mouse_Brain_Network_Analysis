'''
有关CCFv3模型的转换，中间量统计量生成

Reco_CCF_Data.npy 调整深度后的CCF标准模型矩阵
AreaTimeCalu.npy 调整后模型，每个区域的面积统计
AreaCenterHalf.npy 调整后模型，每个区域的几何中心点
'''
## 推荐深度的CCF模型转换
import BasicFunction as BF
import SimpleITK as sitk
import numpy as np
import matplotlib.pyplot as plt
import os
import csv

# region_id 和 region_name 匹配信息
pair_list=[]
structure_map=[]
with open("..\\Data\\Dataset_Structure.csv", "r") as f:
    reader = csv.reader(f)
    structure_info = list(reader)
    f.close()
    for x in structure_info:
        pair_list.append(x[0])
        t=[]
        temp=x[1].split('/')
        del temp[0]
        del temp[-1]
        for k in temp:
            t.append(k)
        structure_map.append(t)

path="..\\Other Information\\Selected_Regions.xls"
area_list = BF.read_xlsx(path,'Sheet1')
del area_list[0]
area_list=np.array(area_list)
area_name=area_list[:,0].tolist()
area_list=area_list.tolist()
#np.save(file="./Save_Data/RegionName.npy", arr=BF.getregionname(area_name,1))
#np.save(file="./Save_Data/RegionId.npy", arr=area_name)
'''
# 对所有区域生成对应合适深度的列表
select_depth=[]
for i in range(0,len(pair_list)):
    temp='0'
    for k in range(0,len(area_list)):
        if int(area_list[k][1])>int(structure_info[i][-1]):
            continue
        if structure_map[i][int(area_list[k][1])-1]==area_list[k][0]:
            temp=area_list[k][0]
            break
    if temp=='0':
        select_depth.append(pair_list[i])
    else:
        select_depth.append(temp)

## Warning 这个步骤比较慢
# 生成中间量文件 
# 需要先生成转换后的CCF文件和数量统计，之后就可以统计中心坐标点
img = sitk.ReadImage('..\\Other Information\\annotation_25.nrrd')
#padding
imarray=np.zeros([457,321,529])
imarray[0:456,0:320,0:528]=sitk.GetArrayViewFromImage(img)

## warning 这部分非常的慢
# 修改nrrd内的数值到合适深度
for i in range(0,np.shape(imarray)[0]):
    print(i)
    for j in range(0,np.shape(imarray)[1]):
        for k in range(0,np.shape(imarray)[2]):
            if str(int(imarray[i,j,k])) not in pair_list:
                print([i,j,k,imarray[i,j,k]]+' not in pair_list')
                continue
            if str(int(imarray[i,j,k]))=='0':
                continue
            # 修改区域id
            area_id=pair_list.index(str(int(imarray[i,j,k])))
            imarray[i,j,k]=int(select_depth[area_id])
np.save(file="./Save_Data/Reco_CCF_Data.npy", arr=imarray)
'''
'''
## 统计所有区域出现的次数
area_calu=np.zeros(len(area_list))
Reco_Data=np.load(file="./Save_Data/Reco_CCF_Data.npy")
for i in range(0,np.shape(Reco_Data)[0]):
    print(i)
    for j in range(0,np.shape(Reco_Data)[1]):
        for k in range(0,np.shape(Reco_Data)[2]):
            if str(int(Reco_Data[i,j,k])) in area_name:
                t=area_name.index(str(int(Reco_Data[i,j,k])))
                area_calu[t]=area_calu[t]+1

np.save(file="./Save_Data/AreaTimesCalu.npy",arr=area_calu) 
'''
'''
## 计算区域中心 半侧脑区
Reco_Data=np.load(file="./Save_Data/Reco_CCF_Data.npy")
area_calu_half=np.zeros(len(area_list)) # MB 313 HY 1097
area_center=np.zeros([len(area_list),3])
# area_name.append('313')
# area_name.append('1097')
# for i in range(0,np.shape(Reco_Data)[0]):
for i in range(0,259):
    print(i)
    for j in range(0,np.shape(Reco_Data)[1]):
        for k in range(0,np.shape(Reco_Data)[2]):
            if str(int(Reco_Data[i,j,k])) in area_name:
                t=area_name.index(str(int(Reco_Data[i,j,k])))
                area_center[t,0]=area_center[t,0]+i
                area_center[t,1]=area_center[t,1]+j
                area_center[t,2]=area_center[t,2]+k
                area_calu_half[t]=area_calu_half[t]+1
for i in range(0,len(area_calu_half)):
    area_center[i,:]=area_center[i,:]/area_calu_half[i]
np.save(file="./Save_Data/AreaCenterHalf.npy",arr=area_center)
'''
'''
## 生成二维shadow文件 拍到二维上去 删除y轴
Reco_Data=np.load(file="./Save_Data/Reco_CCF_Data.npy")
Area_Center=np.load(file="./Save_Data/AreaCenterHalf.npy")
Reco_Data=Reco_Data[0:456,0:320,0:528]

TwoDemMap=np.zeros([np.shape(Reco_Data)[0],np.shape(Reco_Data)[2]])
for i in range(0,np.shape(Reco_Data)[0]):
    print(i)
    for k in range(0,np.shape(Reco_Data)[2]):
        for j in range(0,np.shape(Reco_Data)[1]):
            if int(Reco_Data[i,j,k])!=0:
                TwoDemMap[i,k]=1
                break
# 边界识别
x=[]
y=[]
z=[]
for i in range(1,np.shape(TwoDemMap)[0]-1):
    for j in range(1,np.shape(TwoDemMap)[1]-1):
        if TwoDemMap[i,j]!=TwoDemMap[i+1,j] or TwoDemMap[i,j]!=TwoDemMap[i-1,j] or TwoDemMap[i,j]!=TwoDemMap[i,j+1] or TwoDemMap[i,j]!=TwoDemMap[i,j-1]:
            x.append(i)
            y.append(j)
            z.append(1)

plt.figure(figsize=(4.56,5.28),dpi=200)
plt.axis('off')
plt.scatter(x, y, z)
# plt.scatter(Area_Center[:,0],Area_Center[:,2],np.ones(316))
plt.savefig('TwoDemShadow.jpg',bbox_inches = 'tight', pad_inches = 0,dpi=200)
# import seaborn as sns
# sns_plot = sns.heatmap(data=TwoDemMap)

# 三维内所有坐标点的位置
#from mpl_toolkits.mplot3d import Axes3D 
#fig = plt.figure()
#ax = Axes3D(fig)
#ax.scatter(Area_Center[:,0],Area_Center[:,1],Area_Center[:,2])
#np.save(file="ShadowMap.npy",arr=TwoDemMap)
'''