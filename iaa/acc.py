__author__ = 'erwich/sikkel'

#Takes in a txt file, tab separated e.g.:
#C1	C1	0	2	0	0	0.0
#C2	C2	0	14	0	0	0.0
#S	S	0	10	0	0	0.0

import os
from sys import argv
import numpy as np

def print_total_corpus():
    '''
    Takes as input a txt iaa file, tab separated.
    Accumulates the coref values per txt file
    and prints the total values of the corpus.
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

def get_total_anns(doc_str):
    '''
    Takes as input a txt file, tab separated.
    Accumulates all coref values per txt file for one corpus,
    for A and B and returns a Psalms and Numbers tuple
    '''
    
    Aps = 0
    Bps = 0
    Anu = 0
    Bnu = 0
    
    Lps = 0
    Mps = 0
    Rps = 0
    Totps = 0
    tot_sets_ps = 0
    
    Lnu = 0
    Mnu = 0
    Rnu = 0
    Totnu = 0
    tot_sets_nu = 0
    
    ps_tup = tuple()
    nu_tup = tuple()

    for dirpath,_,filenames in os.walk(doc_str):
        for f in filenames:
            fs = os.path.abspath(os.path.join(dirpath, f))
            mention_data = np.loadtxt(fs, usecols=(2,3,4), dtype=int)
            classes = np.loadtxt(fs, usecols=(0,1), dtype=str)
            if f.startswith('Ps'):
                for i in classes[:,0]:
                    if i != '-':
                        Aps += 1
                for j in classes[:,1]:
                    if i != '-':
                        Bps += 1
                Lps += mention_data[:,0].sum()
                Mps += mention_data[:,1].sum()
                Rps += mention_data[:,2].sum()
                Totps = Lps+Mps+Rps
                tot_sets_ps = Aps + Bps
                
            elif f.startswith('Nu'):
                for i in classes[:,0]:
                    if i != '-':
                        Anu += 1
                for j in classes[:,1]:
                    if i != '-':
                        Bnu += 1
                Lnu += mention_data[:,0].sum()
                Mnu += mention_data[:,1].sum()
                Rnu += mention_data[:,2].sum()
                Totnu = Lnu+Mnu+Rnu
                tot_sets_nu = Anu + Bnu
    ps_tup  = (Lps, Mps, Rps, Totps, Aps, Bps, tot_sets_ps)
    nu_tup = (Lnu, Mnu, Rnu, Totnu, Anu, Bnu, tot_sets_nu)
    
    return ps_tup, nu_tup

def print_total(name):
    '''
    Takes as input a txt .iaa file, tab separated.
    Accumulates the coref differences per file
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