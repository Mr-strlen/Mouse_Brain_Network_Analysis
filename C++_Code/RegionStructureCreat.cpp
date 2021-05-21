#include "BasicFunction.h"
int main(){
    string diskname=GetDisklist();
    string filepath=diskname+"Vaa3D\\Other Information\\Mouse_temp.csv";
    string outpath="..\\TreeRecord.csv";
    ifstream in(filepath);
    ofstream OpenFile(outpath); 
    int count=0;
    string query;
    int TreeLevel[14]={0};
    while(getline(in,query)){
        if (count==0){count++;continue;}
        vector<string> temp;
        temp=split(query,",");
        int depth=CountCharNum(query,',')-8;
        TreeLevel[depth-1]=atoi(temp[0].data());
        string strtemp="/";
        for(int i=0;i<depth-1;i++)
            strtemp=strtemp+to_string(TreeLevel[i])+"/";
        strtemp=strtemp+to_string(TreeLevel[depth-1]);
        OpenFile<<temp[0]<<","<<strtemp<<endl;       
    }
    OpenFile<<"0,/0"<<endl;
    OpenFile.close();
    return 0;
}