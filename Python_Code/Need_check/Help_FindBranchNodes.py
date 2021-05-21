## 统计每个swc文件中的branch数量，生成branch数量统计文件
## Warning 这部分没有进行同侧异侧区分
import BasicFunction as BF
import os
import csv
import numpy as np
# 读取深度推荐列表
diskname=BF.get_disklist()
path=diskname+"\\Vaa3D\\Other Information\\Selected_Regions.xlsx"
#path="E:\\Vaa3D\\Other Information\\Soma_region_and_location.xlsx"
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

## 每个文件统计
empty=[]
path = diskname+'\\Vaa3D\\Data\\Dataset_All'
# path = 'E:\\Vaa3D\\Data\\1708_registered_model'
for root,dirs,files in os.walk(path,topdown=True):
    for name in files:
        # print(name)
        temp=name.split('.')
        ## 文件树状结构
        filedata=[]
        with open(os.path.join(root,name)) as file_object:
            contents = file_object.readlines()
#            print(len(contents))
            file_object.close()
            while contents[0][0]=='#':
                del contents[0] 
            for x in contents:
                t=x.split( )
                filedata.append(t)
        #  filedata 投射重复处理
        count=0
        while count!=len(filedata)-1:
            if filedata[count][0]==filedata[count][-1]:
                del filedata[count]
                print(name)
            else:
                count=count+1
        
        
        node_list=[]
        # 构建node_list
        for i in range(0,len(filedata)+1):
            node_list.append([i])
        for i in range(0,len(filedata)):
            if filedata[i][-1]=="-1":
                node_list[0].append(i+1)
            else:
                node_list[int(filedata[i][-1])].append(i+1)
        
        # 覆盖所有过度节点
        for i in range(0,len(node_list)):
            if len(node_list[i])<2:
                continue
            else:
                for j in range(1,len(node_list[i])):
                    nextnode=node_list[i][j]
                    while(len(node_list[nextnode])==2):
                        nextnode=node_list[nextnode][1]
                    node_list[i][j]=nextnode


        # 删除过渡节点
        count=1 #保留根节点
        while count!=len(node_list):
            if len(node_list[count])!=2:
                count=count+1
            else:
                del node_list[count]
        
        leaf_node=[] # 所有叶子节点 长度为1
        branch_node=[] # 所有branch节点 长度大于2
        branch_num=0 # branch的个数 branch节点分支个数的总和
        branch_num_node=[] # branch数量=leaf_node+branch_node
        for x in node_list:
            if len(x)==1:
                leaf_node.append(x[0])
                branch_num_node.append(x[0])
            elif len(x)>2:
                branch_node.append(x)
                branch_num=branch_num+len(x)-1
                branch_num_node.append(x[0])
                # if len(x)!=3 and 1 not in x: #输出三叉节点
                    # print(name)
        if branch_num_node[0]==1:
            del branch_num_node[0]
        
        
        ## 节点匹配区域
        if not os.path.exists("..\\Out\\"+temp[0]+"_cul.txt"):
            print(temp)
            continue
        with open("..\\Out\\"+temp[0]+"_cul.txt") as file_object:
            contents = file_object.readlines()
            file_object.close()
            filedata=[]
            while contents[0][0]=='#':
                del contents[0]

        # 统计匹配组
        id_list=[]
        for x in branch_num_node:
            t=contents[x-1]
            t1=t.split( )
            # 修改区域id
            area_id=match_list.index(t1[-2])
            for k in area_list:
                if int(k[1])>int(Structure[area_id][-1]):
                    continue
                if structure_map[area_id][int(k[1])-1]==k[0]:
                    t1[-2]=str(k[0])
                    break
            id_list.append(int(t1[-2]))
        id_set=list(set(id_list))
        t1=contents[0].split( )
        for x in id_set:
            empty.append([t1[-2],x,str(id_list.count(x)),temp[0]])


## 保存文件
with open("..\\Data\\Reco_Dataset_Branchnum.csv","w+",newline='') as f:
    csv_writer = csv.writer(f)
    for rows in empty:
        csv_writer.writerow(rows)
    f.close()








