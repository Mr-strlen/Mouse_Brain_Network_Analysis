#include<iostream>
#include<string>
#include<fstream>
#include<io.h>
#include<vector>
#include<math.h>
#include<Windows.h>
using namespace std;

//获取文件目录
void getFiles( string path, vector<string>& files )  
{  
    //文件句柄  
    long   hFile   =   0;  
    //文件信息  
    struct _finddata_t fileinfo;  
    string p;  
    if((hFile = _findfirst(p.assign(path).append("\\*").c_str(),&fileinfo)) !=  -1)  
    {  
        do  
        {  
            //如果是目录,迭代之  
            //如果不是,加入列表  
            if((fileinfo.attrib &  _A_SUBDIR))  
            {  
                if(strcmp(fileinfo.name,".") != 0  &&  strcmp(fileinfo.name,"..") != 0)  
                    getFiles( p.assign(path).append("\\").append(fileinfo.name), files );  
            }  
            else  
            {  
                files.push_back(p.assign(path).append("\\").append(fileinfo.name) );  
            }  
        }while(_findnext(hFile, &fileinfo)  == 0);  
        _findclose(hFile);  
    }  
}

//字符串分隔
vector<string> split(const string &s, const string &seperator){
    vector<string> result;
    typedef string::size_type string_size;
    string_size i = 0;
    
    while(i != s.size()){
    //找到字符串中首个不等于分隔符的字母；
        int flag = 0;
        while(i != s.size() && flag == 0){
            flag = 1;
            for(string_size x = 0; x < seperator.size(); ++x){
                if(s[i] == seperator[x]){
                       ++i;
                       flag = 0;
                       break;
                }
            }
        }
    
    //找到又一个分隔符，将两个分隔符之间的字符串取出；
    flag = 0;
    string_size j = i;
    while(j != s.size() && flag == 0){
        for(string_size x = 0; x < seperator.size(); ++x){
            if(s[j] == seperator[x]){
                flag = 1;
                break;
            }
            if(flag == 0) {++j;}
        }
    }
    if(i != j){
        result.push_back(s.substr(i, j-i));
        i = j;
    }
  }
  return result;
}

//统计某个符号数量（,）
int CountCharNum(const string s, const char a)
{
	int count=0,mark=-1;
    for(int i=0;i<s.length();i++)
    {
        //消除“”带来的影响
        if(s[i]=='"')
            mark=-mark;
        if(s[i]==a &&  mark<0)
            count++;
    }
    
    return count;
}

//获取本地磁盘符

string GetDisklist(){
    DWORD dwLen = GetLogicalDriveStrings(0, NULL);	//获取系统字符串长度.
	char * pszDriver = new char[dwLen];				//构建一个相应长度的数组.
	GetLogicalDriveStrings(dwLen, pszDriver);		//获取盘符字符串.
    string temp;
	while(*pszDriver != '\0'){	
        temp=pszDriver;
		pszDriver += strlen(pszDriver) + 1;			//定位到下一个字符串.加一是为了跳过'\0'字符串.
	}
    return temp;

}