import numpy as np

## 单个神经元数据和中尺度网络的比较
total=np.load('.\Save_Data\connection_matrix.npy')
single=np.load('.\Save_Data\connection_matrix_single.npy')
middle=np.load('.\Save_Data\connection_matrix_allen.npy')
data=[]
data_s=[]
data_m=[]
for i in range(0,total.shape[0]):
    for j in range(0,total.shape[1]):
        if total[i,j]>0:
            data.append(total[i,j])
            
for i in range(0,single.shape[0]):
    for j in range(0,single.shape[1]):
        if single[i,j]>0:
            data_s.append(single[i,j])
            
for i in range(0,middle.shape[0]):
    for j in range(0,middle.shape[1]):
        if middle[i,j]>0:
            data_m.append(middle[i,j])


import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy.stats import norm
mu =np.mean(data) 
sigma =np.std(data)
mu_s =np.mean(data_s) 
sigma_s =np.std(data_s)
mu_m =np.mean(data_m) 
sigma_m =np.std(data_m)

num_bins = 100 #直方图柱子的数量

n_s, bins_s, patches_s = plt.hist(data_s,bins=num_bins,range=(-2,4.5), density=1, alpha=0.55)
n_m, bins_m, patches_m = plt.hist(data_m,bins=num_bins,range=(-2,4.5), density=1, alpha=0.55)
n, bins, patches = plt.hist(data,bins=num_bins,range=(-2,4.5), density=1, alpha=0.55)


y_s = norm.pdf(bins_s, mu_s, sigma_s)
y_m = norm.pdf(bins_m, mu_m, sigma_m)
y = norm.pdf(bins, mu, sigma)

plt.plot(bins_s, y_s, linewidth=3, color='#4169E1') #绘制y的曲线
plt.plot(bins_m, y_m, linewidth=3, color='#FF8C00') #绘制y的曲线
plt.plot(bins, y, linewidth=3, color='#228B22') #绘制y的曲线

plt.legend(['single-neuron fitted curve','mesoscopic fitted curve','refined fitted curve','single-neuron data','mesoscopic data','refined data'])

plt.xlabel('Value',fontsize=12)
plt.ylabel('Probability',fontsize=12)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)


import pandas as pd
s = pd.DataFrame(data_s)
print(s.describe())
s = pd.DataFrame(data_m)
print(s.describe())
s = pd.DataFrame(data)
print(s.describe())