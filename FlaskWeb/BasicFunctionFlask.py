'''包含公用的函数'''
import string
import os
from PIL import Image
import numpy as np
import random
import xlrd
import csv
#获取U盘盘符
def get_disklist():
    disk_list = []
    for c in string.ascii_uppercase:
        disk = c+':'
        if os.path.isdir(disk):
            disk_list.append(disk)
    return disk_list[-1]
'''
# Image.open会全部转换为uint8问题很大
def tif_read(path):
    img = Image.open(path)
    images = []
    for i in range(img.n_frames):
        img.seek(i)
        images.append(np.array(img))
    return np.array(images)
'''
def randomcolor():
    colorArr=['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
    color=""
    for i in range(6):
        color+=colorArr[random.randint(0,14)]
    return '#'+color

def read_xlsx(path,sheetname):
    workbook = xlrd.open_workbook(path)
    booksheet = workbook.sheet_by_name(sheetname)
    p = list()
    for row in range(booksheet.nrows):
            row_data = []
            for col in range(booksheet.ncols):
                    cel = booksheet.cell(row, col)
                    val = cel.value
                    try:
                            val = cel.value
                            val = re.sub(r'\s+', '', val)
                    except:
                            pass
 
                    if type(val) == float:
                        val = int(val)
                    else:
                        val = str( val )
                    row_data.append(val)
            p.append(row_data)
    return  p

# 清空所有变量
def clear_all():
    #Clears all the variables from the workspace of the spyder application.
    gl = globals().copy()
    for var in gl:
        if var[0] == '_': continue
        if 'func' in str(globals()[var]): continue
        if 'module' in str(globals()[var]): continue
        del globals()[var]
        
#  根据区域id list 得到区域名称 
def getregionname(id_list,aa):
    # 如果有同侧异侧标记
    side_list=[]
    if 'side' in str(aa):
        for i in range(0,len(id_list)):
            x=id_list[i].split('_')
            side_list.append(x[1])
            x=x[0]
            id_list[i]=x
        aa=int(aa[-1])
        
    name_list=[]
    with open("..\\Data\\Dataset_Structure.csv", "r") as f:
        reader = csv.reader(f)
        struct_data=np.array(list(reader))
        area_list=struct_data[:,0].tolist()
        for i in range(0,len(id_list)):
            t= area_list.index(id_list[i])
            t1=struct_data[t,2+aa].tolist()
            if len(side_list):
                name_list.append(t1+'_'+side_list[i][0:3])
            else:
                name_list.append(t1)
    return name_list