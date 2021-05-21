import csv
import numpy as np
import BasicFunction as BF

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

relation_matrix=np.load('.\Save_Data\connection_matrix.npy')

region_list.sort()
projection_list.sort()
## igraph 画图
import igraph as ig
g = ig.Graph(directed=True)
node_list=[]
edge_width=[]
edge_list=[]
edge_weight=[]


for i in range(0,len(region_list)):
    for j in range(0,len(projection_list)):
        if float(relation_matrix[i,j])>0:
            if region_list[i] not in node_list:
                node_list.append(region_list[i])
            if projection_list[j] not in node_list:
                node_list.append(projection_list[j])
                
            edge_list.append((region_list[i],projection_list[j]))
            edge_weight.append(relation_matrix[i,j])
            edge_width.append(relation_matrix[i,j]*10)

#node_list.append('empty point_up')
#node_list.append('empty point_down')
g.add_vertices(node_list)
g.add_edges(edge_list)

'''
g.es['weight']=edge_weight
g.es['width']=edge_width

g.vs['label'] = node_list


### 可视化 ###
# 简化图像 删除只有出度和入度的节点
t1=g.indegree()
t2=g.outdegree()
for k in range(len(t1)-1,-1,-1):
    if t1[k]==0 or t2[k]==0:
        g.delete_vertices(k)

# 计算 hub score作为节点大小
import matplotlib.pyplot as plt
hub_score=g.hub_score()
size_temp=[]
for x in range(0,len(hub_score)):
    if hub_score[x] < 0.2:
        size_temp.append(14)
    else:
        size_temp.append(np.floor(hub_score[x]*70))
        if hub_score[x]>0.7:
            print(node_list[x])
g.vs['size']=size_temp
# 计算聚类结果作为颜色和类别
clu_result=g.clusters()
temp_color={}  
for x in list(set(clu_result.membership)):
    if x not in temp_color.keys():
        temp_color[x]=BF.randomcolor()
color_list=[]
for x in clu_result.membership:
    color_list.append(temp_color[x])
g.vs['color'] = color_list
g.vs['class'] = clu_result.membership
g.get_edgelist()
ig.summary(g)
value=g.clossness()
# node 信息
node=[]
for i in range(0,len(g.vs['label'])):
    node.append([str(i),g.vs['label'][i],g.vs['size'][i],value[i],g.vs['class'][i]])
# edge 信息
edge=g.get_edgelist()
'''


### 网络分析 ###
import matplotlib.pyplot as plt
import random

## degree distribution compare
degree_result=[[],[],[],[]]
degree_dis=g.degree_distribution()
x=np.array(range(int(degree_dis._min)+1,int(degree_dis._max)+1))
y=[]
for t in degree_dis._bins:
    y.append(t+1)
for i in range(0,len(y)):
    degree_result[0].append([x[i],y[i]])
    
## ER random
g_er=ig.GraphBase.Erdos_Renyi(len(node_list),m=len(edge_list),directed=True,loops=True)
degree_list_er=g_er.degree()
dd=plt.hist(degree_list_er,bins=max(degree_list_er)-min(degree_list_er))
for i in range(0,len(dd[0])):
    degree_result[1].append([dd[0][i]+1,dd[1][i]+1])

# small-world
g_ws=ig.GraphBase.Watts_Strogatz(1, len(node_list), 33, 0.1, loops=True)
while g_ws.ecount() > g.ecount():
    k=random.randrange(0,g_ws.ecount()-1)
    temp=g_ws
    temp.delete_edges(k)
    if not temp.is_connected():
        continue
    else:
        g_ws.delete_edges(k)
degree_list_ws=g_ws.degree()
dd=plt.hist(degree_list_ws,bins=max(degree_list_ws)-min(degree_list_ws))
for i in range(0,len(dd[0])):
    degree_result[2].append([dd[0][i]+1,dd[1][i]+1])

# scale-free
g_ba=ig.GraphBase.Barabasi(n=len(node_list),m=34,directed=True)
while g_ba.ecount() > g.ecount():
    k=random.randrange(0,g_ba.ecount()-1)
    temp=g_ba
    temp.delete_edges(k)
    if not temp.is_connected():
        continue
    else:
        g_ba.delete_edges(k)
degree_list_ba=g_ba.degree()
dd=plt.hist(degree_list_ba,bins=max(degree_list_ba)-min(degree_list_ba))
for i in range(0,len(dd[0])):
    degree_result[3].append([dd[0][i]+1,dd[1][i]+1])
plt.close()


graph_analysis=[]
graph_analysis.append([g.diameter(),g.radius(),g.average_path_length(),g.transitivity_undirected(),g.transitivity_avglocal_undirected(),g.density(loops=True),g.assortativity_degree()])
graph_analysis.append([g_er.diameter(),g_er.radius(),g_er.average_path_length(),g_er.transitivity_undirected(),g_er.transitivity_avglocal_undirected(),g_er.density(loops=True),g_er.assortativity_degree()])
graph_analysis.append([g_ws.diameter(),g_ws.radius(),g_ws.average_path_length(),g_ws.transitivity_undirected(),g_ws.transitivity_avglocal_undirected(),g_ws.density(loops=True),g_ws.assortativity_degree()])
graph_analysis.append([g_ba.diameter(),g_ba.radius(),g_ba.average_path_length(),g_ba.transitivity_undirected(),g_ba.transitivity_avglocal_undirected(),g_ba.density(),g_ba.assortativity_degree()])

### 信息传递比较（有向图）
## Triad census distribution
triad_censu=[[],[],[],[]]
for x in g.triad_census():
    triad_censu[0].append(int(x)+1)
for x in g_er.triad_census():
    triad_censu[1].append(int(x)+1)
for x in g_ws.triad_census():
    triad_censu[2].append(int(x)+1)
for x in g_ba.triad_census():
    triad_censu[3].append(int(x)+1)
