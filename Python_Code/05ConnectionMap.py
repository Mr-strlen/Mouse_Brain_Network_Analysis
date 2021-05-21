'''
这里使用最基本的关系图构建方式
1. 根据深度调整后Reco_Dataset_Cell，统计出所有连接关系
2. 填充同侧异侧关系
3. 将连接矩阵中所有的零使用mesoscale connectome替换 
4. 得到关系矩阵
'''
import csv
import numpy as np
import BasicFunction as BF
import matplotlib.pyplot as plt

## 读取Reco_Dataset_Cell得到映射矩阵 
with open("..\\Data\\Reco_Dataset_Cell.csv", "r") as f:
    reader = csv.reader(f)
    data=np.array(list(reader))
region_list=[]
projection_list=[]
for i in data:
    region_list.append(str(i[0]))
    projection_list.append(str(i[1])+'_'+str(i[2]))
region_list=list(set(region_list))
projection_list=list(set(projection_list))
'''
## 填充矩阵 这里很慢
relation_map=np.zeros([len(region_list),len(projection_list)])
relation_count=np.zeros([len(region_list),len(projection_list)]) # 统计每个投射有多少个神经元
for i in range(0,len(region_list)):
    print(i)
    for j in range(0,len(projection_list)):
        t=projection_list[j].split('_')
        r=np.where((data[:,0]==region_list[i]) & (data[:,1]==t[0]) & (data[:,2]==t[1]))[0]
        if len(r)>0:
            for k in r:
                relation_map[i,j]=relation_map[i,j]+data[k,3].astype(float)
                relation_count[i,j]=relation_count[i,j]+1
# 求投射的平均
for i in range(0,len(region_list)):
    for j in range(0,len(projection_list)):
        if relation_count[i,j]>0:
            relation_map[i,j]=relation_map[i,j]/relation_count[i,j]
            # 取log(e)(mm+1)
            if relation_map[i,j]>=40:
                relation_map[i,j]=np.log(relation_map[i,j]/250+1)
            else:
                relation_map[i,j]=0
np.save('.\Save_Data\connection_map',relation_map.astype(np.float64))
'''
projection_list1=BF.getregionname(projection_list,'side1')
region_list1=BF.getregionname(region_list,1)

## 构建反转矩阵
region_list2=[]
projection_list2=[]
for i in range(0,len(region_list1)):
    region_list2.append(region_list1[i]+'_Con')
    region_list1[i]=region_list1[i]+'_Ips'
for x in projection_list1:
    if 'Con' in x:
        projection_list2.append(x.replace('Con','Ips'))
    else:
        projection_list2.append(x.replace('Ips','Con'))

region_list=region_list1+region_list2 #soma区域列表
projection_list=list(set(projection_list1+projection_list2)) # 投射区域列表
'''
## 填充反转后的矩阵 
relation_map=np.load('./Save_Data/connection_map.npy')
relation_matrix=np.zeros([len(region_list),len(projection_list)])
for i in range(0,len(region_list)):
    print(i)
    line=region_list[i].split('_')
    for j in range(0,len(projection_list)):
        if line[1]=='Ips':
            if projection_list[j] in projection_list1:
                relation_matrix[i,j]=relation_map[region_list1.index(region_list[i]),projection_list1.index(projection_list[j])]
        elif line[1]=='Con':
            if projection_list[j] in projection_list2:
                relation_matrix[i,j]=relation_map[region_list2.index(region_list[i]),projection_list2.index(projection_list[j])]
        else:
            print('no matching error')
# np.save('.\Save_Data\connection_matrix_single.npy',relation_matrix.astype(np.float64))
'''
'''
## 使用allen结果填充
## 统计allen结果
# relation_matrix=np.zeros([len(region_list),len(projection_list)])
relation_matrix=np.load('.\Save_Data\connection_matrix_single.npy')
with open('./Allen_Data/normalized_connection_strength.csv') as f:
    reader=csv.reader(f)
    data=np.array(list(reader))
    allen_matrix=data[1:,1:].astype(np.float64)
# 构建矩阵
projection_list_allen=[]
for x in list(data[0,1:]):
    projection_list_allen.append(str(x))
region_list_allen=[]
for x in list(data[1:,0]):
    region_list_allen.append(str(x))

# 填充矩阵
for i in range(0,len(region_list)):
    t=region_list[i].split('_')
    if t[0] not in region_list_allen:
        print(region_list[i]+' not in lines')
        continue
    line=region_list_allen.index(t[0])
    temp=allen_matrix[line,:]
    for j in range(0, len(projection_list)):
        if relation_matrix[i,j]==0:
            if t[1]=='Ips':
                tt=projection_list[j]
            else:
                if 'Ips' in projection_list[j]:
                    tt=projection_list[j].replace('Ips','Con')
                elif 'Con' in projection_list[j]:
                    tt=projection_list[j].replace('Con','Ips')
            if tt in projection_list_allen:
                row=projection_list_allen.index(tt)
                relation_matrix[i,j]=temp[row].astype(np.float64)
            else:
                print(projection_list[j] +' not in rows')
np.save('.\Save_Data\connection_matrix.npy',relation_matrix.astype(np.float64))
'''
relation_matrix=np.load('.\Save_Data\connection_matrix.npy')
'''
with open("connection matrix.csv","w+",newline='') as f:
    csv_writer = csv.writer(f)
    for rows in relation_matrix:
        csv_writer.writerow(rows)
    f.close()
'''

'''
## 输出Linus需要的文件
# 1. 所有区域的名称和他们的大小
area_list=[]
region_size=np.load(file="./Save_Data/AreaTimesCalu.npy")
for x in np.load(file="./Save_Data/RegionName.npy"):
    area_list.append(str(x))

empty=[]
for x in list(set(projection_list+region_list)):
    t=x.split('_')
    if t[0] not in area_list:
        empty.append([x,'0'])
        print(x)
    else:
        empty.append([x,int(region_size[area_list.index(t[0])]/2.0)])
with open("regions-size.csv","w+",newline='') as f:
    csv_writer = csv.writer(f)
    for rows in empty:
        csv_writer.writerow(rows)
    f.close()
with open('data.txt','w') as f:    #设置文件对象   
    f.write('{')
    for i in range(0,len(region_list)):
        for j in range(0, len(projection_list)):
            empty="(("+region_list[i]+",'e'),("+projection_list[j]+",'e')):"+str('%.3f'%relation_matrix[i,j])+","
            if i==len(region_list)-1 and j==len(projection_list)-1:
                empty=empty[0:-1]
            f.write(empty)    
    f.write('}')
    f.close()
'''

region_list.sort()
projection_list.sort()


## igraph 画图
import igraph as ig
import cairo
import cv2
import math

g = ig.Graph(directed=True)
node_list=[]
node_color=[]
edge_list=[]
edge_cost=[]
edge_weight=[]
edge_width=[]
edge_color=[]

for i in range(0,len(region_list)):
    for j in range(0,len(projection_list)):
        if float(relation_matrix[i,j])>0:
            if region_list[i] not in node_list:
                node_list.append(region_list[i])
                node_color.append(BF.randomcolor())
            if projection_list[j] not in node_list:
                node_list.append(projection_list[j])
                node_color.append(BF.randomcolor())
            edge_list.append((region_list[i],projection_list[j]))
            edge_color.append(node_color[node_list.index(region_list[i])])
            edge_weight.append(relation_matrix[i,j])
            edge_cost.append(1/relation_matrix[i,j])
            edge_width.append(relation_matrix[i,j]*10)

#node_list.append('empty point_up')
#node_list.append('empty point_down')
g.add_vertices(node_list)
g.add_edges(edge_list)

g.es['weight']=edge_weight
g.es['cost']=edge_cost
g.es['width']=edge_width
g.es['color']=edge_color
g.es['arrow_size']=1.5

g.vs['color'] = node_color
g.vs['label'] = node_list
g.vs['size']=25
g.vs['label_size']=15
layout=g.layout("fr")
#g.rewire(n=1000, mode='simple')
#out=ig.plot(g,layout=layout,bbox = (2000, 1600))

relation_matrix_single=np.load('.\Save_Data\connection_matrix_single.npy')
g_s = ig.Graph(directed=True)
node_list_s=[]
edge_list_s=[]
edge_weight_s=[]
edge_cost_s=[]
for i in range(0,len(region_list)):
    for j in range(0,len(projection_list)):
        if relation_matrix_single[i,j]>0:
            if region_list[i] not in node_list_s:
                node_list_s.append(region_list[i])
            if projection_list[j] not in node_list_s:
                node_list_s.append(projection_list[j])
            edge_list_s.append((region_list[i],projection_list[j]))
            edge_weight_s.append(relation_matrix_single[i,j])
            edge_cost_s.append(1/relation_matrix_single[i,j])
g_s.add_vertices(node_list_s)
g_s.add_edges(edge_list_s)
g_s.es['weight']=edge_weight_s
g_s.es['cost']=edge_cost_s

g_s.vs['label'] = node_list_s

relation_matrix_middle=np.load('.\Save_Data\connection_matrix_allen.npy')
g_m = ig.Graph(directed=True)
node_list_m=[]
edge_list_m=[]
edge_weight_m=[]
edge_cost_m=[]
for i in range(0,len(region_list)):
    for j in range(0,len(projection_list)):
        if relation_matrix_middle[i,j]>0:
            if region_list[i] not in node_list_m:
                node_list_m.append(region_list[i])
            if projection_list[j] not in node_list_m:
                node_list_m.append(projection_list[j])
            edge_list_m.append((region_list[i],projection_list[j]))
            edge_weight_m.append(relation_matrix_middle[i,j])
            edge_cost_m.append(1/relation_matrix_middle[i,j])
g_m.add_vertices(node_list_m)
g_m.add_edges(edge_list_m)
g_m.es['weight']=edge_weight_m
g_m.es['cost']=edge_cost_m

g_m.vs['label'] = node_list_m



'''
# 获取每个点的坐标
area_center=np.load(file=".\Save_Data\AreaCenterHalf.npy")
area_name=[]
for x in np.load(file=".\Save_Data\RegionName.npy"):
    area_name.append(str(x))

count=30
node_local=[]
for x in node_list:
    temp=x.split('_')
    if 'empty point' in temp[0]:
        continue
    if temp[0] not in area_name:
        print(temp[0])
        node_local.append((1,count))
        count=count+30
        continue
    t=area_name.index(temp[0])
    if temp[1]=='Ips':
        node_local.append((area_center[t,0],area_center[t,2]))
    elif temp[1]=='Con':
        node_local.append((456-area_center[t,0],area_center[t,2]))

node_local.append((0,0))
node_local.append((456,528))


## 画图保存
layout=node_local
out=ig.plot(g,layout=layout,bbox=(912,1056))
#out.save('Network.png')
img1 = cv2.imread('Network.png')
img2 = cv2.imread('TwoDemShadow_reverse.jpg')
img2 = cv2.resize(img2,(912,1056))#统一图片大小

combine = cv2.addWeighted(img1,0.8,img2,0.2,0)
graph_name='total.png'
cv2.imwrite(graph_name, combine, [int(cv2.IMWRITE_JPEG_QUALITY),100])
cv2.imshow('combine',combine)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''

### 网络分析 参考https://kateto.net/netscix2016.html
import random
'''
### 网络形态比较（无向图）
## degree distribution compare
degree_dis=g.degree_distribution()
x=np.array(range(int(degree_dis._min)+1,int(degree_dis._max)+1))
y=[]
for t in degree_dis._bins:
    y.append(t+1)
x=np.log10(x)
y=np.log10(y)

degree_dis=g_s.degree_distribution()
x_s=np.array(range(int(degree_dis._min)+1,int(degree_dis._max)+1))
y_s=[]
for t in degree_dis._bins:
    y_s.append(t+1)
x_s=np.log10(x_s)
y_s=np.log10(y_s)

degree_dis=g_m.degree_distribution()
x_m=np.array(range(int(degree_dis._min)+1,int(degree_dis._max)+1))
y_m=[]
for t in degree_dis._bins:
    y_m.append(t+1)
x_m=np.log10(x_m)
y_m=np.log10(y_m)

g_er=ig.GraphBase.Erdos_Renyi(len(node_list),m=len(edge_list),directed=True,loops=True)
degree_list_er=g_er.degree()
dd=plt.hist(degree_list_er,bins=max(degree_list_er)-min(degree_list_er))
x_er=[]
y_er=[]
for i in dd[1]:
    x_er.append(i+1)
for i in dd[0]:
    y_er.append(i+1)
x_er=x_er[1:]
x_er=np.log10(x_er)
y_er=np.log10(y_er)

g_ws=ig.GraphBase.Watts_Strogatz(1, len(node_list), 33, 0.1, loops=True)

while g_ws.ecount() > g.ecount():
    k=random.randrange(0,g_ws.ecount()-1)
    temp=g_ws
    temp.delete_edges(k)
    if not temp.is_connected():
        continue
    else:
        g_ws.delete_edges(k)
#ig.summary(g_ws)
degree_list_ws=g_ws.degree()
dd=plt.hist(degree_list_ws,bins=max(degree_list_ws)-min(degree_list_ws))
x_ws=[]
y_ws=[]
for i in dd[1]:
    x_ws.append(i+1)
for i in dd[0]:
    y_ws.append(i+1)
x_ws=x_ws[1:]
x_ws=np.log10(x_ws)
y_ws=np.log10(y_ws)

g_ba=ig.GraphBase.Barabasi(n=len(node_list),m=34,directed=True)

while g_ba.ecount() > g.ecount():
    k=random.randrange(0,g_ba.ecount()-1)
    temp=g_ba
    temp.delete_edges(k)
    if not temp.is_connected():
        continue
    else:
        g_ba.delete_edges(k)

ig.summary(g_ba)
degree_list_ba=g_ba.degree()
dd=plt.hist(degree_list_ba,bins=max(degree_list_ba)-min(degree_list_ba))
x_ba=[]
y_ba=[]
for i in dd[1]:
    x_ba.append(i+1)
for i in dd[0]:
    y_ba.append(i+1)
x_ba=x_ba[1:]
x_ba=np.log10(x_ba)
y_ba=np.log10(y_ba)


plt.close()
size=20
alpha_value=0.7
plt.scatter(x,y,alpha=alpha_value)
plt.scatter(x_s,y_s,alpha=alpha_value)
plt.scatter(x_m,y_m,alpha=alpha_value)
plt.scatter(x_er,y_er,marker='+',c='#FF0000',alpha=alpha_value-0.1)
plt.scatter(x_ws,y_ws,marker='x',c='#9400D3',alpha=alpha_value-0.15)
plt.scatter(x_ba,y_ba,marker='o',facecolors='none',edgecolors='#A0522D',alpha=alpha_value-0.2)
plt.legend(['single + mesocpic','single neuron', 'mesoscopic','ER network','Small world','Scale-Free'])
plt.xticks([0,1,2,3],['1','10','100','1000'])
plt.yticks([0,1,2,3],['1','10','100','1000'])
plt.xlabel('Degrees(log)',fontsize=12)
plt.ylabel('Frequency(log)',fontsize=12)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)



plt.close()
bar_width = 0.13
## path length hist
path_legnth_hist=g.path_length_hist()
path_legnth_hist_s=g_s.path_length_hist()
path_legnth_hist_m=g_m.path_length_hist()
(path_legnth_hist_er,_)=g_er.path_length_hist()
(path_legnth_hist_ws,_)=g_ws.path_length_hist()
(path_legnth_hist_ba,_)=g_ba.path_length_hist()
x=np.arange(int(path_legnth_hist._min),int(path_legnth_hist._max))
t1=[]
for k in path_legnth_hist._bins:
    t1.append(int(k))
plt.bar(x, t1, bar_width, align="center")

x=np.arange(int(path_legnth_hist_s._min),int(path_legnth_hist_s._max))
t2=[]
for k in path_legnth_hist_s._bins:
    t2.append(int(k))
plt.bar(x+bar_width*1, t2, bar_width, align="center")

x=np.arange(int(path_legnth_hist_m._min),int(path_legnth_hist_m._max))
t3=[]
for k in path_legnth_hist_m._bins:
    t3.append(int(k))
plt.bar(x+bar_width*2, t3, bar_width, align="center")

plt.bar(np.arange(1,len(path_legnth_hist_er)+1)+bar_width*3, path_legnth_hist_er, bar_width, align="center")
plt.bar(np.arange(1,len(path_legnth_hist_ws)+1)+bar_width*4, path_legnth_hist_ws, bar_width, align="center")
plt.bar(np.arange(1,len(path_legnth_hist_ba[0:7])+1)+bar_width*5, path_legnth_hist_ba[0:7], bar_width, align="center")
plt.legend(['single + mesocpic','single neuron', 'mesoscopic','ER network','Small world','Scale-Free'])
plt.xticks([0.39,1.39,2.39,3.39,4.39,5.39,6.39,7.39,8.39],['0','1','2','3','4','5','6','7','8'])
plt.yticks([0,100000,200000,300000],['0','1e6','2e6','3e6'])
plt.xlabel('Path Length',fontsize=12)
plt.ylabel('Frequency',fontsize=12)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

## diameter and radius
temp=[g_s.diameter(),
      g_m.diameter(),
      g.diameter(),
      g_er.diameter(),
      g_ws.diameter(),
      g_ba.diameter()]
print('diameter:')
print(temp)

temp=[g_s.radius(),
      g_m.radius(),
      g.radius(),
      g_er.radius(),
      g_ws.radius(),
      g_ba.radius()]
print('radius:')
print(temp)

## size of the largest cliques
temp=[g_s.clique_number(),
      g_m.clique_number(),
      g.clique_number(),
      g_er.clique_number(),
      g_ws.clique_number(),
      g_ba.clique_number()]
print('clique_number:')
print(temp)

## average_path_length
temp=[g_s.average_path_length(),
      g_m.average_path_length(),
      g.average_path_length(),
      g_er.average_path_length(),
      g_ws.average_path_length(),
      g_ba.average_path_length()]
print('average_path_length:')
print(temp)

## global transitivity (clustering coefficient) 
temp=[g_s.transitivity_undirected(),
      g_m.transitivity_undirected(),
      g.transitivity_undirected(),
      g_er.transitivity_undirected(),
      g_ws.transitivity_undirected(),
      g_ba.transitivity_undirected()]
print('global transitivity (clustering coefficient):')
print(temp)

## transitivity_avglocal_undirected
# the average of the vertex transitivities of the graph
#Note that this measure is different from the global transitivity measure as it simply takes the average local transitivity across the whole network.
temp=[g_s.transitivity_avglocal_undirected(),
      g_m.transitivity_avglocal_undirected(),
      g.transitivity_avglocal_undirected(),
      g_er.transitivity_avglocal_undirected(),
      g_ws.transitivity_avglocal_undirected(),
      g_ba.transitivity_avglocal_undirected()]
print('average of the vertex transitivities')
print(temp)


## density
if True in g_s.is_loop():
    print('g_s loop')
if True in g_m.is_loop():
    print('g_m loop')
if True in g.is_loop():
    print('g loop')
if True in g_er.is_loop():
    print('g_er loop')
if True in g_ws.is_loop():
    print('g_ws loop')
if True in g_ba.is_loop():
    print('g_ba loop')

temp=[g_s.density(loops=True),
      g_m.density(loops=True),
      g.density(loops=True),
      g_er.density(loops=True),
      g_ws.density(loops=True),
      g_ba.density()]
print('density:')
print(temp)

## the assortativity of a graph based on vertex degrees (同配性)
temp=[g_s.assortativity_degree(),
      g_m.assortativity_degree(),
      g.assortativity_degree(),
      g_er.assortativity_degree(),
      g_ws.assortativity_degree(),
      g_ba.assortativity_degree()]
print('assortativity:')
print(temp)


### 信息传递比较（有向图）
## Triad census distribution
bar_width = 0.1
temp=[[],[],[],[],[],[]]
for x in g.triad_census():
    temp[0].append(np.log10(int(x)+1))
for x in g_s.triad_census():
    temp[1].append(np.log10(int(x)+1))
for x in g_m.triad_census():
    temp[2].append(np.log10(int(x)+1))
for x in g_er.triad_census():
    temp[3].append(np.log10(int(x)+1))
for x in g_ws.triad_census():
    temp[4].append(np.log10(int(x)+1))
for x in g_ba.triad_census():
    temp[5].append(np.log10(int(x)+1))

plt.close()
x=np.arange(1,17)
# plt.bar(x, temp[0], bar_width)
# plt.bar(x+bar_width*1, temp[1], bar_width, align="center")
# plt.bar(x+bar_width*2, temp[2], bar_width, align="center")
# plt.bar(x+bar_width*3, temp[3], bar_width, align="center")
plt.bar(x+bar_width*4, temp[4], bar_width, align="center")
plt.bar(x+bar_width*5, temp[5], bar_width, align="center")
plt.plot(x, temp[0])
plt.plot(x, temp[1])
plt.plot(x, temp[2])
plt.plot(x, temp[3])
plt.plot(x, temp[4])
plt.plot(x, temp[5])
plt.legend(['single + mesocpic','single neuron', 'mesoscopic','ER network','Small world','Scale-Free'])
plt.ylim([0,9])
plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],fontsize=12)
plt.yticks([0,1,2,3,4,5,6,7,8],['1','10','1e2','1e3','1e4','1e5','1e6','1e7','1e8'],fontsize=12)
plt.xlabel('States',fontsize=12)
plt.ylabel('Times(log)',fontsize=12)


'''

## reciprocity 
# Reciprocity defines the proportion of mutual connections in a directed graph
temp=[g_s.reciprocity(),
      g_m.reciprocity(),
      g.reciprocity()]
print('reciprocity:')
print(temp)

## 节点的平均 cost 
temp=[np.sum(g_s.es['cost'])/len(g_s.es['cost']),
      np.sum(g_m.es['cost'])/len(g_m.es['cost']),
      np.sum(g.es['cost'])/len(g.es['cost'])]
print('cost:')
print(temp) 

### 计算网络带权重的效率
def NetworkEfficiency(g):
    efficiency=0
    for i in range(0,len(g.vs['label'])):
        count=0
        temp_e=0
        temp=g.get_shortest_paths(v=g.vs['label'][i],to=g.vs['label'],weights=g.es['cost'],mode='all',output="epath")
        
        for j in range(0,len(temp)):
            if len(temp[j])==0:
                continue
            elif j==i:
                continue
            else:
                count=count+1
                for k in temp[j]:
                    temp_e=temp_e+g.es['weight'][k]
        efficiency=efficiency+temp_e/count
    efficiency=efficiency/len(g.vs['label'])
    return efficiency

# print('combine effic:')
# print(NetworkEfficiency(g))
# print('sinlgle effic:')
# print(NetworkEfficiency(g_s))
# print('Mesoscopic effic:')
# print(NetworkEfficiency(g_m))

hub_node=[]
hub_node_s=[]
hub_node_m=[]
### 5. Hubs, centrality and robustness
print('\n Combine Network')
authority_score=g.authority_score(weights=g.es['weight'])
hub_score=g.hub_score(weights=g.es['weight'])
print('-----hub_score-----')
for x in range(0,len(hub_score)):
    if hub_score[x]> 0.8:
        hub_node.append(g.vs['label'][x])
        print(g.vs['label'][x])
print('authority_score-----')
for x in range(0,len(authority_score)):
    if authority_score[x] > 0.9:
        print(g.vs['label'][x])


print('\n Single Network')
authority_score_s=g_s.authority_score(weights=g_s.es['weight'])
hub_score_s=g_s.hub_score(weights=g_s.es['weight'])
print('-----hub_score-----')
for x in range(0,len(hub_score_s)):
    if hub_score_s[x]> 0.8:
        hub_node_s.append(g_s.vs['label'][x])
        print(g_s.vs['label'][x])
print('-----authority_score-----')
for x in range(0,len(authority_score_s)):
    if authority_score_s[x] > 0.9:
        print(g_s.vs['label'][x])


print('\n Mesoscopic Network')
authority_score_m=g_m.authority_score(weights=g_m.es['weight'])
hub_score_m=g_m.hub_score(weights=g_m.es['weight'])
print('-----hub_score-----')
for x in range(0,len(hub_score_m)):
    if hub_score_m[x]> 0.8:
        hub_node_m.append(g_m.vs['label'][x])
        print(g_m.vs['label'][x])
print('-----authority_score-----')
for x in range(0,len(authority_score_m)):
    if authority_score_m[x] > 0.9:
        print(g_m.vs['label'][x])



## 网络攻击
for x in hub_node:
    t=g.vs['label'].index(x)
    g.delete_vertices(t)

for x in hub_node_s:
    t=g_s.vs['label'].index(x)
    g_s.delete_vertices(t)
    
for x in hub_node_m:
    t=g_m.vs['label'].index(x)
    g_m.delete_vertices(t)
    
print('combine effic after attack:')
print(NetworkEfficiency(g))
print('sinlgle effic after attack:')
print(NetworkEfficiency(g_s))
print('Mesoscopic effic after attack:')
print(NetworkEfficiency(g_m))
'''
## diversity
# The structural diversity index of a vertex is simply the (normalized) Shannon entropy of the weights of the edges incident on the vertex.
# The measure is defined for undirected graphs only; edge directions are ignored.
# g_s.diversity(weights=edge_weight_s)

### 2. clustering coefficient and motifs


## dyad_census
temp=[g_s.dyad_census(),
      g_m.dyad_census(),
      g.dyad_census(),
      g_er.dyad_census(),
      g_ws.dyad_census(),
      g_ba.dyad_census()]
print('dyad_census mutual, asymmetric and null connections')
print(temp)

### 3. Path length and efficiency
## independence_number
# temp=[g_s.independence_number(),
#       g_m.independence_number(),
#       g.independence_number(),
#       g_er.independence_number(),
#       g_ws.independence_number(),
#       g_ba.independence_number()]
# print('independence_number:')
# print(temp)




### 4. connection density or cost



### 5. Hubs, centrality and robustness
print('\n Combine Network')
authority_score=g.authority_score(weights=g.es['weight'])
hub_score=g.hub_score(weights=g.es['weight'])
print('-----hub_score-----')
for x in range(0,len(hub_score)):
    if hub_score[x]> 0.9:
        print(g.vs['label'][x])
print('authority_score-----')
for x in range(0,len(authority_score)):
    if authority_score[x] > 0.9:
        print(g.vs['label'][x])
print('\n Single Network')
authority_score_s=g_s.authority_score(weights=g_s.es['weight'])
hub_score_s=g_s.hub_score(weights=g_s.es['weight'])
print('-----hub_score-----')
for x in range(0,len(hub_score_s)):
    if hub_score_s[x]> 0.9:
        print(g_s.vs['label'][x])
print('-----authority_score-----')
for x in range(0,len(authority_score_s)):
    if authority_score_s[x] > 0.9:
        print(g_s.vs['label'][x])

print('\n Mesoscopic Network')
authority_score_m=g_m.authority_score(weights=g_m.es['weight'])
hub_score_m=g_m.hub_score(weights=g_m.es['weight'])
print('-----hub_score-----')
for x in range(0,len(hub_score_m)):
    if hub_score_m[x]> 0.9:
        print(g_m.vs['label'][x])
print('-----authority_score-----')
for x in range(0,len(authority_score_m)):
    if authority_score_m[x] > 0.9:
        print(g_m.vs['label'][x])
        






### 6. Modularity
## closeness
# temp=[g_s.clique_number(),
#       g_m.clique_number(),
#       g.clique_number(),
#       g_er.clique_number(),
#       g_ws.clique_number(),
#       g_ba.clique_number()]
# print('closeness without weigth:')
# print(temp)

# temp=[g_s.closeness(weights=edge_weight_s),
#       g_m.clique_number(weights=edge_weight_m),
#       g.clique_number(weights=edge_weight)]
# print('closeness with weigth:')
# print(temp)

## betweenness()
## cocitation()
## coreness()
## eccentricity()
## eigenvector_centrality()


## Modularity 需要给定点的标签
#temp=np.ones([len(node_list),1])
#g.modularity(temp,weights=edge_weight)
#g.community_fastgreedy()
'''
'''
### 构建三个网络的无向网络
g = ig.Graph(directed=False)
node_list=[]
edge_list=[]
edge_cost=[]
edge_weight=[]
for i in range(0,len(region_list)):
    for j in range(0,len(projection_list)):
        if float(relation_matrix[i,j])>0:
            if region_list[i] not in node_list:
                node_list.append(region_list[i])
            if projection_list[j] not in node_list:
                node_list.append(projection_list[j])
            if (region_list[i],projection_list[j]) not in edge_list and (projection_list[j],region_list[i]) not in edge_list:
                edge_list.append((region_list[i],projection_list[j]))
                edge_weight.append(relation_matrix[i,j])
                edge_cost.append(1/relation_matrix[i,j])
g.add_vertices(node_list)
g.add_edges(edge_list)
g.es['weight']=edge_weight
g.es['cost']=edge_cost
g.vs['label'] = node_list


relation_matrix_single=np.load('.\Save_Data\connection_matrix_single.npy')
g_s = ig.Graph(directed=False)
node_list_s=[]
edge_list_s=[]
edge_weight_s=[]
edge_cost_s=[]
for i in range(0,len(region_list)):
    for j in range(0,len(projection_list)):
        if relation_matrix_single[i,j]>0:
            if region_list[i] not in node_list_s:
                node_list_s.append(region_list[i])
            if projection_list[j] not in node_list_s:
                node_list_s.append(projection_list[j])
            if (region_list[i],projection_list[j]) not in edge_list_s and (projection_list[j],region_list[i]) not in edge_list_s:
                edge_list_s.append((region_list[i],projection_list[j]))
                edge_weight_s.append(relation_matrix_single[i,j])
                edge_cost_s.append(1/relation_matrix_single[i,j])
g_s.add_vertices(node_list_s)
g_s.add_edges(edge_list_s)
g_s.es['weight']=edge_weight_s
g_s.es['cost']=edge_cost_s
g_s.vs['label'] = node_list_s

relation_matrix_middle=np.load('.\Save_Data\connection_matrix_allen.npy')
g_m = ig.Graph(directed=False)
node_list_m=[]
edge_list_m=[]
edge_weight_m=[]
edge_cost_m=[]
for i in range(0,len(region_list)):
    for j in range(0,len(projection_list)):
        if relation_matrix_middle[i,j]>0:
            if region_list[i] not in node_list_m:
                node_list_m.append(region_list[i])
            if projection_list[j] not in node_list_m:
                node_list_m.append(projection_list[j])
            if (region_list[i],projection_list[j]) not in edge_list_m and (projection_list[j],region_list[i]) not in edge_list_m:
                edge_list_m.append((region_list[i],projection_list[j]))
                edge_weight_m.append(relation_matrix_middle[i,j])
                edge_cost_m.append(1/relation_matrix_middle[i,j])
g_m.add_vertices(node_list_m)
g_m.add_edges(edge_list_m)
g_m.es['weight']=edge_weight_m
g_m.es['cost']=edge_cost_m
g_m.vs['label'] = node_list_m
'''


'''
## cluster 要使用有向图
clu_result=g.clusters()
Q=ig.GraphBase.modularity(g,clu_result.membership)
print(Q)

clu_result=g_s.clusters()
Q=ig.GraphBase.modularity(g_s,clu_result.membership)
print(Q)

clu_result=g_m.clusters()
Q=ig.GraphBase.modularity(g_m,clu_result.membership)
print(Q)

'''
# fastgreedy
# fastgreedy=g.community_fastgreedy(weights=g.es['weight']) # 这里被解释为连接强度
# c=list(fastgreedy.as_clustering()) 
# membership=[]
# for i in range(0,len(g.vs['label'])):
#     membership.append(0)
# for i in range(0,len(c)):
#     for k in c[i]:
#         membership[k]=i
# Q=ig.GraphBase.modularity(g,membership)
# print('fastgreedy:')
# print(Q)

# fastgreedy √
# fastgreedy=g_s.community_fastgreedy(weights=g_s.es['weight']) # 这里被解释为连接强度 无向图
# c=list(fastgreedy.as_clustering()) 
# membership=[]
# for i in range(0,len(g_s.vs['label'])):
#     membership.append(0)
# for i in range(0,len(c)):
#     for k in c[i]:
#         membership[k]=i
# Q=ig.GraphBase.modularity(g_s,membership)
# print(Q)

# fastgreedy=g_m.community_fastgreedy(weights=g_m.es['weight']) # 这里被解释为连接强度
# c=list(fastgreedy.as_clustering()) 
# membership=[]
# for i in range(0,len(g_m.vs['label'])):
#     membership.append(0)
# for i in range(0,len(c)):
#     for k in c[i]:
#         membership[k]=i
# Q=ig.GraphBase.modularity(g_m,membership)
# print(Q)


# 其他聚类方式
# community_edge_betweenness
# community_edge_betweenness=g.community_edge_betweenness(weights=g.es['cost']) # 这里权重被解释为距离
# c=list(community_edge_betweenness.as_clustering(n=100))  
'''
g=g_s
# community_label_propagation 可以有向图
community_label_propagation=g.community_label_propagation(weights=g.es['weight'])# 这里被解释为连接强度
Q=ig.GraphBase.modularity(g,community_label_propagation._membership)
print('community_label_propagation:')
print(Q)

# community_multilevel 无向图 √
# community_multilevel=g.community_multilevel(weights=g.es['weight'], return_levels=False) #这里被解释为连接强度 无向图
# Q=ig.GraphBase.modularity(g,community_multilevel._membership)
# print('community_multilevel:')
# print(Q)


# community_walktrap 可以有向图 √
community_walktrap=g.community_walktrap(weights=g.es['weight'],steps=4) #这里被解释为连接强度 可以有向图
c=list(community_walktrap.as_clustering()) 
membership=[]
for i in range(0,len(g.vs['label'])):
    membership.append(0)
for i in range(0,len(c)):
    nodes=c[i]
    for j in nodes:
        membership[j]=i
Q=ig.GraphBase.modularity(g,membership)
print('community_walktrap:')
print(Q)

# community_leading_eigenvector 无向图 √
# community_leading_eigenvector=g.community_leading_eigenvector(weights=g.es['weight'],clusters=None) #这里被解释为连接强度 
# Q=ig.GraphBase.modularity(g,community_leading_eigenvector._membership)
# print('community_leading_eigenvector:')
# print(Q)


# community_infomap 可以有向 √
community_infomap=g.community_infomap(edge_weights=g.es['weight'])#这里被解释为连接强度 
Q=ig.GraphBase.modularity(g,community_infomap._membership)
print('community_infomap:')
print(Q)


#community_spinglass 这里被解释为连接强度 可以有向 有点慢 但是结果要好一些
community_spinglass=g.community_spinglass(weights=g.es['weight'],spins=25,parupdate=False,start_temp=1,stop_temp=0.01,cool_fact=0.99,update_rule="config",gamma=1,implementation="orig")
Q=ig.GraphBase.modularity(g,community_spinglass._membership)
print('community_spinglass:')
print(Q)

# community_optimal_modularity() 这个会炸 这里被解释为连接强度
'''
'''
g=g_s
# 构建层次图
match_list=[]
structure_map=[]
with open("..\\Data\\Dataset_Structure.csv", "r") as f2:
    reader = csv.reader(f2)
    Structure = list(reader)
    f2.close()
    for x in Structure:
        t=[];
        match_list.append(x[2])
        temp=x[1].split('/')
        del temp[0]
        del temp[-1]
        for k in temp:
            t.append(k)
        structure_map.append(t)

with open(".\Jupyter\\test.csv", "r") as f2:
    reader = csv.reader(f2)
    data_temp = list(reader)
    f2.close()
temp=[]
for x in data_temp:
    temp.append(x[2])

temp_size=[]
# size 
for x in g.hub_score():
    if x<0.1:
        temp_size.append(6)
    else:
        temp_size.append(x*60)
g.vs['size']=temp_size

for k in range(len(g.vs['label'])-1,-1,-1):
    t=g.vs['label'][k].split('_')[0]
    if t not in temp:
        g.delete_vertices(k)

color_list=['#B15646','#E0D2A3','#A6BACC','#6F7F66','#038C7F','#F0E68C','#FF4500','#90EE90','#FFC0CB','#BA55D3']
color_temp=[]
for k in range(0,len(g.vs['label'])):
    t=g.vs['label'][k].split('_')[0]
    color_temp.append(color_list[int(data_temp[temp.index(t)][1])])
g.vs['color']=color_temp

# 删除所有阈值小于的边
for i in range(len(g.es['weight'])-1,-1,-1):
    if g.es['weight'][i]<1:
        g.delete_edges(i)


# 删除孤立点
t=g.degree()
for k in range(len(t)-1,-1,-1):
    if t[k]==0:
        g.delete_vertices(k)
ig.summary(g)
### 从聚类的结果中
# 映射到 Thalamus 549, Hypothalamus 1097, Cerebral cortex 688,Cerebellar cortex 528 and Hippocampal 1089，Midbrain 313
# node_community=[]
# for x in c:
#     temp=[]
#     for j in x:
#         temp.append(g.vs['label'][j])
#     node_community.append(temp)

high_region=[['TH','549'],['HY','1097'],['CTX','688'],['CBX','528'],['HPF','1089'],['MB','313']]
for i in range(0,len(node_community)):
    print(i)
    for j in range(0,len(node_community[i])):
        temp=node_community[i][j].split('_')[0]
        if temp not in match_list:
            print(temp+' '+str(i)+' '+str(j))
        else:
            t=structure_map[match_list.index(temp)]
            for k in high_region:
                if k[1] in t:
                    node_community[i][j]=k[0]
                    break

# 统计community中区域数量
community_count=[]
for x in node_community:
    temp=[]
    for k in high_region:
        temp.append(x.count(k[0]))
    community_count.append(temp)
'''

# 保存网络格式
# g=ig.load('igraph_map',format="edges")
# ig.write(g,'igraph_map',format="gml")
