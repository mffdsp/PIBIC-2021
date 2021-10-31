import numpy as np
from math import *
import matplotlib.pyplot as plt

def detectRwave(ecg_file):
    x = np.load(ecg_file) #TODO trocar para json
    N = x.shape[0]

    #contagem de percentual de execucao
    ip = 0
    lg = 0

    # R detector variables
    sigma = 2
    delta = 2
    beta = 15
    atv = 0

    maxi = np.zeros(N+beta)
    mini = np.zeros(N+beta)
    h = np.zeros(N+beta)
    a = np.zeros(N+beta)
    g = np.zeros(N+beta)
    n = np.zeros(N+beta)
    r = np.zeros(N+beta)
    v = np.zeros(N+beta)
    w = np.zeros(N+beta)

    maxi[0] = x[0]
    mini[0] = x[0]
    h[0] = x[0] - (maxi[0]+mini[0])/2

    for i in range(1,N-1):
        if x[i] > maxi[i-1]:
            maxi[i] = maxi[i-1] + sigma*delta
        else:
            maxi[i] = maxi[i-1] - delta

        if x[i] < mini[i-1]:
            mini[i] = mini[i-1] - sigma*delta
        else:
            mini[i] = mini[i-1] + delta

        # filtro PA
        h[i] = x[i] - (maxi[i] + mini[i])/2

        # detector de amplitude
        a[i] = maxi[i] - mini[i]

        # extrator de ruidos
        if a[i] <= abs(h[i]):
            n[i] = np.sign(h[i])*(abs(h[i])-a[i])
        else:
            n[i] = 0

        # detector triangular
        if i > beta:
            if n[i]>0 and n[i-beta]<n[i] and n[i]>n[i+beta]:
                g[i] = n[i] - max(n[i-beta], n[i+beta])
            elif n[i]<0 and n[i-beta]>n[i] and n[i]<n[i+beta]:
                g[i] = n[i] + min(n[i-beta], n[i+beta])
            else:
                g[i] = 0

        # detector de cristas
        if g[i] > g[i-1] and g[i] > g[i+1]:
            r[i] = g[i]
        else:
            r[i] = 0

        # detector de vales
        if g[i] < g[i-1] and g[i] < g[i+1]:
            v[i] = g[i]
        else:
            v[i] = 0

        # unificador de batimentos
        if r[i] > 0:
            w[i] = r[i]
        elif v[i] < 0:
            w[i] = -v[i]

        # detector de batimentos
        if i > ip:
            print("executando...", lg)
            lg += 10
            ip += (N-1)/10

    T = np.arange(0,15,0.0001) #TODO usar T como entrada
    # T = T[:-beta]
    plt.plot(T, w[:-beta], linestyle=' ', marker='x')
    plt.plot(T,r[:-beta],color='r')
    plt.show()

if __name__ == "__main__":
    detectRwave('ecg.npy')