import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt
import pandas as pd

def Temp(R,c1,c2,c3):
    return   1/(c1 + c2*np.log(R) + c3*(np.log(R))**3) #c1*np.exp(1000.*c2/R)
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
def R(T,c1,c2):
    return 1000*c2/np.log(T/c1)
def T_K(v,v_ref):
    d0 =0.000000*0
    d1 =2.5173462*10
    d2 =-1.1662878*1
    d3 =-1.0833638*1
    d4 =-8.9773540*10**(-1)
    d5 =-3.7342377*10**(-1)
    d6 =-8.6632643*10**(-2)
    d7 =-1.0450598*10**(-2)
    d8 =-5.1920577*10**(-4)
    V = v + v_ref
    t = d0+d1*V+d2*V**2+d3*V**3+d4*V**4+d5*V**5+d6*V**6+d7*V**7+d8*V**8
    T = t + 273.15
    return T
def fit(f,x,y):
    #curvefit
    popt, pcovt = optimize.curve_fit(f,x,y,(1,0,0))
    err = np.sqrt(np.diag(pcovt))
    #print("The parameters are:",popt)
    #print("Uncertianty in the parameters is:",err)
    #R = np.linspace(Resistance.min() - 5, Resistance.max() + 5, 1000)
    #t = T(R,*popt)
    #get the chisq
    #print(chi_sq(T(Resistance,*popt),T_measured))
    return popt, err

T_room = 293.1
R_room = 969.6
T_ice = 273.1
R_ice = 972.1
T_but = 136
R_but = 1156.0 #1153
T_dia = 195.2
R_dia = 1051.56
T_LN2 = 77.2
R_LN2 = 1294.5 #1295.2
T_LHe = 4.2
R_LHe = 3705.7
T_meth = 175.6
R_meth = 1074.56
T_CO2 = 194.65
R_CO2 = 1046.3
T_A = 178.15
R_A  = 1073.52
Tm = np.array([T_ice,T_CO2,T_meth,T_dia,T_A,T_but,T_LN2])
Rm = np.array([R_ice,R_CO2,R_meth,R_dia,R_A,R_but,R_LN2])

coef, err = fit(Temp,Rm,Tm)
print("a = %f pm %f, b = %f pm %f, c = %f pm %f"%(coef[0],err[0],coef[1],err[1],coef[2],err[2]))
r = np.linspace(900,4000,1000)
T = Temp(r,*coef)
plt.plot(r,T,c = 'r',label= 'Fit')
plt.scatter(Rm,Tm,label = 'Data')
plt.legend()
plt.xlabel("Resistance (Ohms)")
plt.ylabel("Temperature (Kelvin)")
plt.savefig("/Users/lucas/Documents/SLab/Data/Calibrated_Thermistor_11_7.png")
R = data['R'][1140]
a = np.exp(1000*coef[1]/R)
b = (1000*coef[0]/R)*a
c = - b*coef[1]/R
dR = R*0.000001
err/coef
print("part1 = %f, part2 = %f, part3 = %f" % (a**2*err[0]**2 ,b**2*err[1]**2,c**2*dR**2))
print("R = %f" % (R))
print("T=%f"%(Temp(R,*coef)))
print("Chisq = %f"%(chi_sq(Tm, Temp(Rm,*coef))))
print("err/coef = %f, %f, %f" % (err[0]/coef[0],err[1]/coef[1],err[2]/coef[2]))
#print("dT = %f"%(np.sqrt(a**2*err[0]**2 +b**2*err[1]**2 + c**2*dR**2),))

#print("T=%f"%(Temp(960.,*coef)))


#plt.scatter(data['R'][4800:4900],data['T'][4800:4900])
