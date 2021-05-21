## 使用pyecharts画结构图

from pyecharts import options as opts
from pyecharts.charts import Page, Tree
#https://pyecharts.org/#/zh-cn/tree_charts
## 需要调整大小 
#pyecharts

# CTX结构
data_ctx = [{"children": [
        {"children":[
                {"children":[
                       {"name":"FRP(0)"},
                        {"name":"MO(91)"},
                        {"name":"SS(251)"},
                        {"name":"GU(10)"},
                        {"name":"VISC(7)"},
                        {"name":"AUD(18)"},
                        {"name":"VIS(51)"},
                        {"name":"ACA(4)"},
                        {"name":"PL(1)"},
                        {"name":"ILA(0)"},
                        {"name":"ORB(8)"},
                        {"name":"AI(36)"},
                        {"name":"RSP(35)"},
                        {"name":"PTLp(14)"},
                        {"name":"TEa(9)"},
                        {"name":"PERI(0)"},
                        {"name":"ECT(4)"}
                        ],"name": "Isocortex(539)"},
                {"children":[
                        {"name":"MOB(0)"},
                        {"name":"AOB(0)"},
                        {"name":"AON(4)"},
                        {"name":"TT(0)"},
                        {"name":"DP(0)"},
                        {"name":"PIR(2)"},
                        {"name":"NLOT(0)"},
                        {"name":"COA(1)"},
                        {"name":"PAA(1)"},
                        {"name":"TR(0)"}
                        ],"name": "Olfactory areas(12)"},
                {"children":[
                        {"name": "HIP(11)"},
                        {"name": "RHP(10)"}
                        ],"name": "Hippocampal formation(21)"}
                ],"name": "Cortical plate(572)"},
         {"children":[
                {"name": "Layer 6b, isocortex(0)"},
                {"name": "Claustrum(16)"},
                {"children":[
                        {"name": "EPd(3)"},
                        {"name": "EPv(0)"}
                        ],"name": "Endopiriform nucleus(3)"},
                {"name": "Lateral amygdalar nucleus(1)"},
                {"children":[
                        {"name": "BLAa(1)"},
                        {"name": "BLAp(0)"},
                        {"name": "BLAv(0)"}
                        ],"name": "Basolateral amygdalar nucleus(1)"},
                {"children":[
                        {"name": "BMAa(0)"},
                        {"name": "BMAp(1)"}
                        ],"name": "Basomedial amygdalar nucleus(1)"},
                {"name": "Posterior amygdalar nucleus(3)"}
                ],"name": "Cortical subplate(24)"}       
        ],"name": "Cerebral cortex(596)"}
]


# TH结构
data_th = [{"children": [
        {"children":[
                {"name":"VENT(394)"},
                {"name":"SPF(0)"},
                {"name":"SPA(0)"},
                {"name":"PP(0)"},
                {"name":"GENd(86)"}
                ],"name": "Thalamus, sensory-motor cortex related(480)"},
        {"children":[
                {"name":"LAT(52)"},
                {"name":"ATN(20)"},
                {"name":"MED(14)"},
                {"name":"MTN(13)"},
                {"name":"ILM(8)"},
                {"name":"RT(42)"},
                {"name":"GENv(9)"},
                {"name":"EPI(0)"}
                ],"name": "Thalamus, polymodal association cortex related(158)"}
        ],"name": "Thalamus(657)"}
]


# 整体到CTX TH
data = [{"children": [
    {"name":"Other Areas(0)"},
    {"name":"Outside Areas(2)"},
    {"children": [
                {"children":[
                        {"children":[
#                                {"name": "Cerebral cortex"}
                                data_ctx[0]
                                ],"name": "Cerebrum(900)"},
                        {"children":[
                                {"children":[
#                                        {"name": "Thalamus"}
                                        data_th[0]
                                        ],"name": "Interbrain(677)"}
                                ],"name": "Brain stem(688)"}
                    ],"name": "grey(1588)"}
                ],"name": "root(1706)"}
            
        ],"name": "All data(1708)"}
]


tree=(
      Tree(
              init_opts=opts.InitOpts(width='1960px',height='1200px')
      )
      .add("",data,layout="orthogonal",symbol_size=15,collapse_interval=0,initial_tree_depth=7,
              label_opts=opts.LabelOpts(font_size=16,font_weight='bolder')
           )
      .set_global_opts(title_opts=opts.TitleOpts(title="Total-Structure"))
 )


tree.render()



## 完整数据
'''
# CTX结构
data_ctx = [{"children": [
        {"children":[
                {"children":[
                        {"name":"Frontal pole, cerebral cortex(0)"},
                        {"name":"Somatomotor areas(91)"},
                        {"name":"Somatosensory areas(251)"},
                        {"name":"Gustatory areas(10)"},
                        {"name":"Visceral area(7)"},
                        {"name":"Auditory areas(18)"},
                        {"name":"Visual areas(51)"},
                        {"name":"Anterior cingulate area(4)"},
                        {"name":"Prelimbic area(1)"},
                        {"name":"Infralimbic area(0)"},
                        {"name":"Orbital area(8)"},
                        {"name":"Agranular insular area(36)"},
                        {"name":"Retrosplenial area(35)"},
                        {"name":"Posterior parietal association areas(14)"},
                        {"name":"Temporal association areas(9)"},
                        {"name":"Perirhinal area(0)"},
                        {"name":"Ectorhinal area(4)"}
                        ],"name": "Isocortex(539)"},
                {"children":[
                        {"name": "Main olfactory bulb(0)"},
                        {"name": "Accessory olfactory bulb(0)"},
                        {"name": "Anterior olfactory nucleus(4)"},
                        {"name": "Taenia tecta(0)"},
                        {"name": "Dorsal peduncular area(0)"},
                        {"name": "Piriform area(2)"},
                        {"name": "Nucleus of the lateral olfactory tract(0)"},
                        {"name": "Cortical amygdalar area(1)"},
                        {"name": "Piriform-amygdalar area(1)"},
                        {"name": "Postpiriform transition area(0)"}
                        ],"name": "Olfactory areas(12)"},
                {"children":[
                        {"name": "Hippocampal region(11)"},
                        {"name": "Retrohippocampal region(10)"}
                        ],"name": "Hippocampal formation(21)"}
                ],"name": "Cortical plate(572)"},
         {"children":[
                {"name": "Layer 6b, isocortex(0)"},
                {"name": "Claustrum(16)"},
                {"children":[
                        {"name": "dorsal part(3)"},
                        {"name": "ventral part(0)"}
                        ],"name": "Endopiriform nucleus(3)"},
                {"name": "Lateral amygdalar nucleus(1)"},
                {"children":[
                        {"name": "anterior part(1)"},
                        {"name": "posterior part(0)"},
                        {"name": "ventral part(0)"}
                        ],"name": "Basolateral amygdalar nucleus(1)"},
                {"children":[
                        {"name": "anterior part(0)"},
                        {"name": "posterior part(1)"}
                        ],"name": "Basomedial amygdalar nucleus(1)"},
                {"name": "Posterior amygdalar nucleus(3)"}
                ],"name": "Cortical subplate(24)"}       
        ],"name": "Cerebral cortex(596)"}
]


# TH结构
data_th = [{"children": [
        {"children":[
                {"name": "Ventral group of the dorsal thalamus(394)"},
                {"name": "Subparafascicular nucleus(0)"},
                {"name": "Subparafascicular area(0)"},
                {"name": "Peripeduncular nucleus(0)"},
                {"name": "Geniculate group, dorsal thalamus(86)"}
                ],"name": "Thalamus, sensory-motor cortex related(480)"},
        {"children":[
                {"name": "Lateral group of the dorsal thalamus(52)"},
                {"name": "Anterior group of the dorsal thalamus(20)"},
                {"name": "Medial group of the dorsal thalamus(14)"},
                {"name": "Midline group of the dorsal thalamus(13)"},
                {"name": "Intralaminar nuclei of the dorsal thalamus(8)"},
                {"name": "Reticular nucleus of the thalamus(42)"},
                {"name": "Geniculate group, ventral thalamus(9)"},
                {"name": "Epithalamus(0)"}
                ],"name": "Thalamus, polymodal association cortex related(158)"}
        ],"name": "Thalamus(657)"}
]


# 整体到CTX TH
data = [{"children": [
    {"name":"Other Areas(0)"},
    {"name":"Outside Areas(2)"},
    {"children": [
                {"children":[
                        {"children":[
#                                {"name": "Cerebral cortex"}
                                data_ctx[0]
                                ],"name": "Cerebrum(900)"},
                        {"children":[
                                {"children":[
#                                        {"name": "Thalamus"}
                                        data_th[0]
                                        ],"name": "Interbrain(677)"}
                                ],"name": "Brain stem(688)"}
                    ],"name": "Basic cell groups and regions(1588)"}
                ],"name": "root(1706)"}
            
        ],"name": "All data(1708)"}
]
'''