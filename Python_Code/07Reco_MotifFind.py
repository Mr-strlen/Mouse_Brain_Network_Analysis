'''
这部分代码比较多，包括：
1. 筛选有效连接 使用axon length 500/25 
'''
import csv
import numpy as np
import matplotlib.pyplot as plt
import os
import BasicFunction as BF
   
### 推荐深度数据 ###
# 使用axon 长度 （长度比例的问题在于，存在一些丰富长度的次要区域会被忽视，所以不适用）
with open("..\\Data\\Reco_Dataset_Cell.csv", "r") as f:
    reader = csv.reader(f)
    Data=list(reader)
    Data.append(['-1','-1', '-1', '-1', '-1', '-1'])
    Data = np.array(Data)
    f.close()

threshold=100/25 #有效连接阈值
connect_data=[]; #有效连接数据
## 统计每个神经元内部投射长度分布
soma_name=Data[0,5]
dist_soma_axon=[]
start=0
end=0
for i in range(0,len(Data)):
    if Data[i,5]!=soma_name:
        for k in range(start,end+1):
            dist_soma_axon.append(np.float(Data[k,3]))
            #添加有效连接
            if np.float(Data[k,3])>threshold:
                connect_data.append(Data[k,:].tolist())

        start=i
        soma_name=Data[i,5]
    else:
        end=i
        
# plt.hist(dist_soma_axon,bins=100,range=[0,100]) # 呈现了所有神经元的个体投射长度占比的分布，就可以设定阈值，例如10% 认为是每个细胞自己的有效连接

'''
## 使用branch 数量分布 废弃
# Warning 这部分没有进行同侧异侧区分
with open("..\\Data\\Reco_Dataset_Branchnum.csv", "r") as f:
    reader = csv.reader(f)
    Data=list(reader)
    Data.append(['-1', '-1', '-1', '-1'])
    Data = np.array(Data)
    f.close()

threshold=1 #有效连接阈值
connect_data=[]; #有效连接数据

## 统计每个神经元内部投射占比的分布
soma_name=Data[0,3]
dist_soma_branch=[]
start=0
end=0
for i in range(0,len(Data)):
    if Data[i,3]!=soma_name:
        for k in range(start,end+1):
            dist_soma_branch.append(np.float(Data[k,2]))
            #添加有效连接
            if np.float(Data[k,2])>=threshold:
                connect_data.append(Data[k,:].tolist())
        
        start=i
        soma_name=Data[i,3]
    else:
        end=i      

plt.hist(dist_soma_branch,bins=100,range=[0,100]) # 呈现了所有神经元的个体投射长度占比的分布，就可以设定阈值，例如10% 认为是每个细胞自己的有效连接
'''


### 根据cell type区域统计 ###
import BasicFunction as BF

path="..\\Other Information\\Soma_region_and_location.xls"
area_data = BF.read_xlsx(path,'Sheet1')
del area_data[0]
area_data=np.array(area_data)

## 删除Error_Data内的soma
for filename in os.listdir('..\\Error_Data\\'):
    temp=filename.split('_cul')
    temp=temp[0]
    t=np.where(area_data[:,0]==temp)
    area_data=np.delete(area_data,t,axis = 0)

area_list=area_data[:,4].tolist()
area_set=set(area_list)
times=[]
for x in area_set:
    times.append([x,area_list.count(x)])
times=np.array(times)
times = times[np.argsort(-times[:,1].astype(np.float64))] #统计了cell type区域划分下，每个区域神经元数量（小于10可以不用考虑了）

### 遍历cell type区域 区域内特征包括同侧和异侧 每个区域内聚类，得到motif ###
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(font_scale=0.6)
import pandas as pd
import scipy.cluster.hierarchy as sch
import math
from sklearn.cluster import KMeans
from sklearn import metrics
import rpy2.robjects as robjects
sns.set()
motif_projmap={} #映射图
motif_projfreq={} #映射图频率
motif_count=[] # 每个区域最终统计的motif的数量
area_calu=np.load(file=".\Save_Data\AreaTimesCalu.npy")
for region_name in range(0,1):#len(times)):
    a_t=times[region_name,0].tolist()# 当前区域名称
    soma_list=[]
    for x in area_data:
        if x[4]==a_t:
            soma_list.append(x[0].tolist())
    #丢掉数量少的区域
    if len(soma_list)<10:
        continue
     # 根据soma_list Data构建对应的投射序列
    projection_list=[]
    for x in soma_list:
        t = np.where(Data[:,5]==x)
        temp= Data[t,1:3].tolist()
        temp=temp[0]
        for k in temp:
            projection_list.append(k[0]+'_'+k[1][0:3])
    projection_list=list(set(projection_list))
    
    # 构建二维矩阵
    heat_value=np.zeros((len(soma_list),len(projection_list))) 
    for i in range(0,len(soma_list)):
        t = np.where(Data[:,5]==soma_list[i])
        temp= Data[t,1:3].tolist()
        t_value=Data[t,3].astype(np.float64)
        t_value=t_value[0]
        temp=temp[0]
        for k in range(0,len(temp)):
            heat_value[i,projection_list.index(temp[k][0]+'_'+temp[k][1][0:3])]=t_value[k]

    ## 归一化 x/total length
    for i in range(0,len(heat_value)):
        sum_t=np.sum(heat_value[i,:])
        heat_value[i,:]=heat_value[i,:]/sum_t
    # 取log
    for i in range(0,np.size(heat_value,0)):
        for j in range(0,np.size(heat_value,1)):
            if heat_value[i,j]!=0:
                heat_value[i,j]=np.log(heat_value[i,j]*100+1)
    # cc=getregionname(projection_list,'side1')
    ## 根据层次聚类步骤重新模拟过程递推
    # sns_plot = sns.clustermap(data=heat_value,xticklabels=cc,col_cluster=False)
    #sns_plot = sns.heatmap(data=heat_value,xticklabels=cc)
    '''
    cc=sns_plot.dendrogram_row.linkage #得到每步聚类过程
    #ccc=sns_plot.dendrogram_row.reordered_ind #重新排序的行索引
    #plt.show()
    
    clustermap=[]
    motifsnum=[]
    maxdepth=0
    for i in range(0,len(heat_value)):
        clustermap.append([i,[i],1,0])
    startnum=len(heat_value)-1
    for x in cc:
        startnum=startnum+1
        t_list=np.array(clustermap)
        t1=np.where(t_list[:,0]==x[0])[0][0]
        t2=np.where(t_list[:,0]==x[1])[0][0]
        tt1=clustermap[t1]
        tt2=clustermap[t2]
        clustermap.append([startnum,list(set(tt1[1]) | set(tt2[1])),len(tt1[1])+len(tt2[1]),max([tt1[2],tt2[2]])+1])
        if maxdepth<max([tt1[2],tt2[2]])+1:
            maxdepth=max([tt1[2],tt2[2]])+1
        del clustermap[max([t1,t2])]
        del clustermap[min([t1,t2])]
        #计算大于10的数量
        t_list=np.array(clustermap)
        motifsnum.append([len(np.where(t_list[:,2]>=10)[0]),maxdepth])
        #if maxdepth==57:
            #break
    
    ## 使用SSE确定分层数
    sse_list = [ ]
    end_length=0
    if len(soma_list)>=50:
        K = range(1, 50)
        end_length=50
    else:
        K=range(1,len(soma_list)-1)
        end_length=len(soma_list)-1
    for k in range(1,end_length): 
        kmeans=KMeans(n_clusters=k,n_jobs = 6) 
        kmeans.fit(heat_value) 
        sse_list.append(kmeans.inertia_)   #model.inertia_返回模型的误差平方和，保存进入列表
    #折线图展示聚类数——SSE曲线
    #plt.figure() 
    #plt.plot(np.array(K), sse_list, 'bx-')
    #plt.rcParams['figure.figsize'] = [12,8]
    #plt.xlabel('分群数量',fontsize=18)
    #plt.ylabel('SSE',fontsize=18)
    #plt.xticks(fontsize=15)
    #plt.yticks(fontsize=15)
    #plt.show()
    
    ## 使用阈值确定分类数量（这里需要确认）
    for i in range(0,len(sse_list)):
        if (max(sse_list)-sse_list[i])/(max(sse_list)-min(sse_list))>0.85:
            break
    class_num=i
    
    
    ## 另一种手肘法 图像对称
    Nc = range(1, 50)
    kmeans = [KMeans(n_clusters=i) for i in Nc]
    score = [kmeans[i].fit(heat_value).score(heat_value) for i in range(len(kmeans))]
    plt.plot(Nc,score)
    plt.xlabel('Number of Clusters')
    plt.ylabel('Score')
    plt.title('Elbow Curve')
    plt.show()


    ## 使用轮廓系数法确认分层数 平均轮廓系数(silhouette_score)最大的k便是最佳聚类数
    clusters = range(2,20)
    sc_scores = []
    for k in clusters:  
        kmeans_model = KMeans(n_clusters=k, n_jobs = 6).fit(heat_value)
        sc_score = metrics.silhouette_score(heat_value, kmeans_model.labels_, metric='euclidean')
        sc_scores.append(sc_score)
        print(sc_scores)
    #作出K—平均轮廓系数曲线
    plt.figure()
    plt.plot(clusters, sc_scores, 'bx-')
    plt.rcParams['figure.figsize'] = [12,8]
    plt.xlabel('分群数量',fontsize=18)
    plt.ylabel('Silhouette Coefficient Score',fontsize=18)  #样本平均轮廓系数
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.show()
    sc_scores.index(max(sc_scores))
    '''
    
    ## 使用R语言中的函数进行聚类 文件流
    # 保存数据
    heat_value_t=heat_value.tolist()
    endstr = '\n'
    with open("..\\Temp\\heat_value.csv","w+",newline='') as f:
        csv_writer = csv.writer(f)
        for rows in heat_value_t:
            csv_writer.writerow(rows)
        f.close()
    if os.path.exists("..\\Temp\\Cluster_Result.csv"):
        os.remove("..\\Temp\\Cluster_Result.csv")
    
    robjects.r.source('..\\R_Code\\Cluster_R.R')
    
    # 读取分类结果
    with open("..\\Temp\\Cluster_Result.csv","r",newline='') as f:
        reader = csv.reader(f)
        label_data=list(reader)
        del label_data[0]
        label_data=np.array(label_data)
        f.close()
    t_cluster=label_data[:,1].astype(int)
    class_num=int(max(t_cluster))
    
    ## 根据上述方法确定分类数量，并生成映射网络
    #kmeans = KMeans(n_clusters=class_num, random_state=0).fit(heat_value)
    #t_cluster= np.array(kmeans.labels_)
    
    # 根据分类结果
    projection_list=np.array(projection_list)
    count=1
    for i in range(1,class_num+1):
        if len(np.where(t_cluster==i)[0])>=10:
            t=heat_value[np.where(t_cluster==i),:][0]
            # 大于3std以外的值
            line_t=np.sum(t, axis=0)
            tt=np.where(line_t>np.mean(line_t)+3*np.std(line_t))[0]
            # 计算每列在整体均值以上的个数，作为frequency
            freq_temp=[]
            for k in tt:
                f_t=np.where(t[:,k]>(np.mean(line_t)/(len(t))))
                freq_temp.append(len(f_t[0])/len(t))
                
            print([i,BF.getregionname(projection_list[tt],'side1')])
            motif_projmap[a_t+'_'+str(i)]=BF.getregionname(projection_list[tt],'side1')
            motif_projfreq[a_t+'_'+str(i)]=freq_temp
            #ax=plt.subplot(3,3,count)
            count=count+1
            #sns.heatmap(t,cmap="YlOrRd",center=2,xticklabels=False)
            #ax.set_title('Motif '+str(i))
            #plt.yticks(rotation=0) 
    if count>1:
        motif_count.append([times[region_name,0].tolist(),times[region_name,1].tolist(),count-1,area_calu[region_name]])


'''
## 绘制motif数量和soma数量/region area的散点和拟合曲线
from scipy import optimize
motif_count=np.array(motif_count)

x0=motif_count[:,2].astype(np.float)
# y0=motif_count[:,1].astype(np.float) # 每个区域motif的分类数和times的关系
y0=motif_count[:,3].astype(np.float) # 每个区域motif的分类数和region area的关系
plt.scatter(x0,y0)
# 直线拟合与绘制
def f_1(x, A, B):
    return A * x + B

A1, B1 = optimize.curve_fit(f_1, x0, y0)[0]
x1 = np.arange(min(x0), max(x0), 0.01)#30和75要对应x0的两个端点，0.01为步长
y1 = A1 * x1 + B1
plt.plot(x1, y1, "blue")
'''

os.chdir("..\\Python_Code")
'''
## igraph 整体画图
import igraph as ig
import cairo
import cv2
g = ig.Graph(directed=True)
node_list=[]
edge_list=[]
edge_weight=[]
edge_width=[]
edge_color=[]
color_list=[]
node_color=[]
for key in list(motif_projmap.keys()):
    t=motif_projmap.get(key)
    temp=key.split("_")
    temp=temp[0]
    if temp+'_Ips' not in node_list:
        node_list.append(temp+'_Ips')
        node_color.append(BF.randomcolor())
    t_color=BF.randomcolor()
    for x in t:
        if x not in node_list:
            node_color.append(BF.randomcolor())
            node_list.append(x)
        edge_list.append((temp+'_Ips',x))
        edge_color.append(t_color)
    t=motif_projfreq.get(key)
    for x in t:
        edge_weight.append(x)
        edge_width.append(7*x)
node_list.append('empty point_up')
node_list.append('empty point_down')
g.add_vertices(node_list)
g.add_edges(edge_list)

g.es['weight']=edge_weight
g.es['width']=edge_width
g.es['color']=edge_color
g.es['arrow_size']=1.5
s_t=[]
l_t=[]
for x in range(0,len(node_list)-2):
    s_t.append(25)
    l_t.append(15)
s_t.append(0)
s_t.append(0)
l_t.append(0)
l_t.append(0)
g.vs['color'] = node_color
g.vs['label'] = node_list
g.vs['size']=s_t
g.vs['label_size']=l_t
# 获取每个点的坐标
area_center=np.load(file=".\Save_Data\AreaCenterHalf.npy")
path="..\\Other Information\\Selected_Regions.xls"
reco_area = BF.read_xlsx(path,'Sheet1')
del reco_area[0]
reco_area=np.array(reco_area)
area_name=reco_area[:,2].tolist()

count=0
node_local=[]
for x in node_list:
    temp=x.split('_')
    if 'empty point' in temp[0]:
        continue
    if temp[0] == 'MB':
        node_local.append((228,300))
    if temp[0] == 'HY':
        node_local.append((228,180))
    if temp[0] not in area_name:
        print(temp[0])
        # node_local.append((1,count))
        # count=count+10
        continue
    t=area_name.index(temp[0])
    if temp[1]=='Ips':
        node_local.append((area_center[t,0],area_center[t,2]))
    elif temp[1]=='Con':
        node_local.append((456-area_center[t,0],area_center[t,2]))
node_local.append((0,0))
node_local.append((456,528))
layout=node_local
out=ig.plot(g,layout=layout,bbox=(912,1056))

out.save('Network.png')
img1 = cv2.imread('Network.png')
img2 = cv2.imread('TwoDemShadow_reverse.jpg')
img2 = cv2.resize(img2,(912,1056))#统一图片大小

combine = cv2.addWeighted(img1,0.8,img2,0.2,0)
graph_name='total.png'
cv2.imwrite('..\\Motif_Images\\'+graph_name, combine, [int(cv2.IMWRITE_JPEG_QUALITY),100])
cv2.imshow('combine',combine)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 保存网络格式
# g=ig.load('igraph_map',format="edges")
# ig.write(g,'igraph_map',format="gml")
'''

## igraph 分区域画图
import igraph as ig
import cairo
import cv2
# 构建所有子图
area_center=np.load(file=".\Save_Data\AreaCenterHalf.npy")
path="..\\Other Information\\Selected_Regions.xls"
reco_area = BF.read_xlsx(path,'Sheet1')
del reco_area[0]
reco_area=np.array(reco_area)
area_name=reco_area[:,2].tolist()

for name in range(0,len(motif_count)): 
    g = ig.Graph(directed=True)
    node_list=[]
    edge_list=[]
    edge_weight=[]
    edge_width=[]
    edge_color=[]
    color_list=[]
    node_color=[]
    for key in list(motif_projmap.keys()):
        t=motif_projmap.get(key)
        temp=key.split("_")
        if temp[0]==motif_count[name][0]:
            temp=temp[0]
            if temp+'_Ips' not in node_list:
                node_list.append(temp+'_Ips')
                node_color.append(BF.randomcolor())
            t_color=BF.randomcolor()
            for x in t:
                if x not in node_list:
                    node_color.append(BF.randomcolor())
                    node_list.append(x)
                edge_list.append((temp+'_Ips',x))
                edge_color.append(t_color)
            t=motif_projfreq.get(key)
            for x in t:
                edge_weight.append(x)
                edge_width.append(7*x)
    node_list.append('empty point_up')
    node_list.append('empty point_down')
    
    g.add_vertices(node_list)
    g.add_edges(edge_list)
    
    s_t=[]
    l_t=[]
    for x in range(0,len(node_list)-2):
        s_t.append(25)
        l_t.append(15)
    s_t.append(0)
    s_t.append(0)
    l_t.append(0)
    l_t.append(0)
    
    g.es['weight']=edge_weight
    g.es['width']=edge_width
    g.es['color']=edge_color
    g.es['arrow_size']=1.5
    
    g.vs['color'] = node_color
    g.vs['label'] = node_list
    g.vs['size']=s_t
    g.vs['label_size']=l_t
    
    # 获取每个点的坐标
    count=0
    node_local=[]
    for x in node_list:
        temp=x.split('_')
        if 'empty point' in temp[0]:
            continue
        if temp[0] == 'MB':
            node_local.append((228,300))
        if temp[0] == 'HY':
            node_local.append((228,180))
        if temp[0] not in area_name:
            print(temp[0])
            #node_local.append((1,count))
            #count=count+10
            continue
        t=area_name.index(temp[0])
        if temp[1]=='Ips':
            node_local.append((area_center[t,0],area_center[t,2]))
        elif temp[1]=='Con':
            node_local.append((456-area_center[t,0],area_center[t,2]))
    node_local.append((0,0))
    node_local.append((456,528))
    layout=node_local
    out=ig.plot(g,layout=layout,bbox=(912,1056))
    out.save('temp.png')
    ## 合并轮廓
    img1 = cv2.imread('temp.png')
    img2 = cv2.imread('TwoDemShadow_reverse.jpg')
    img2 = cv2.resize(img2,(912,1056))#统一图片大小
    
    combine = cv2.addWeighted(img1,0.8,img2,0.2,0)
    graph_name=motif_count[name][0]+'_igraph.png'
    cv2.imwrite('..\\Motif_Images\\'+graph_name, combine, [int(cv2.IMWRITE_JPEG_QUALITY),100])
    #cv2.imshow('dst',dst)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
