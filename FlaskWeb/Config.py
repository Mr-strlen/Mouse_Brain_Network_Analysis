from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os, csv

app = Flask(__name__)

# session 秘钥
app.secret_key = os.getenv("SECRET_KEY", "secret string")

# 贫穷版
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:BrainTell123#@127.0.0.1:3306/BrainTellDataset?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
db=SQLAlchemy(app)

## 构建表
# soma的基本信息表
class SomaBasicInfo(db.Model):
    Dataset_Name = db.Column(db.String(20), nullable=True)
    Brain_Id = db.Column(db.String(20), nullable=True)
    Neuron_Id = db.Column(db.String(30), nullable=False, primary_key=True)
    Soma_X = db.Column(db.Float, nullable=False)
    Soma_Y = db.Column(db.Float, nullable=False)
    Soma_Z = db.Column(db.Float, nullable=False)
    Manually_Corrected_Soma_Region = db.Column(db.String(20), nullable=False)
    Cortical_Layer = db.Column(db.String(20), nullable=True)
    Transgenic_Line = db.Column(db.Text, nullable=True)

    def __init__(self, dataset_name, brain_id, nenuron_id, soma_x, soma_y, soma_z, manually_corrected_soma_region,
                 cortical_layer, transgenic_line):
        self.Dataset_Name = dataset_name
        self.Brain_Id = brain_id
        self.Neuron_Id = nenuron_id
        self.Soma_X = soma_x
        self.Soma_Y = soma_y
        self.Soma_Z = soma_z
        self.Manually_Corrected_Soma_Region = manually_corrected_soma_region
        self.Cortical_Layer = cortical_layer
        self.Transgenic_Line = transgenic_line

# celltype的基本信息表
class CellTypeInfo(db.Model):
    Celltype_Id = db.Column(db.String(20), nullable=True, primary_key=True)
    Celltype_Name = db.Column(db.String(20), nullable=True)
    Celltype_Fullname = db.Column(db.Text, nullable=True)
    Celltype_Path = db.Column(db.Text, nullable=True)
    Celltype_Depth = db.Column(db.Float, nullable=True)

    def __init__(self, celltype_id, celltype_name, celltype_fullname, celltype_path, celltype_depth):
        self.Celltype_Id = celltype_id
        self.Celltype_Name = celltype_name
        self.Celltype_Fullname = celltype_fullname
        self.Celltype_Path = celltype_path
        self.Celltype_Depth = celltype_depth


def app_init():
    db.create_all()
    ## 插入soma数据
    temp = db.session.query(SomaBasicInfo).all()
    if len(temp)<1:
        filepath = os.path.split(os.path.realpath(__file__))[0]
        filepath = filepath.replace('FlaskWeb', 'Other Information')
        with open(filepath + '\\Soma_region_and_location.csv', "r") as f:
            reader = csv.reader(f)
            Data = list(reader)
            del[Data[0]]
            f.close()
        for x in Data:
            if 'A' not in x[0]:
                dataset_name = 'BrainTell'
            else:
                dataset_name = 'Janelia'
            temp = SomaBasicInfo(dataset_name, x[7], x[0], float(x[1]), float(x[2]), float(x[3]), x[4], x[5], x[6])
            db.session.add(temp)
        db.session.commit()

    ## 插入celltype数据
    temp = db.session.query(CellTypeInfo).all()
    if len(temp) < 1:
        filepath = os.path.split(os.path.realpath(__file__))[0]
        filepath = filepath.replace('FlaskWeb', 'Other Information')
        with open(filepath + '\\Soma_region_and_location.csv', "r") as f:
            reader = csv.reader(f)
            Data = list(reader)
            del [Data[0]]
            f.close()
        celltype_list=[]
        for x in Data:
            celltype_list.append(x[4])
        celltype_list=list(set(celltype_list))
        celltype_list.sort()

        filepath = filepath.replace('Other Information','Data')
        with open(filepath +"\\Dataset_Structure.csv", "r") as f:
            reader = csv.reader(f)
            structure = list(reader)
            structure_list = []
            for x in structure:
                structure_list.append(x[3])
        for x in celltype_list:
            if x == 'unknown':
                x = 'Other Areas'
            t = structure_list.index(str(x))
            temp = CellTypeInfo(structure[t][0], structure[t][3], structure[t][2], structure[t][1], float(structure[t][4]))
            db.session.add(temp)
        db.session.commit()
    return app, db