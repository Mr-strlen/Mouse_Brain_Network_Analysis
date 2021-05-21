# 将apo文件转换为swc文件
import BasicFunction as BF
import os
diskname=BF.get_disklist()
path='E:\\Vaa3D\\Other Information\\Bouton_apo'
out_path='E:\\Vaa3D\\Other Information\\Bouton_swc'
dir_list=[]
for root,dirs,files in os.walk(path,topdown=True):
    t=root.split('\\')
    dir_list.append(t[-1])
del dir_list[0]
# 读入数据
for dir_name in dir_list:
    for root,dirs,files in os.walk(path+'\\'+dir_name,topdown=True):
        for name in files:
            empty=['##n type x y z r parent']
            with open(os.path.join(root,name)) as file_object:
                contents = file_object.readlines()
                print(len(contents))
                file_object.close()
                while contents[0][0]=='#':
                    del contents[0]
            count=1
            for x in contents:
                t=x.split(',')
                empty.append(str(count)+' 1 '+t[5]+' '+t[6]+' '+t[4]+' 1 -1')
                count=count+1
            
            endstr = '\n'
            if not os.path.exists(out_path+'\\'+dir_name):
                os.mkdir(out_path+'\\'+dir_name)
            temp=name.split('.')
            with open(out_path+'\\'+dir_name+'\\'+temp[0]+'.swc',"w+") as f:
                f.write(endstr.join(empty))
                f.close()