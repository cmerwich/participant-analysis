__author__ = 'erwich/sikkel'

import os

from sys import argv, stderr

import numpy as np
from scipy.optimize import linear_sum_assignment

def error(*args, **kwargs):
    '''
    Prints error messages.
    '''

    print(*args, file=stderr, **kwargs)
    exit(1)

def parse_ann(annFile):
    '''
    Parses a plain text brat annotation file for a given repository
    specified in `compare_ann()`, and returns an np.array of corefs and singletons
    '''

    errors = 0

    results_list = []
    t2mDict = {}
    singletonSet = set()
    dataPartsList = []

    firstChars = {'T', '#', '*'}
    cClass = 0

    with open(annFile) as fh:
        for (i, line) in enumerate(fh):
            epos = f'{i + 1} '
            line = line.rstrip('\n')
            firstChar = line[0]

            if firstChar not in firstChars:
                error(f'{epos}Unrecognized line "{line}"')
                errors +=1
                continue

            numFields = 2 if firstChar =='*' else 3
            parts = line.split('\t')

            if len(parts) != numFields:
                error(f'{epos}line does not have exactly {numFields} parts: "{line}"')
                errors += 1
                continue

            if firstChar == 'T':
                (tPart, mentionStr, aWord) = parts
                mParts = mentionStr.split()
                if len(mParts) != 3:
                    error(f'{epos}T-line mention does not have exactly 3 parts: "{line}"')
                    errors += 1
                    continue
                t2mDict[tPart] = mentionStr
                singletonSet.add(mentionStr)

            elif firstChar == '*':
                corefSets = set()
                (char, data) = parts
                dataParts = data.split()
                if len(dataParts) <= 1 or dataParts[0] != 'Coreference':
                    error(f'{epos}*-line spec does not have the right parts: "{line}"')
                    errors += 1
                    continue
                cClass += 1
                dataPartsList.append(dataParts)
        
        for l in dataPartsList:
            corefSets = set()
            for tPart in l[1:]:
                if tPart in corefSets:
                    error(f'{epos}*-"{tPart} occurs in multiple classes "{corefSets[tPart]}" in "{line}"')
                    errors += 1
                    continue
                corefSets.add(t2mDict[tPart])
                singletonSet.discard(t2mDict[tPart])
            
            results_list.append(corefSets)
        
        results_list.append(singletonSet) #results_list[-1] is the singletonSet
    
    if errors:
        error(f'There are {errors} errors in annotation file')    
    
    #print(f'There are {cClass} coreference classes and {len(singletonSet)} singletons in specified annotation file(s)\n')
    
    results_array = np.array(results_list)

    return results_array

def f(V, s):
    r = 0
    for e in s:
        r += len(V[e])
    return r

def distance(A, B, i, j):
    return len(A[i]^B[j])
    
def match(A, B, d):
    '''
    Matches the nodes in a bipartite graph with n and k nodes using the
    distance function d(i,j) and stores the matching in array r.
    The unpaired corefs are calculated by f().
    '''

    n = len(A)
    k = len(B)
    cost = np.zeros((n, k))
    
    for i in range(n):
        for j in range(k):
            cost[i, j] = d(A, B, i, j)
    row_ind, col_ind = linear_sum_assignment(cost)
    unpaired_A = f(A, set(range(n)) - set(row_ind))
    unpaired_B = f(B, set(range(k)) - set(col_ind))
    total_cost = cost[row_ind, col_ind].sum() + unpaired_A + unpaired_B
    uA = set(range(n)) - set(row_ind)
    uB = set(range(k)) - set(col_ind)
    
    return total_cost.sum(), row_ind, col_ind, uA, uB

def make_r(B):
    '''
    Makes an array of zero's with the length of array B.
    '''
    
    r = np.zeros(len(B), dtype=int)
    return r

def tag(S, i):
    '''
    Tags the compared sets according to their types.
    C for coreference class.
    S for singletons.
    '''
    
    if i + 1 == len(S):
        return 'S'
    else:
        return f'C{i+1}'

def print_set_distance(sA, tagA, sB, tagB):
    '''
    Prints the paired and unpaired coref sets of annotator A and B.
    Returns the difference (Left, Right),
    intersection (M), symmetric difference (D) and delta() (d) of two sets. 
    '''
    L = len(sA-sB)
    M = len(sA&sB)
    R = len(sB-sA)
    D = L + R
    d = round(D/(L+M+R),4)
    print(tagA, tagB, L, M, R, D, d, sep='\t')
    
def compare_corefs(A, B, uA, rx, cx, uB):
    for i in range(len(rx)):
        print_set_distance(A[rx[i]], tag(A, rx[i]), B[cx[i]], tag(B, cx[i]))
    for i in uA:
        print_set_distance(A[i], tag(A, i), set(), '-')
    for i in uB:
        print_set_distance(set(), '-', B[i], tag(B, i))

def compare_ann(pathA, pathB):
    '''
    Executes the comparison between the brat annotation files of annotator A and B.
    '''
    
    annFileA = os.path.expanduser(pathA)
    annFileB = os.path.expanduser(pathB)
    
    results_array_A = parse_ann(annFileA)
    results_array_B = parse_ann(annFileB)
    
    make_r(results_array_B)
    cost, rx, cx, uA, uB = match(results_array_A, results_array_B, distance)
    
    compare_corefs(results_array_A, results_array_B, uA, rx, cx, uB)
    
if __name__ == "__main__":
    compare_ann(argv[1], argv[2])
