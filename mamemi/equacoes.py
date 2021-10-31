from math import *
import numpy as np


def equacoes(x, RR, z0):
    A_ecg = np.array([1.2, -5, 30, -7.5, 0.75])
    B_ecg = np.array([0.25, 0.1, 0.1, 0.1, 0.4])
    TH = np.array([-1/3, -1/12, 0, 1/12, 1/2])*pi
    
    w = 2*pi/RR
    
    k = 0
    alpha = 1-sqrt(x[0]**2 + x[1]**2)
    th = atan2(x[1],x[0])
    for ii in range(5):
        k = k - (A_ecg[ii]*(th-TH[ii])*exp(-(th-TH[ii])**2/(2*B_ecg[ii]**2)))
    
    xdot = np.zeros(3)
    xdot[0] = alpha*x[0] - w*x[1] + 0*x[2]
    xdot[1] = w*x[0] + alpha*x[1] + 0*x[2]
    xdot[2] = 0*x[0] + 0*x[1] - 1*x[2] + k + z0
    
    return xdot