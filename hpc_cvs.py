import multiprocessing as mp
import os
import sys
import numpy as np
import pandas as pd
import scipy
from matplotlib import pyplot as plt


def run_chunk(arguments):
    LAM, W0, alpha, dt, tw, pet, num_sims, cpu = arguments        
    t = np.linspace(0,tw,int(np.ceil(tw/dt)))
    CV = np.zeros_like(LAM)
    for i in range(np.shape(LAM)[0]):
        for j in range(np.shape(LAM)[1]):
            lam, w0 = LAM[i,j], W0[i,j]
            S = np.zeros((num_sims, len(t)))
            for num in range(num_sims): 
                rainfall = np.array([np.random.exponential(alpha) if np.random.uniform() > np.exp(-lam*dt) else 0.0 for i in range(len(t))])
                x = np.zeros_like(rainfall)
                for idx in range(len(rainfall)-1):
                    dx = rainfall[idx]/w0 - pet*x[idx]*dt/w0
                    x[idx+1] = x[idx] + dx
                    x[idx+1] = np.min([x[idx+1], 1])
                s = x*w0
                S[num,:] = s
            CV[i,j] = np.std(S[:,-1])/np.mean(S[:,-1])
    return (CV, cpu)

def main():
    cores = mp.cpu_count()
    sys.stdout.write('There are %s cores'%(cores) + '\r\n')
    tw = 180.0 # wet season length in days
    pet = 2.0  # pet during wet season (mm/day)
    dt = 0.1
    alpha = 60.0
    num_sims = 10000
    W0 = np.linspace(50, 1000, 50)
    LAM = np.linspace(1/30., 8/30.0,50)
    X,Y = np.meshgrid(LAM, W0)
    Xs, Ys = np.array_split(X,cores), np.array_split(Y, cores)
    args = [(Xs[i], Ys[i], alpha, dt, tw, pet, num_sims, range(cores)[i]) for i in range(len(Xs))]
    pool = mp.Pool()
    results = pool.map(run_chunk, args)
    CVS_list = [0 for i in range(len(Xs))]
    for result in results:
         CVS_list[result[1]] = result[0]

    pool.close()
    pool.terminate()
    CVS = np.concatenate(CVS_list)
    pd.to_pickle([X, Y, CVS], './monte_carlo_output/output.p')

    # plt.contourf(X,Y,CVS)
    # plt.xlabel('Storm frequency [events per day]')
    # plt.ylabel('Storage capacity [mm]')
    # plt.title('Dry season storage sensitivity\nto climate and storage capacity')
    # cb = plt.colorbar()
    # cb.set_label('CV conditions @ dry season start ')
    # plt.savefig('./plots/output.pdf')

if __name__ == '__main__':
    main()

