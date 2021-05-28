import csv
import numpy as np
import BasicFunction as BF
import matplotlib.pyplot as plt

## 读取Reco_Dataset_Cell得到映射矩阵 
with open("..\\Data\\Reco_Dataset_Cell.csv", "r") as f:
    reader = csv.reader(f)
    data=np.array(list(reader))
region_list=[]
projection_list=[]
for i in data:
    region_list.append(str(i[0]))
    projection_list.append(str(i[1])+'_'+str(i[2]))
region_list=list(set(region_list))
projection_list=list(set(projection_list))

projection_list=BF.getregionname(projection_list,'side1')
region_list=BF.getregionname(region_list,1)


allen_matrix=np.zeros([len(region_list),len(projection_list)])
region_list.sort()
projection_list.sort()

'''
## allen experiment data 
# document https://allensdk.readthedocs.io/en/latest/allensdk.core.mouse_connectivity_cache.html
import pandas as pd
from allensdk.core.mouse_connectivity_cache import MouseConnectivityCache
mcc = MouseConnectivityCache()
structure_tree = mcc.get_structure_tree()

allen_proj=[]
for x in projection_list:
    allen_proj.append(x.split('_')[0])
allen_proj=list(set(allen_proj))
allen_proj.sort()

import time,math
time_start = time.time()

for i in range(0,len(region_list)):
    time_end = time.time() 
    print('Time cost = %fs' % (time_end - time_start))
    time_start = time_end
    if i>0:
        np.save('./temp/mratix'+'_'+str(i)+'.npy',allen_matrix)
    for j in range(0,len(allen_proj)):
        if j%10==0:
            print([i,j])
        
        soma=region_list[i]
        proj=allen_proj[j]

        if soma =='Other Areas' or proj == 'Other Areas' or soma =='Outside Areas' or proj == 'Outside Areas':
            continue
        
        try:
            soma_region = structure_tree.get_structures_by_acronym([soma])[0]
        except:
            soma_region=[]
            print('soma region not exist: '+soma)
        
        try:
            proj_region = structure_tree.get_structures_by_acronym([proj])[0]
        except:
            soma_region=[]
            print('projection region not exist: '+proj)
        
        
        select_experiments = mcc.get_experiments(cre=True,injection_structure_ids=[soma_region['id']])
        if len(select_experiments)<1:
            continue
        
        # print("%d experiments" % len(select_experiments))
        exp_hemi={}
        for e in select_experiments:
            try:
                exp_info=mcc.get_experiment_structure_unionizes(experiment_id=e['id'])
            except:
                print(str(e['id'])+' have problem')
                continue
            else:
                cc=list(exp_info['hemisphere_id'])
                if cc.count(2)>=cc.count(1):
                    exp_hemi[e['id']]=2
                else:
                    exp_hemi[e['id']]=1
                
        structure_unionizes = mcc.get_structure_unionizes([ e['id'] for e in select_experiments ], 
                                                  is_injection=False,
                                                  structure_ids=[proj_region['id']],
                                                  include_descendants=False)
        if len(structure_unionizes)<1:
            continue
        
        select_unionizes=structure_unionizes[structure_unionizes.hemisphere_id != 3]
        select_unionizes=select_unionizes[select_unionizes.volume > 0.1]
        select_unionizes=select_unionizes[select_unionizes.projection_density>0.00001]
        if len(select_unionizes)<1:
            continue
        else:
            con_list=[]
            ips_list=[]
            hemi_id=list(select_unionizes['hemisphere_id'])
            exp_id=list(select_unionizes['experiment_id'])
            npv_list=list(select_unionizes['normalized_projection_volume'])
            
            for k in range(0,len(select_unionizes)):
                if int(hemi_id[k])==exp_hemi[exp_id[k]]:
                    ips_list.append(float(npv_list[k]))
                else:
                    con_list.append(float(npv_list[k]))
            
            #矩阵填充
            if proj+'_Ips' in projection_list and len(ips_list)>0:
                t=projection_list.index(proj+'_Ips')
                allen_matrix[i,t]=np.mean(ips_list)
            if proj+'_Con' in projection_list and len(con_list)>0:
                t=projection_list.index(proj+'_Con')
                allen_matrix[i,t]=np.mean(con_list)
'''
import numpy as np
t1=np.load('./temp/mratix_12_202105261525.npy')
t2=np.load('./temp/mratix_32_202105261923.npy')
t3=np.load('./temp/mratix_48_202105262132.npy')
t4=np.load('./temp/mratix_70_202105262326.npy')
t5=np.load('./temp/mratix_112_202105271326.npy')
t6=np.load('./temp/mratix_117_202105271456.npy')
t7=np.load('./temp/mratix_160_202105272212.npy')
t8=np.load('./temp/mratix_161_202105280950.npy')


temp=t1[0:12,:]
temp=np.r_[temp,t2[12:32,:]]
temp=np.r_[temp,t3[32:48,:]]
temp=np.r_[temp,t4[48:70,:]]
temp=np.r_[temp,t5[70:112,:]]
temp=np.r_[temp,t6[112:117,:]]
temp=np.r_[temp,t7[117:160,:]]
temp=np.r_[temp,t8[160:161,:]]
temp=np.log(temp*100+1)

import seaborn as sns
sns_plot = sns.heatmap(temp)
np.save('./Save_Data/connection_matrix_allenbrainatlas.npy',allen_matrix)