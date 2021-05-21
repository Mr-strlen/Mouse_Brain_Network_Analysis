# -*- coding: utf-8 -*- #设置中文注释
import igraph as ig
import cairo
import csv
import math
import numpy as np
import matplotlib.pyplot as plt
import random
# 构建匹配结构
pair_list=[]
structure_map=[]
with open("..\\Data\\Dataset_Structure.csv", "r") as f1:
    reader = csv.reader(f1)
    structure_info = list(reader)
    f1.close()
    for x in structure_info:
        pair_list.append(x[0])
        t=[]
        temp=x[1].split('/')
        del temp[0]
        del temp[-1]
        for k in temp:
            t.append(k)
        structure_map.append(t)

# 画图
g = ig.Graph(directed=True)
with open('..\\Data\\Data_Statistics.csv') as f:
    reader =csv.reader(f)
    count_info = np.array(list(reader))
    f.close()
pair_list=list(map(str,count_info[:,0]))

# 添加网络中的点 边
with open("..\\Heatmap_Data_cor_tha\\Heatmap_depth_8_cor_tha.csv") as f1:
    reader = csv.reader(f1)
    heatmap_info = list(reader)
    f1.close()
    point_list=[]
    edges=[]
    edge_color=[]
    edge_weight=[]
    for x in heatmap_info:
        if int(count_info[pair_list.index(x[0]),1])>20 and float(x[2])>40: #soma数量和axon长度筛选
            point_list.append(x[0])
            point_list.append(x[1])
            edges.append((x[0],x[1]))
            edge_weight.append(float(x[2]))
            if structure_map[pair_list.index(x[0])][3]=='688':
                edge_color.append('#FF4500')
            elif structure_map[pair_list.index(x[0])][4]=='549':
                edge_color.append('#16982B')

point_list=list(set(point_list))
g.add_vertices(point_list)


# 随机边
edges_random=np.array(edges)
for i in range(0,100):
    # 改入边
    t1=random.randint(0,len(edges)-1)
    t2=random.randint(0,len(edges)-1)
#    print([t1,t2])
    temp=edges_random[t1,1]
    edges_random[t1,1]=edges_random[t2,1]
    edges_random[t2,1]=temp
    # 改出边
    t1=random.randint(0,len(edges)-1)
    t2=random.randint(0,len(edges)-1)
#    print([t1,t2])
    temp=edges_random[t1,0]
    edges_random[t1,0]=edges_random[t2,0]
    edges_random[t2,0]=temp
    temp=edge_weight[t1]
    edge_weight[t1]=edge_weight[t2]
    edge_weight[t2]=temp
g.add_edges(edges_random) #随机边 

#g.add_edges(edges)

# 边属性
g.es['weight']=edge_weight
edge_width=[]
for i in edge_weight:
    edge_width.append(math.log(i,3))
g.es['width']=edge_width
g.es['color']=edge_color
g.es['arrow_size']=1.5


# 节点属性
label_name=[]
color_list=[]
        
for x in point_list:
    label_name.append(structure_info[pair_list.index(x)][-2])
    if structure_map[pair_list.index(x)][3]=='688':
        color_list.append('#FF7F50')
    elif structure_map[pair_list.index(x)][4]=='549':
        color_list.append('#808000')
g.vs['label'] = label_name
g.vs['color'] = color_list
g.vs['size']=55
g.vs['label_size']=25

# 获取每个点的坐标
Area_Center=np.load(file="Area_Center_right.npy")
'''
layout=g.layout("lgl")
out=ig.plot(g,layout=layout,bbox = (1500, 1500))
# out.save('..\\Start_Presentation\\Images\\Network.png')
#out.save('..\\Start_Presentation\\Images\\Random_Network.png')

# 图论分析
g_d=g.degree()
betweenness = g.betweenness()
g_d_in=g.indegree()
g_d_out=g.outdegree()
#plt.hist(g_d,bins=20)
plt.hist(betweenness,bins=78,range=[50,400])
#plt.show()
'''