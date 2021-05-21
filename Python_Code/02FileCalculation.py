# 读取Tif文件并做匹配，计算import os
import math
import BasicFunction as BF
import os
import SimpleITK as sitk
import numpy as np
import csv

diskname=BF.get_disklist()
img = sitk.ReadImage('..\\Other Information\\annotation_25.nrrd')
#padding
imarray=np.zeros([457,321,529])
imarray[0:456,0:320,0:528]=sitk.GetArrayViewFromImage(img)

'''
# 比较tif文件和nrrd文件，存在不少差异，其中tif中的部分数值在csv文件中找不到对应编号，所以是存在问题的。
import numpy as np
from libtiff import TIFFfile
tif = TIFFfile(diskname+'\\Vaa3D\\Other Information\\annotation_25_gu.tif')
samples, _ = tif.get_samples()
samples=samples[0]

pair_dic=dict()
size=np.shape(imarray)
for i in range(0,size[0]):
    for j in range(0,size[1]):
        for k in range(0,size[2]):
            if samples[i][j][k]!=imarray[i][j][k]:
                #print([i,j,k])
                pair_dic[samples[i][j][k]]=imarray[i][j][k]
'''

'''
# pair dicOutput
{312782620.0: 312782632, 312782660.0: 312782640, 484682530.0: 484682520, 312782600.0: 312782578, 
 484682500.0: 484682512, 484682460.0: 484682470, 182305700.0: 182305693, 589508400.0: 589508447, 
 182305710.0: 182305705, 312782560.0: 312782550, 496345660.0: 496345668, 563807400.0: 563807439, 
 560581570.0: 560581563, 589508500.0: 589508451, 549009200.0: 549009227, 526157200.0: 526157192, 
 526322270.0: 526322264, 527697000.0: 527696977, 576073700.0: 576073704, 606826600.0: 606826647, 
 614454300.0: 614454277, 607344830.0: 607344846, 606826700.0: 606826663, 599626940.0: 599626927}
'''

# path = "..\\Test_Data"
#path = diskname+'\\Vaa3D\\Data\\1708_registered_model'
path = diskname+'\\Vaa3D\\Data\\Dataset_All'
#maxlen=0
def filecalculation(root,name):
    empty=[]
    with open(os.path.join(root,name)) as file_object:
        contents = file_object.readlines()
        print(len(contents))
        file_object.close()
        t=name.split('.')
#        if len(contents)>maxlist:
#                maxlist=len(contents)
        while contents[0][0]=='#':# 删除注释
            del contents[0]
        node_list=[]
        for i in range(0,len(contents)):
            node_list.append(0)
        for lineid in range(0,len(contents)):
            x=contents[lineid]
            x=x.strip("\n")
            t1=x.split( )
            t1=list(map(float,t1))
            if t1[0]==t1[-1]: #修正版本的数据会出现自己导向自己的情况，得处理这个问题
                print('Circle Warning!!! '+ t[0])
                continue
            '''
            超过边界数据标记为-1
            没有超过边界，但是区域在矫正之后依然为0的，是匹配到了空区域
            
            叶子节点为0 分支节点>1 过渡节点为1
            '''
            #部分超过边界的值
            if math.floor(t1[2])>527 or math.floor(t1[4])>455 or math.floor(t1[3])>319:
                areaid=-1
                t2=contents[int(t1[-1])-1].split( )
                t2=list(map(float,t2))
                linelen=math.sqrt((t1[2]-t2[2])*(t1[2]-t2[2])+(t1[3]-t2[3])*(t1[3]-t2[3])+(t1[4]-t2[4])*(t1[4]-t2[4]))
                                
                empty.append(x+" "+str(areaid)+" "+str(linelen)+' Out_side')
                node_list[int(t1[-1])-1]=node_list[int(t1[-1])-1]+1
            else:
                # areaid=int(imarray[math.floor(t1[4]),math.floor(319-t1[3]),math.floor(t1[2])]) #y轴翻转，xz调换 Vaa3d中读入tif似乎会做翻转，不知道为什么
                areaid=int(imarray[math.floor(t1[4]),math.floor(t1[3]),math.floor(t1[2])]) #xz调换 python直接读入源文件是没有翻转的
                
                ## 判断位置
                if math.floor(t1[4])>228:
                    temp_side='left'
                else:
                    temp_side='right'
                
                # 失配矫正
                if areaid==0:
                    if int(imarray[math.floor(t1[4])+1,math.floor(t1[3]),math.floor(t1[2])])!=0:
                        areaid=int(imarray[math.floor(t1[4])+1,math.floor(t1[3]),math.floor(t1[2])])
                        
                    elif int(imarray[math.floor(t1[4]),math.floor(t1[3])+1,math.floor(t1[2])])!=0:
                        areaid=int(imarray[math.floor(t1[4]),math.floor(t1[3])+1,math.floor(t1[2])])
                    
                    elif int(imarray[math.floor(t1[4]),math.floor(t1[3]),math.floor(t1[2])+1])!=0:
                        areaid=int(imarray[math.floor(t1[4]),math.floor(t1[3]),math.floor(t1[2])+1])
                    
                    elif int(imarray[math.floor(t1[4])+1,math.floor(t1[3])+1,math.floor(t1[2])])!=0:
                        areaid=int(imarray[math.floor(t1[4])+1,math.floor(t1[3])+1,math.floor(t1[2])])
                    
                    elif int(imarray[math.floor(t1[4])+1,math.floor(t1[3]),math.floor(t1[2])+1])!=0:
                        areaid=int(imarray[math.floor(t1[4])+1,math.floor(t1[3]),math.floor(t1[2])+1])
                    
                    elif int(imarray[math.floor(t1[4]),math.floor(t1[3])+1,math.floor(t1[2])+1])!=0:
                        areaid=int(imarray[math.floor(t1[4]),math.floor(t1[3])+1,math.floor(t1[2])+1])
                    
                    elif int(imarray[math.floor(t1[4])+1,math.floor(t1[3])+1,math.floor(t1[2])+1])!=0:
                        areaid=int(imarray[math.floor(t1[4])+1,math.floor(t1[3])+1,math.floor(t1[2])+1])
                # 仍然失配 则为0
                
                # 非soma区域
                if int(t1[-1])!=-1:
                    t2=contents[int(t1[-1])-1].split( )
                    t2=list(map(float,t2))
                    linelen=math.sqrt((t1[2]-t2[2])*(t1[2]-t2[2])+(t1[3]-t2[3])*(t1[3]-t2[3])+(t1[4]-t2[4])*(t1[4]-t2[4]))
                    empty.append(x+" "+str(areaid)+" "+str(linelen)+' '+temp_side)
                    node_list[int(t1[-1])-1]=node_list[int(t1[-1])-1]+1
                else:
                    # soma区域(也可能是断点，不影响后续统计)
                    empty.append(x+" "+str(areaid)+" "+"0 "+temp_side)
                    node_list[int(t1[-1])-1]=node_list[int(t1[-1])-1]+1

        # 转换为csv
        data=[]
        for i in range(0,len(empty)):
            temp=empty[i].split()
            temp.append(node_list[i])
            data.append(temp)

        with open("..\\Out\\"+t[0]+"_cul.csv","w+",newline='') as f:
            csv_writer = csv.writer(f)
            for rows in data:
                csv_writer.writerow(rows)
            f.close()

if __name__ == "__main__":
    for root,dirs,files in os.walk(path,topdown=True):
#        files.reverse();
        for name in files:
            filecalculation(root,name)
'''
##n type x        y        z      r  parent regionid length side   leaf
  1,1,   112.068, 148.238, 152.0, 1, -1,    1101,    0,     right, 8

'''

'''
from multiprocessing.pool import Pool
    # 创建多个进程，表示可以同时执行的进程数量。默认大小是CPU的核心数
    p = Pool(8)
    for root,dirs,files in os.walk(path,topdown=True):
        files.reverse();
        for name in files:
            p.apply_async(filecalculation, args=(root,name))
    # 如果我们用的是进程池，在调用join()之前必须要先close()，并且在close()之后不能再继续往进程池添加新的进程
    p.close()
    # 进程池对象调用join，会等待进程吃中所有的子进程结束完毕再去结束父进程
    p.join()
    print("父进程结束。")
'''