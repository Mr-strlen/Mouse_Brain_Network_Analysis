import csv
# soma_region_id 和 soma_name 匹配信息
with open("..\\Data\\Dataset_Soma.csv", "r") as f1:
    reader = csv.reader(f1)
    Soma_Info = list(reader)
    f1.close()
    
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

#分支最大长度
for i in range(0,len(Structure)):
    maxlen=int(Structure[i][-1])
    for j in range(i,len(Structure)):
        if int(Structure[j][-1])>maxlen:
            if structure_map[i][-1]==structure_map[j][int(Structure[i][-1])-1]:
                maxlen=int(Structure[j][-1])
    Structure[i].append(maxlen)
    

with open("..\\Data\\Dataset_Cell.csv", "r") as f3:
    reader = csv.reader(f3)
    Cell_Map = list(reader)
    f3.close()

## 遍历所有depth下的热力图情况
for depth in range(5,12): # 层次信息
    # 从cortex到thalamus
    print(depth)
    depth_map=[]    
    pair_set=[]
    pair_set_soma_axon=[]
    pair_set_soma_dendrite=[]
    for x in Cell_Map:
        id_s=match_list.index(x[0])
        id_p=match_list.index(x[1])
        t1='-2'
        t2='-2'
        if int(Structure[id_s][-2])>=5 and int(Structure[id_p][-2])>=5:
            if depth<=int(Structure[id_s][-2]):
                if (structure_map[id_s][3]=='688' and structure_map[id_p][4]=='549') or (structure_map[id_p][3]=='688' and structure_map[id_s][4]=='549'):
                        t1=structure_map[id_s][depth-1]
            elif int(Structure[id_s][-2])==int(Structure[id_s][-1]) and depth>int(Structure[id_s][-2]): #叶子节点
                if (structure_map[id_s][3]=='688' and structure_map[id_p][4]=='549') or (structure_map[id_p][3]=='688' and structure_map[id_s][4]=='549'):
                    t1=structure_map[id_s][-1]
            if depth<=int(Structure[id_p][-2]):
                if (structure_map[id_s][3]=='688' and structure_map[id_p][4]=='549') or (structure_map[id_p][3]=='688' and structure_map[id_s][4]=='549'):
                    t2=structure_map[id_p][depth-1]
            elif int(Structure[id_p][-2])==int(Structure[id_p][-1]) and depth>int(Structure[id_p][-2]): #叶子节点
                if (structure_map[id_s][3]=='688' and structure_map[id_p][4]=='549') or (structure_map[id_p][3]=='688' and structure_map[id_s][4]=='549'):
                    t2=structure_map[id_p][-1] 
            if t1!='-2' and t2!='-2':
                depth_map.append([t1,t2,x[2],x[3]])
                pair_set.append(t1+"|"+t2)
                if x[2]!='0':
                    pair_set_soma_axon.append(t1+"|"+t2+"|"+x[-1]) #统计有多少个指向某个区域的神经元 axon
                if x[3]!='0':
                    pair_set_soma_dendrite.append(t1+"|"+t2+"|"+x[-1]) #统计有多少个指向某个区域的神经元 dendrite
    
    pair_map=[]
    # 根据层次叠加
    pair_set=list(set(pair_set))
    pair_set_soma_axon=list(set(pair_set_soma_axon))
    pair_set_soma_dendrite=list(set(pair_set_soma_dendrite))
    
    for x in pair_set:
        temp=x.split('|')
        t=[0,0]
        count=0
        for i in depth_map:
            if i[0]==temp[0] and i[1]==temp[1]:
                t[0]=t[0]+float(i[2])
                t[1]=t[1]+float(i[3])
        # 统计神经元个数
        count_axon=0
        count_dendrite=0
        for i in pair_set_soma_axon:
            temp_soma=i.split('|')
            if temp_soma[0]==temp[0] and temp_soma[1]==temp[1]:
                count_axon=count_axon+1
        for i in pair_set_soma_dendrite:
            temp_soma=i.split('|')
            if temp_soma[0]==temp[0] and temp_soma[1]==temp[1]:
                count_dendrite=count_dendrite+1
        if count_axon==0 and t[0]==0:
            count_axon=1
        elif  count_dendrite==0 and t[1]==0:
            count_dendrite=1
        pair_map.append([temp[0],temp[1],str(t[0]),str(t[1]),str(t[0]/count_axon),str(t[1]/count_dendrite)])

    with open('..\\Heatmap_Data_cor_tha\\Heatmap_depth_'+str(depth)+'_cor_tha.csv','w+',newline='') as f:
        csv_writer = csv.writer(f)
        for rows in pair_map:
            csv_writer.writerow(rows)
        f.close()

