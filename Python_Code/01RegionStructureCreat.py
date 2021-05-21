#生成区域关系文件
import csv

with open("..\\Other Information\\Mouse.csv", "r") as f1:
    reader = csv.reader(f1)
    print(type(reader)) 
    empty=[];
    result = list(reader)
    f1.close()
    del result[0]
    temp=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];
    record=[]
    for rows in result:
        depth=len(rows)-9
        record.append(depth)
        temp[depth-1]=rows[1]
        strtemp="/"
        for i in range(0,depth):
            strtemp=strtemp+str(temp[i])+"/"
        if ',' in rows[-1]:
            rows[-1]=rows[-1].replace(', ',' - ')
        empty.append([rows[1],strtemp,rows[-1],rows[2],depth])

empty.append(["0","/0/","Other Areas","Other Areas",1])
empty.append(["-1","/-1/","Outside Areas","Outside Areas",1])
    

with open('..\\Data\\Dataset_Structure.csv','w+',newline='') as f2:
    csv_writer = csv.writer(f2)
    for rows in empty:
        csv_writer.writerow(rows)
    f2.close()