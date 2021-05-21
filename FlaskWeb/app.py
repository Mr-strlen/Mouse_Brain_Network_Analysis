from flask import Flask, render_template, redirect, request, session, abort, flash
from flask_sqlalchemy import SQLAlchemy
import csv, os, random, math
import numpy as np
import json
import BasicFunctionFlask as BF

from Config import app_init, SomaBasicInfo, CellTypeInfo
app, db = app_init()
filepath_l = os.path.split(os.path.realpath(__file__))[0] #当前文件路径

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
        temp = {"name": realname}
    else:
        temp = {"name": realname, "children" : kk}
    return temp

### --- 0. 基础部分 ---
# 0.0 初始页
@app.route('/')
def Initation():
    return render_template("index.html")
@app.route('/index')
def Index():
    return render_template("index.html")

## 0.1 欢迎页面
@app.route('/welcome')
def Welcome():
    return render_template("welcome.html")


### --- 1. 神经元数据展示 ---
## 1.1 单细胞形态数据主页面
@app.route('/neruon_list')
def NeruonList():
    offset = request.args.get('offset', 0, int)
    limit = request.args.get('limit', 20, int)
    temp = db.session.query(SomaBasicInfo).order_by(SomaBasicInfo.Neuron_Id).limit(limit).offset(offset).all()
    count = len(db.session.query(SomaBasicInfo).all())
    return render_template("neruon_list.html", page_data=temp, offset=offset, limit=limit, count=count)

# 1.1.1 绘画单个神经元细胞形态
@app.route('/single_neuron_shape/<id>')
def SingleNeuronShape(id):
    data=[]
    filename=str(id)+'_downsample.csv'
    path = filepath_l.replace('FlaskWeb', 'Out_Downsample')
    with open(path + filename) as file_object:
        reader = csv.reader(file_object)
        contents = list(reader)
    draw_mark = np.zeros([len(contents), 1])
    # 寻找叶子结点
    for n in contents:
        if n[10] == '0':
            data_temp = []
            t1 = n
            while True:
                if draw_mark[int(t1[0]) - 1] == 1:
                    data_temp.append([float(t1[2]), float(t1[3]), float(t1[4])])
                    break;
                data_temp.append([float(t1[2]), float(t1[3]), float(t1[4])])
                draw_mark[int(t1[0]) - 1] = 1
                if t1[6] == '-1':
                    break
                t1 = contents[int(t1[6]) - 1]
            data.append(data_temp)
    return render_template("single_neuron_shape.html",data_r=data,length=len(data))
# 1.1.2 单个神经元数据统计
@app.route('/single_stat/<id>')
def SingleStat(id):
    ## axon dendrite长度 在不同区域的长度 柱状图 Reco_Dataset_Cell.csv 文件中
    neuron_id = str(id)
    filepath = filepath_l.replace('FlaskWeb', 'Data')
    with open(filepath+"\\Reco_Dataset_Cell.csv", "r") as f:
        reader = csv.reader(f)
        statistics = np.array(list(reader))
    temp = np.where(statistics[:, 5] == neuron_id)[0]
    temp = statistics[temp, :]
    temp = temp[np.argsort(-temp[:,3].astype(np.float64))]
    # print(list(temp[:,1]),list(temp[:,3]),list(temp[:,4]))
    region_name = []
    for i in range(0, len(temp)):
        region_name.append(temp[i, 1] + '_' + temp[i, 2][0:3])
    return render_template("single_stat.html", regions=BF.getregionname(region_name[0:10],'side1'), axon_length=list(np.around(temp[0:10,3].astype(np.float64), 2)), dendrite_length=list(np.around(temp[0:10,4].astype(np.float64), 2)))

# 1.1.3 单个神经元映射结构展示
@app.route('/single_tree_structure/<id>')
def SingleTreeStructure(id):
    neuron_id = id
    filepath = filepath_l.replace('FlaskWeb', 'Data')
    ## 径向树状图
    article_info = {}
    data = json.loads(json.dumps(article_info))
    with open(filepath+"\\Reco_Dataset_Path.csv", "r") as f:
        reader = csv.reader(f)
        path = np.array(list(reader))
    with open(filepath+"\\Reco_Dataset_PathLength.csv", "r") as f:
        reader = f.readlines()
        print(len(reader))
        f.close()
        length = []
        for x in reader:
            temp=x.split('\n')[0]
            temp=temp.split(',')
            length.append(temp)

    t = np.where(path[:, 1] == neuron_id)[0]
    neuron_path = path[t, 0]
    neuron_length = []
    for i in range(0,len(path)):
        if path[i][-1] == neuron_id:
            neuron_length.append(length[i][0:-1])
    data_temp = {}
    # 构建树结构
    threshold = 1000
    path_list = []
    for i in range(0, len(neuron_path)):
        # 删除总长度不到threshold的投射分支
        if np.sum(np.array(neuron_length[i]).astype(float)) > threshold:
            temp = neuron_path[i].split('<-')
            temp.reverse()
            path_list.append(temp)
    res = path_gen(0, path_list[0][0], path_list)
    article = json.dumps(res, ensure_ascii=False)
    # print(article)
    #f = open('new_json.json', 'w')
    #f.write(article)
    #f.close()

    return render_template("single_tree_structure.html", tree_json=article)

## 1.2 中尺度统计数据展示 这里直接导向 http://connectivity.brain-map.org/


### --- 2. 对整体数据的统计分析 ---
## 2.1 单细胞形态数据的统计 各种echarts在一张图上
@app.route('/celldata_stat')
def CellDataStat():
    class Result:
        def __init__(self):
            self.name = ''
            self.axon_length = 0
            self.dendrite_length = 0
            self.soma_num = 0
            self.target = ''
            self.source = ''

    filepath=filepath_l.replace('FlaskWeb', 'Data')
    with open(filepath+"\\Reco_Dataset_Cell.csv", "r") as f:
        reader = csv.reader(f)
        Data = np.array(list(reader))
        f.close()
    result = Result()
    result.name = 'Total'
    # soma数量 axon总长度 dendrite总长度
    temp = Data
    result.axon_length = np.sum(temp[:, 3].astype(np.float64))
    result.dendrite_length = np.sum(temp[:, 4].astype(np.float64))
    result.soma_num = len(set(temp[:, 5]))

    # axon dendrite 投射前九个区域（两个饼图）
    projection_list = []
    for x in Data:
        if x[1] + '_' + x[2][0:3] not in projection_list:
            projection_list.append(x[1] + '_' + x[2][0:3])
    projetion_length = np.zeros([len(projection_list), 2])

    for x in temp:
        t = projection_list.index(x[1] + '_' + x[2][0:3])
        projetion_length[t,0] = projetion_length[t,0] + x[3].astype(np.float64)
        projetion_length[t,1] = projetion_length[t,1] + x[4].astype(np.float64)

    # 前十的名称和对应长度
    projection_name = BF.getregionname(projection_list, 'side1')
    temp = np.c_[projetion_length, np.array(projection_name)]
    axon_rank = temp[np.argsort(-projetion_length[:,0]),:]
    dendrite_rank = temp[np.argsort(-projetion_length[:,1]),:]

    if axon_rank[0,2] == result.name + '_Ips':
        result.target = axon_rank[1,2]
    else:
        result.target = axon_rank[0,2]
    result.source = dendrite_rank[0,2]

    sector_graph = []
    for i in range(0,19):
        sector_graph.append([np.floor(axon_rank[i, 0].astype(np.float64)), str(axon_rank[i, 2]),
                             np.floor(dendrite_rank[i, 0].astype(np.float64)), str(dendrite_rank[i, 2])])
    sector_graph.append([np.floor(result.axon_length - np.sum(axon_rank[0:5, 0].astype(np.float64))), 'Others',
                         np.floor(result.axon_length - np.sum(dendrite_rank[0:5, 0].astype(np.float64))), 'Others'])
    axon_name = list(axon_rank[0:19,2])
    axon_name.append('Others')
    dendrite_name = list(dendrite_rank[0:19,2])
    dendrite_name.append('Others')
    return render_template("celldata_stat.html", result=result, sector_graph=sector_graph,  axon_name = axon_name,dendrite_name = dendrite_name)

## 2.2 所有数据的热力图，需要做筛选
@app.route('/celldata_heatmap')
def CellDataHeatmap():
    return render_template("celldata_heatmap.html")

## 2.3 列出所有的celltype信息，提供按钮，按照每个celltype 进行统计画热力图
@app.route('/celltype_list')
def CellTypeList():
    temp = db.session.query(CellTypeInfo).order_by(CellTypeInfo.Celltype_Name).all()
    return render_template("celltype_list.html", page_data=temp)

# 2.3.1 某个celltype的信息统计
@app.route('/celltype_stat/<id>')
def CelltypeStat(id):
    class Result:
        def __init__(self):
            self.name = ''
            self.axon_length = 0
            self.dendrite_length = 0
            self.soma_num = 0
            self.target = ''
            self.source = ''

    celltype=str(id)
    filepath=filepath_l.replace('FlaskWeb', 'Data')
    with open(filepath+"\\Reco_Dataset_Cell.csv", "r") as f:
        reader = csv.reader(f)
        Data = np.array(list(reader))
        f.close()
    result = Result()
    result.name = BF.getregionname([celltype], 1)[0]
    # soma数量 axon总长度 dendrite总长度
    temp = Data[np.where(Data[:, 0] == celltype)[0], :]
    result.axon_length = np.sum(temp[:, 3].astype(np.float64))
    result.dendrite_length = np.sum(temp[:, 4].astype(np.float64))
    result.soma_num = len(set(temp[:, 5]))

    # axon dendrite 投射前九个区域（两个饼图）
    projection_list = []
    for x in Data:
        if x[1] + '_' + x[2][0:3] not in projection_list:
            projection_list.append(x[1] + '_' + x[2][0:3])
    projetion_length = np.zeros([len(projection_list), 2])

    for x in temp:
        t = projection_list.index(x[1] + '_' + x[2][0:3])
        projetion_length[t,0] = projetion_length[t,0] + x[3].astype(np.float64)
        projetion_length[t,1] = projetion_length[t,1] + x[4].astype(np.float64)

    # 前十的名称和对应长度
    projection_name = BF.getregionname(projection_list, 'side1')
    temp = np.c_[projetion_length, np.array(projection_name)]
    axon_rank = temp[np.argsort(-projetion_length[:,0]),:]
    dendrite_rank = temp[np.argsort(-projetion_length[:,1]),:]

    if axon_rank[0,2] == result.name + '_Ips':
        result.target = axon_rank[1,2]
    else:
        result.target = axon_rank[0,2]
    result.source = dendrite_rank[0,2]

    sector_graph = []
    for i in range(0,9):
        sector_graph.append([np.floor(axon_rank[i, 0].astype(np.float64)), str(axon_rank[i, 2]),
                             np.floor(dendrite_rank[i, 0].astype(np.float64)), str(dendrite_rank[i, 2])])
    sector_graph.append([np.floor(result.axon_length - np.sum(axon_rank[0:5, 0].astype(np.float64))), 'Others',
                         np.floor(result.axon_length - np.sum(dendrite_rank[0:5, 0].astype(np.float64))), 'Others'])
    axon_name = list(axon_rank[0:9,2])
    axon_name.append('Others')
    dendrite_name = list(dendrite_rank[0:9,2])
    dendrite_name.append('Others')
    return render_template("celltype_stat.html", result=result, sector_graph=sector_graph,  axon_name = axon_name,dendrite_name = dendrite_name)

# 2.3.2 某个celltype的热力图
@app.route('/celltype_heatmap/<id>')
def CelltypeHeatmap(id):
    import numpy as np
    filepath=filepath_l.replace('FlaskWeb', 'Data')
    ### 推荐深度数据 ###
    with open(filepath+"\\Reco_Dataset_Cell.csv", "r") as f:
        reader = csv.reader(f)
        Data = np.array(list(reader))
        f.close()

    threshold = 100 / 25  # 有效连接阈值
    path = "..\\Other Information\\Soma_region_and_location.xls"
    area_data = BF.read_xlsx(path, 'Sheet1')
    del area_data[0]
    area_data = np.array(area_data)
    ### 94个区域的信息特征
    ## 删除Error_Data内的soma
    for filename in os.listdir('..\\Error_Data\\'):
        temp = filename.split('_cul')
        temp = temp[0]
        t = np.where(area_data[:, 0] == temp)
        area_data = np.delete(area_data, t, axis=0)

    ### 计算区域内的聚类情况，画出聚类后的热力图 ###
    a_t = BF.getregionname([str(id)],1)[0]  # 当前区域名称
    soma_list = []
    for x in area_data:
        if x[4] == a_t:
            soma_list.append(x[0].tolist())

    # 根据soma_list Data构建对应的投射序列
    projection_list = []
    for x in soma_list:
        t = np.where(Data[:, 5] == x)
        temp = Data[t, 1:3].tolist()
        temp = temp[0]
        for k in temp:
            projection_list.append(k[0] + '_' + k[1][0:3])
    projection_list = list(set(projection_list))

    # 构建二维矩阵
    heat_value = np.zeros((len(soma_list), len(projection_list)))
    for i in range(0, len(soma_list)):
        t = np.where(Data[:, 5] == soma_list[i])
        temp = Data[t, 1:3].tolist()
        t_value = Data[t, 3].astype(np.float64)
        t_value = t_value[0]
        temp = temp[0]
        for k in range(0, len(temp)):
            heat_value[i, projection_list.index(temp[k][0] + '_' + temp[k][1][0:3])] = t_value[k]

    # 阈值筛选
    for i in range(0, np.size(heat_value, 0)):
        for j in range(0, np.size(heat_value, 1)):
            if heat_value[i, j] != 0 and heat_value[i, j] < threshold:
                heat_value[i, j] = 0
    soma_label = []
    proj_label = []

    # 丢掉数量少的区域
    if len(soma_list) < 20:
        print('too less soma')
        print('too less soma')
        heat_map = heat_value
        t2 = []
        for i in range(0, np.size(heat_map, 1)):
            if np.sum(heat_map[:, i]) > np.shape(heat_map, 0):
                t2.append(i)
                proj_label.append(projection_list[i])
        heat_map = heat_map[:, tuple(t2)]
        # 取log
        for i in range(0, np.size(heat_map, 0)):
            for j in range(0, np.size(heat_map, 1)):
                heat_map[i, j] = np.log(heat_map[i, j] * 100 + 1)
        proj_label = BF.getregionname(proj_label, 'side1')
        soma_label = soma_list
        web_data = []
        for i in range(0, np.size(heat_map, 0)):
            for j in range(0, np.size(heat_map, 1)):
                web_data.append([j, i, heat_map[i, j]])
        return render_template("celltype_heatmap.html", web_data=web_data, soma_list=soma_label,
                               projection_list=proj_label)
    else:
        # 剔除数值小的行列 std
        mean_t = np.mean(np.sum(heat_value, axis=1))
        std_t = np.std(np.sum(heat_value, axis=1))
        t1 = []
        for i in range(0, np.size(heat_value, 0)):
            if np.sum(heat_value[i, :]) > (mean_t + 1 * std_t):
                t1.append(i)
                soma_label.append(soma_list[i])

        heat_map = heat_value[tuple(t1), :]
        t2 = []
        for i in range(0, np.size(heat_map, 1)):
            if np.sum(heat_map[:, i]) > len(t1):
                t2.append(i)
                proj_label.append(projection_list[i])
        heat_map = heat_map[:, tuple(t2)]

        # 取log
        for i in range(0, np.size(heat_map, 0)):
            for j in range(0, np.size(heat_map, 1)):
                heat_map[i, j] = np.log(heat_map[i, j] * 100 + 1)
        proj_label = BF.getregionname(proj_label, 'side1')

        import scipy.cluster.hierarchy as sch
        from scipy.cluster.vq import vq, kmeans, whiten
        import numpy as np

        data1 = heat_map
        data2 = heat_map.T
        # 1. 层次聚类
        # 生成点与点之间的距离矩阵,这里用的欧氏距离:
        disMat = sch.distance.pdist(data1, 'euclidean')
        # 进行层次聚类:
        Z = sch.linkage(disMat, method='average')
        # 根据linkage matrix Z得到聚类结果:
        cluster = sch.fcluster(Z, t=1, criterion='inconsistent')
        # 2. k-means聚类
        # 将原始数据做归一化处理
        data = whiten(data1)
        centroid = kmeans(data, max(cluster))[0]
        label_row = vq(data, centroid)[0]

        disMat = sch.distance.pdist(data2, 'euclidean')
        Z = sch.linkage(disMat, method='average')
        cluster = sch.fcluster(Z, t=1, criterion='inconsistent')
        data = whiten(data2)
        centroid = kmeans(data, max(cluster))[0]
        label_col = vq(data, centroid)[0]

        # 排序
        t1 = np.argsort(label_col[:])
        t2 = np.argsort(label_row[:])
        heat_map = heat_map[:, t1]
        heat_map = heat_map[t2, :]

        temp = []
        for x in t1:
            temp.append(proj_label[x])
        proj_label = temp

        temp = []
        for x in t2:
            temp.append(soma_label[x])
        soma_label = temp
        label_col = label_col[t1]
        label_row = label_row[t2]
        web_data=[]
        for i in range(0, np.size(heat_map, 0)):
            for j in range(0, np.size(heat_map, 1)):
                web_data.append([j,i,heat_map[i,j]])


        return render_template("celltype_heatmap.html",web_data=web_data,soma_list=soma_label,projection_list=proj_label)

### --- 3. 脑网络的展示和分析 ---
## 3.1 画出整体的脑连接图，并在每个节点上显示一些网络特性
@app.route('/brain_connection_map')
def BrainConnectionMap():
    filepath = filepath_l.replace('FlaskWeb', 'Data')
    ## 读取Reco_Dataset_Cell得到映射矩阵
    with open(filepath+"\\Reco_Dataset_Cell.csv", "r") as f:
        reader = csv.reader(f)
        data = np.array(list(reader))
    region_list = []
    projection_list = []
    for i in data:
        region_list.append(str(i[0]))
        projection_list.append(str(i[1]) + '_' + str(i[2]))
    region_list = list(set(region_list))
    projection_list = list(set(projection_list))

    projection_list1 = BF.getregionname(projection_list, 'side1')
    region_list1 = BF.getregionname(region_list, 1)
    ## 构建反转矩阵
    region_list2 = []
    projection_list2 = []
    for i in range(0, len(region_list1)):
        region_list2.append(region_list1[i] + '_Con')
        region_list1[i] = region_list1[i] + '_Ips'
    for x in projection_list1:
        if 'Con' in x:
            projection_list2.append(x.replace('Con', 'Ips'))
        else:
            projection_list2.append(x.replace('Ips', 'Con'))
    region_list = region_list1 + region_list2  # soma区域列表
    projection_list = list(set(projection_list1 + projection_list2))  # 投射区域列表
    filepath = filepath_l.replace('FlaskWeb', 'Python_Code')
    relation_matrix = np.load(filepath+'\\Save_Data\\connection_matrix.npy')
    region_list.sort()
    projection_list.sort()
    ## igraph 画图
    import igraph as ig
    g = ig.Graph(directed=True)
    node_list = []
    edge_width = []
    edge_list = []
    edge_weight = []

    for i in range(0, len(region_list)):
        for j in range(0, len(projection_list)):
            if float(relation_matrix[i, j]) > 0.7:
                if region_list[i] not in node_list:
                    node_list.append(region_list[i])
                if projection_list[j] not in node_list:
                    node_list.append(projection_list[j])
                edge_list.append((region_list[i], projection_list[j]))
                edge_weight.append(relation_matrix[i, j])
                edge_width.append(relation_matrix[i, j] * 10)

    g.add_vertices(node_list)
    g.add_edges(edge_list)

    g.es['weight'] = edge_weight
    g.es['width'] = edge_width
    g.vs['label'] = node_list

    # 简化图像 删除只有出度和入度的节点
    t1 = g.indegree()
    t2 = g.outdegree()
    for k in range(len(t1) - 1, -1, -1):
        if t1[k] == 0 or t2[k] == 0:
            g.delete_vertices(k)

    # 计算 hub score作为节点大小
    import matplotlib.pyplot as plt
    hub_score = g.hub_score()
    size_temp = []
    for x in range(0, len(hub_score)):
        if hub_score[x] < 0.1:
            size_temp.append(10)
        else:
            size_temp.append(np.floor(hub_score[x] * 100))
            if hub_score[x] > 0.7:
                print(node_list[x])
    g.vs['size'] = size_temp
    # 计算聚类结果作为颜色和类别
    clu_result = g.clusters()
    temp_color = {}
    for x in list(set(clu_result.membership)):
        if x not in temp_color.keys():
            temp_color[x] = BF.randomcolor()
    color_list = []
    for x in clu_result.membership:
        color_list.append(temp_color[x])
    g.vs['color'] = color_list
    g.vs['class'] = clu_result.membership
    g.get_edgelist()
    value = g.betweenness()
    # node 信息
    nodes = []
    for i in range(0, len(g.vs['label'])):
        nodes.append([str(i), g.vs['label'][i], g.vs['size'][i], value[i], g.vs['class'][i]])
    # edge 信息
    edges = g.get_edgelist()

    return render_template("brain_connection_map.html",nodes=nodes,edges=edges,classnum=np.max(clu_result.membership))

## 3.2 网络分析 画出脑网络的部分分布图（和随机网络对比）
@app.route('/brain_graph_analysis')
def BrainGraphAnalysis():
    filepath = filepath_l.replace('FlaskWeb', 'Data')
    ## 读取Reco_Dataset_Cell得到映射矩阵
    with open(filepath + "\\Reco_Dataset_Cell.csv", "r") as f:
        reader = csv.reader(f)
        data = np.array(list(reader))
    region_list = []
    projection_list = []
    for i in data:
        region_list.append(str(i[0]))
        projection_list.append(str(i[1]) + '_' + str(i[2]))
    region_list = list(set(region_list))
    projection_list = list(set(projection_list))

    projection_list1 = BF.getregionname(projection_list, 'side1')
    region_list1 = BF.getregionname(region_list, 1)
    ## 构建反转矩阵
    region_list2 = []
    projection_list2 = []
    for i in range(0, len(region_list1)):
        region_list2.append(region_list1[i] + '_Con')
        region_list1[i] = region_list1[i] + '_Ips'
    for x in projection_list1:
        if 'Con' in x:
            projection_list2.append(x.replace('Con', 'Ips'))
        else:
            projection_list2.append(x.replace('Ips', 'Con'))
    region_list = region_list1 + region_list2  # soma区域列表
    projection_list = list(set(projection_list1 + projection_list2))  # 投射区域列表
    filepath = filepath_l.replace('FlaskWeb', 'Python_Code')
    relation_matrix = np.load(filepath + '\\Save_Data\\connection_matrix.npy')
    region_list.sort()
    projection_list.sort()
    ## igraph 画图
    import igraph as ig
    g = ig.Graph(directed=True)
    node_list = []
    edge_list = []

    for i in range(0, len(region_list)):
        for j in range(0, len(projection_list)):
            if float(relation_matrix[i, j]) > 0.7:
                if region_list[i] not in node_list:
                    node_list.append(region_list[i])
                if projection_list[j] not in node_list:
                    node_list.append(projection_list[j])
                edge_list.append((region_list[i], projection_list[j]))
    g.add_vertices(node_list)
    g.add_edges(edge_list)

    ### 网络分析 ###
    import matplotlib.pyplot as plt
    import random

    ## degree distribution compare
    degree_result = [[], [], [], []]
    degree_dis = g.degree_distribution()
    x = np.array(range(int(degree_dis._min) + 1, int(degree_dis._max) + 1))
    y = []
    for t in degree_dis._bins:
        y.append(t + 1)
    for i in range(0, len(y)):
        degree_result[0].append([x[i], y[i]])

    ## ER random
    g_er = ig.GraphBase.Erdos_Renyi(len(node_list), m=len(edge_list), directed=True, loops=True)
    degree_list_er = g_er.degree()
    dd = plt.hist(degree_list_er, bins=max(degree_list_er) - min(degree_list_er))
    for i in range(0, len(dd[0])):
        degree_result[1].append([dd[0][i] + 1, dd[1][i] + 1])

    # small-world
    g_ws = ig.GraphBase.Watts_Strogatz(1, len(node_list), 33, 0.1, loops=True)
    while g_ws.ecount() > g.ecount():
        k = random.randrange(0, g_ws.ecount() - 1)
        temp = g_ws
        temp.delete_edges(k)
        if not temp.is_connected():
            continue
        else:
            g_ws.delete_edges(k)
    degree_list_ws = g_ws.degree()
    dd = plt.hist(degree_list_ws, bins=max(degree_list_ws) - min(degree_list_ws))
    for i in range(0, len(dd[0])):
        degree_result[2].append([dd[0][i] + 1, dd[1][i] + 1])

    # scale-free
    g_ba = ig.GraphBase.Barabasi(n=len(node_list), m=34, directed=True)
    while g_ba.ecount() > g.ecount():
        k = random.randrange(0, g_ba.ecount() - 1)
        temp = g_ba
        temp.delete_edges(k)
        if not temp.is_connected():
            continue
        else:
            g_ba.delete_edges(k)
    degree_list_ba = g_ba.degree()
    dd = plt.hist(degree_list_ba, bins=max(degree_list_ba) - min(degree_list_ba))
    for i in range(0, len(dd[0])):
        degree_result[3].append([dd[0][i] + 1, dd[1][i] + 1])
    plt.close()

    graph_analysis = []
    graph_analysis.append([g.diameter(), g.radius(), format(g.average_path_length(), '.6f'), format(g.transitivity_undirected(),'.6f'),
                           format(g.transitivity_avglocal_undirected(), '.6f'), format(g.density(loops=True), '.6f'), format(g.assortativity_degree(), '.6f')])
    graph_analysis.append([g_er.diameter(), g_er.radius(), format(g_er.average_path_length(), '.6f'), format(g_er.transitivity_undirected(),'.6f'),
                           format(g_er.transitivity_avglocal_undirected(), '.6f'), format(g_er.density(loops=True), '.6f'), format(g_er.assortativity_degree(), '.6f')])
    graph_analysis.append([g_ws.diameter(), g_ws.radius(), format(g_ws.average_path_length(), '.6f'), format(g_ws.transitivity_undirected(),'.6f'),
                           format(g_ws.transitivity_avglocal_undirected(), '.6f'), format(g_ws.density(loops=True), '.6f'), format(g_ws.assortativity_degree(), '.6f')])
    graph_analysis.append([g_ba.diameter(), g_ba.radius(), format(g_ba.average_path_length(), '.6f'), format(g_ba.transitivity_undirected(),'.6f'),
                           format(g_ba.transitivity_avglocal_undirected(), '.6f'), format(g_ba.density(), '.6f'), format(g_ba.assortativity_degree(), '.6f')])

    ## Triad census distribution
    triad_censu = [[], [], [], []]
    for x in g.triad_census():
        triad_censu[0].append(int(x) + 1)
    for x in g_er.triad_census():
        triad_censu[1].append(int(x) + 1)
    for x in g_ws.triad_census():
        triad_censu[2].append(int(x) + 1)
    for x in g_ba.triad_census():
        triad_censu[3].append(int(x) + 1)
    return render_template("brain_graph_analysis.html", graph_analysis=graph_analysis, degree_result=degree_result, triad_censu=triad_censu)

## 3.3 模拟仿真
# (弃) 直接画图显示在网页中
@app.route("/brain_simulation")
def NeuronShapeWasted():
    import matplotlib
    matplotlib.use('Agg')  # 不出现画图的框
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import axes3d
    from io import BytesIO
    import base64

    ## 单个细胞不同颜色
    fig = plt.figure()
    point = [[], [], []]
    ax = fig.gca(projection='3d')
    path = filepath_l.replace('FlaskWeb', 'Out_Downsample')
    for root, dirs, files in os.walk(path, topdown=True):
        # files=files[2:3]
        # print("文件◎",os.path.join(root,name))
        for name in files:
            with open(os.path.join(root, name)) as file_object:
                reader = csv.reader(file_object)
                contents = list(reader)
                file_object.close()
                id_set = []
                # 建立颜色区域dic
                for t1 in contents:
                    id_set.append(t1[7])
                id_set = list(set(id_set))
                color_dic = dict()
                for x in id_set:
                    color_dic[x] = BF.randomcolor()

                # 整体图像
                for t1 in contents:
                    del t1[9:11]
                    t1 = list(map(float, t1))
                    if int(t1[6]) != -1:
                        t2 = contents[int(t1[6]) - 1]
                        del t2[9:11]
                        color_id = t2[7]
                        t2 = list(map(float, t2))
                        x = [t1[2], t2[2]]
                        y = [t1[3], t2[3]]
                        z = [t1[4], t2[4]]
                        ax.plot(x, y, z, color_dic[color_id])

    # 转成图片的步骤
    sio = BytesIO()
    plt.savefig(sio, format='png')
    data = base64.encodebytes(sio.getvalue()).decode()
    print(data)
    html = '''
       <html>
           <body>
               <img src="data:image/png;base64,{}" />
           </body>
        <html>
    '''
    plt.close()
    # 记得关闭，不然画出来的图是重复的
    return html.format(data)
    #format的作用是将data填入{}

### --- 4. 细胞类型在网络分析上的统计 基本和之前的数据统计类似---
## 4.1 一样的，展示所有celltype
@app.route('/celltype_list_network')
def CellTypeListNetwork():
    return render_template("celltype_list_network.html")

#4.1.1 某个celltype的motif拆分
@app.route('/celltype_motif_network')
def CellTypeMotifNetwork():
    return render_template("celltype_motif_network.html")
# 4.1.2 某个celltype的网络形状
@app.route('/celltype_map_network')
def CellTypeMapNetwork():
    return render_template("celltype_map_network.html")

# 4.1.3 某个celltype的仿真
@app.route('/celltype_simulation_network')
def CellTypeSimulationNetwork():
    return

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
