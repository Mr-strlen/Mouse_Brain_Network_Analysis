/* test_plugin.cpp
 * This is a test plugin, you can use it as a demo.
 * 2020-12-8 : by YourName
 */
 
#include "v3d_message.h"
#include "v3d_interface.h"
#include <vector>
#include "test_plugin.h"
using namespace std;
Q_EXPORT_PLUGIN2(test, TestPlugin);
 
QStringList TestPlugin::menulist() const
{
	return QStringList() 
		<<tr("menu1")
		<<tr("menu2")
		<<tr("about");
}

QStringList TestPlugin::funclist() const
{
	return QStringList()
		<<tr("func1")
		<<tr("func2")
		<<tr("help");
}

void TestPlugin::domenu(const QString &menu_name, V3DPluginCallback2 &callback, QWidget *parent)
{
	if (menu_name == tr("menu1"))
	{
        unsigned char * inimg1d = 0;
        V3DLONG  in_sz[4];
        int datatype;
        char * filenames="D:\\Vaa3D_QPH\\vaa3d_tools\\hackathon\\Graduation_Project\\Test_Data\\236174_3829_x14826_y27255.semi_r.swc";
        if(!simple_loadimage_wrapper(callback,filenames, inimg1d, in_sz, datatype))
        {
            v3d_msg("It's success!");
        }

	}
	else if (menu_name == tr("menu2"))
	{
		v3d_msg("To be implemented.");
	}
	else
	{
		v3d_msg(tr("This is a test plugin, you can use it as a demo.. "
			"Developed by YourName, 2020-12-8"));
	}
}

bool TestPlugin::dofunc(const QString & func_name, const V3DPluginArgList & input, V3DPluginArgList & output, V3DPluginCallback2 & callback,  QWidget * parent)
{
	vector<char*> infiles, inparas, outfiles;
	if(input.size() >= 1) infiles = *((vector<char*> *)input.at(0).p);
	if(input.size() >= 2) inparas = *((vector<char*> *)input.at(1).p);
	if(output.size() >= 1) outfiles = *((vector<char*> *)output.at(0).p);

	if (func_name == tr("func1"))
	{
        v3d_msg("To be implemented.");
    }
	else if (func_name == tr("func2"))
	{
		v3d_msg("To be implemented.");
	}
	else if (func_name == tr("help"))
	{
		v3d_msg("To be implemented.");
	}
	else return false;

	return true;
}

