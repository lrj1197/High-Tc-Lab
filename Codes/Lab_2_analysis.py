from numpy import *
from scipy import optimize
import matplotlib.pyplot as plt
import os
import pandas as pd
from scipy.signal import argrelextrema

#Real data.txt, 3,
def chi_sq(data_1, data_true):
    x=[]
    bin = len(data_1)
    for i in range(len(data_1)):
        z = (data_1[i] - data_true[i])**2/data_true[i]
        x.append(z)
    s = sum(x)/(bin-1)
    if s < 1.:
        print('Great fit: Chi_sq = %.2f' % (s,))
        return s
    elif np.isclose(s,1.,1.):
        print('Okay fit: Chi_sq = %.2f' % (s,))
        return s
    else:
        print('Bad fit: Chi_sq = %.2f' % (s,))
        return s
def f(x,m,b):
    return m*x + b
#data = genfromtxt('/Users/lucas/Documents/SLab/Data/Lab_2_data/data0_11_7.txt')
data = genfromtxt('/Users/lucas/Documents/SLab/Data/Lab_2_data/data2_11_7.txt')
dataset = pd.DataFrame(data)

head = ['Temperature', 'Resistance', 'Time','Current', 'Power','dR',  'dT','Voltage','R_T']
for index in range(dataset.shape[1]):
    dataset[head[index]] = dataset[index]
    del dataset[index]
dataset.shape[0]
t = []
r = []
for index in range(dataset.shape[0]):
    if dataset['Time'][index] > 200.0 and dataset['Time'][index] < 2000:
        t.append(dataset['Temperature'][index])
        r.append(dataset['Resistance'][index])

        #print(dataset['Time'][index])
#dataset.head()


T = dataset['Temperature']
R = dataset['Resistance']
#sloped = [3400:3600]
#flat = [2000:2600]
#TF = T[2000:2600]
#RF = R[2000:2600]
#RS = R[3400:3600]
#TS = T[3400:3600]
#Whole Picture:[:11210]
#flat = [:10800]
#sloped = [10800:11210] - [10810:10960]

for i in range(len(T[:1500])):
    if R[i] > 1.2 and T[i] < 113.0:
        R[i] = nan
        T[i] = nan

#flat [:12000]
#sloped [12000:20000]

x = array([.16 for i in range(len(r[:10900]))])
y = array([.16 for i in range(len(r[10900:20000]))])

plt.scatter(t[:10900],r[:10900]-x,c='b',s=1)
plt.scatter(t[10900:20000],r[10900:20000]-y,c='b',s=1)
#plt.scatter(T[1200:1800],R[1200:1800],c='b')
plt.ylabel("Resistance (Ohms)")
plt.xlabel("Temperature (Kelvin)")
plt.savefig("/Users/lucas/Documents/SLab/Data/data2_uniform_11_7.png")



def Critical_Temp(R_flat,T_flat,R_sloped,T_sloped):
    popt_sloped, pcovt_sloped = optimize.curve_fit(f,T_sloped,R_sloped,(1,1))
    err_sloped = sqrt(diag(pcovt_sloped))
    popt_flat, pcovt_flat = optimize.curve_fit(f,T_flat,R_flat,(0,0))
    err_flat = sqrt(diag(pcovt_flat))
    print('%f %f %f %f'%(popt_sloped[0],popt_sloped[1],popt_flat[0],popt_flat[1]))
    print("%f %f %f %f"%(err_sloped[0],err_sloped[1],err_flat[0],err_flat[1]))
    Tc = (popt_sloped[1] - popt_flat[1])/(popt_flat[0] - popt_sloped[0])
    a = 1.*err_sloped[1]/(popt_flat[0] - popt_sloped[0])
    b = 1.*err_flat[1]/(-popt_flat[0] + popt_sloped[0])
    c = err_flat[0]*(popt_sloped[1] - popt_flat[1])/(popt_flat[0] - popt_sloped[0])**2
    d = err_sloped[0]*(popt_sloped[1] - popt_flat[1])/(popt_flat[0] - popt_sloped[0])**2
    dTc = sqrt(a**2 + b**2 + c**2 + d**2)
    return Tc,dTc
TS = t[10900:20000] -y
RS = r[10900:20000] -y
TF = t[:10900]-x
RF = r[:10900]-x

T,dT = Critical_Temp(RF,TF,RS,TS)

print("The Critical Temperature is %f with Uncertianty of %f"%(T,dT))
