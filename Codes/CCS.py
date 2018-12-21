import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt

#1/T = C1 + C2 * ln(R) + C3 * ln(R)3 - Steinhart-Hart Eqn
def T(R,c1,c2,c3):
    return 1/(c1 + c2*np.log(R) +c3*np.log(R)**3)

def chi_sq(data_1, data_true):
    x=[]
    bin = len(data_1)
    for i in range(len(data_1)):
        z = (data_1[i] - data_true[i])**2/data_true[i]
        x.append(z)
    s = sum(x)/(bin-1)
    if s > 3.5:
        print('Bad fit: Chi_sq = %.2f' % (s,))
    if np.isclose(s,1.,1.):
        print('Okay fit: Chi_sq = %.2f' % (s,))
    if s < 1.:
        print('Great fit: Chi_sq = %.2f' % (s,))
#get the calibration data: T in K, R in Omhs
T_room =
R_room =
T_ice =
R_ice =
T_LN2 =
R_LN2 =

T_measured = np.array([T_room, T_ice, T_LN2])
Resistance = np.array([R_room, R_ice, R_LN2])

#curvefit
popt, pcovt = optimize.curve_fit(T,T_measured,Resistance,(0,0,0))
err = np.sqrt(np.diag(pcovt))
print("The parameters are:",popt)
print("Error is:",err)
R = np.linspace(Resistance.min() - 5, Resistance.max() + 5, 1000)
t = T(R,*popt)

#get the chisq
print(chi_sq(T(Resistance,*popt),T_measured))

#plot the results
plt.plot(R,t,label = 'Fit')
plt.scatter(Resistance,T_measured, label = 'Measured')
plt.legend()
#plt.text("")
plt.xlabel("Resistance (Ohms)")
plt.ylabel("Temperature (Kelvin)")
plt.savefig("/Users/lucas/Documents/SLab/Data/Calibrated_Thermistor.png")
