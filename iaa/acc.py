__author__ = 'erwich/sikkel'

#Takes in a txt file, tab separated e.g.:
#C1	C1	0	2	0	0	0.0
#C2	C2	0	14	0	0	0.0
#S	S	0	10	0	0	0.0
import os
from sys import argv
import numpy as np

#d_str = os.path.expanduser('~/github/cmerwich/participant-analysis/iaa/iaa-files')
#directory = ('~/iaa/iaa-files')

def print_total_corpus():
    '''
    Takes as input a txt file, tab separated.
    Accumulates the coref differences per txt file
    and prints its total on standard output.
    Example call: python3 acc.py Psalms_*.ann
    '''
    L = 0
    M = 0
    R = 0
    D = 0
    d = 0
    doc_str = os.path.expanduser('~/github/cmerwich/participant-analysis/iaa/iaa-files')
    for dirpath,_,filenames in os.walk(doc_str):
        for f in filenames:
            if f.endswith('.iaa'):
                fs = os.path.abspath(os.path.join(dirpath, f))
                data = np.loadtxt(fs, usecols=(2,3,4), dtype=int)
                L += data[:,0].sum()
                M += data[:,1].sum()
                R += data[:,2].sum()
                D = L + R 
                d = round(D/(L+M+R),4)

    print('total_corpus', '-', L, M, R, D, d, sep='\t')
    return 'total_corpus', L, M, R, D, d

def print_total(name):
    '''
    Takes as input a txt file, tab separated.
    Accumulates the coref differences per txt file
    and prints its total on standard output.
    Example call: python3 acc.py Psalms_*.ann
    '''
    
    data = np.loadtxt(name, usecols=(2,3,4), dtype=int)
    
    Lt = data[:,0].sum()
    Mt = data[:,1].sum()
    Rt = data[:,2].sum()
    Dt = Lt + Rt
    dt = round(Dt/(Lt+Mt+Rt),4)
    
    print(name, '-', Lt, Mt, Rt, Dt, dt, sep='\t')
    return name, Lt, Mt, Rt, Dt, dt

if __name__ == "__main__":
    for i in range(1, len(argv)):
        print_total(argv[i])