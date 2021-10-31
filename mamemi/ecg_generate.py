import numpy as np
from math import *
from runkut4 import runkut4
import matplotlib.pyplot as plt

def generate(start_t, Ts, end_t, HR):

    #definindo condicoes para o ecg
    T = np.arange(start_t,end_t,Ts)
    N = T.shape[0]
    RR = 60/HR # duration between R waves
    tmax = 0.2 + 0.1555*RR
    ts_VAD = 0.5 # duration time of VAD systole
    t_eject = (RR*ts_VAD)/Ts # Ejection time for VAD in fill-to-empty operation
    t_eject_c = t_eject

    xecg = np.zeros((1,N))
    yecg = np.zeros((1,N))
    zecg = np.zeros((1,N))
    z0 = np.zeros((1,N))

    xecg[0][0] = -1

    x = np.array([xecg[0][0], yecg[0][0], zecg[0][0]])

    for i in range(N-1):
        xdot, x = runkut4(Ts, x, RR, z0[0][0])
        z0[0][i+1] = 0.15*sin(2*pi*(60/(12+np.random.normal()))*T[i+1])
        HR = 60 + 2*np.random.normal()
        RR = 60/HR
        xecg[0][i+1] = x[0]
        yecg[0][i+1] = x[1]
        zecg[0][i+1] = x[2]

    # plt.plot(T, zecg[0])
    # plt.show()
    # print(zecg[0])
    return zecg[0]

if __name__ == "__main__":
    ecg = generate(0,0.0001,15,60)
    np.save('ecg.npy',ecg)
    #TODO usar json e salvar vetor T