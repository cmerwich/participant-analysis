__author__ = 'erwich/sikkel'

#Takes in a txt file, tab separated e.g.:
#C1	C1	0	2	0	0	0.0
#C2	C2	0	14	0	0	0.0
#S	S	0	10	0	0	0.0

from sys import argv
import numpy as np

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
