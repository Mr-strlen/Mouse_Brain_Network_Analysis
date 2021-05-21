#include "BasicFunction.h"
typedef struct Node{
    int type,parent,leaf=1;//类型，父节点，是否为叶子节点
    double x,y,z,r;//坐标xyz，半径
    double lenth;//所在分枝长度
    int areaid;//匹配区域编号
}Node;
Node Tree[100000];
int main()
{ 
	vector<string> files; 
	string filePath = "..\\Test_Data";
	//获取该路径下的所有文件  
	getFiles(filePath, files);
	char str[30];  
	int size = files.size();  
	for (int i = 0;i < size;i++)  
	{  
	    cout<<files[i].c_str()<<endl;  
        string query;
        ifstream in(files[0].c_str());
        int count=0;
        //构建结构体
        while(getline(in,query)){
            if (count==0){count++;continue;}
            vector<string> temp;
            temp=split(query," ");
            Tree[atoi(temp[0].data())-1].x=atof(temp[2].data());
            Tree[atoi(temp[0].data())-1].y=atof(temp[3].data());
            Tree[atoi(temp[0].data())-1].z=atof(temp[4].data());
            Tree[atoi(temp[0].data())-1].r=atof(temp[5].data());
            Tree[atoi(temp[0].data())-1].type=atoi(temp[1].data());
            Tree[atoi(temp[0].data())-1].parent=atoi(temp[6].data());
            if(Tree[atoi(temp[0].data())-1].parent!=-1){
                Tree[Tree[atoi(temp[0].data())-1].parent].leaf=0;
            }
            count++;
        }
        //进行区域匹配
        //计算路径长度
        for(int i=0;i<count;i++)
        {
            if(Tree[i].parent=-1)
                Tree[i].lenth=0;
            else
                Tree[i].lenth=sqrt((Tree[Tree[i].parent].x-Tree[i].x)*(Tree[Tree[i].parent].x-Tree[i].x)+
                (Tree[Tree[i].parent].y-Tree[i].y)*(Tree[Tree[i].parent].y-Tree[i].y)+
                (Tree[Tree[i].parent].z-Tree[i].z)*(Tree[Tree[i].parent].z-Tree[i].z));
        }
	}
   
	return 0;
}