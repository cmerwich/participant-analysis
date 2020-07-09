__author__ = 'erwich/sikkel'

import os
from sys import stderr

import numpy as np
from scipy.optimize import linear_sum_assignment
from difflib import ndiff

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
    m2wDict = {}
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
                (mm, aStart, aEnd) = mParts
                aStart = int(aStart)
                aEnd = int(aEnd)
                
                t2mDict[tPart] = mentionStr
                singletonSet.add(mentionStr)
                m2wDict[mentionStr] = aWord

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
    
    results_array = np.array(results_list)

    return results_array, m2wDict

def selection_size(L, s):
    '''
    L is a list of sets, s is a set of indices in L. This function
    returns the total of the cardinalities of the sets selected by s.
    '''
    
    r = 0
    for e in s:
        r += len(L[e])
    return r

#def ds(A, B, i, j):
#    return len(A[i]^B[j])

def distance(s1, s2):
    return (len(s1 - s2), len(s1 & s2), len(s2 - s1))
    
def match(A, B, d):
    '''
    Matches the nodes in a bipartite graph with n and k nodes using the
    distance function d(i,j) and stores the matching in array r.
    The unpaired corefs are calculated by selection_size().
    '''

    n = len(A)
    k = len(B)
    cost = np.zeros((n, k))
    
    for i in range(n):
        for j in range(k):
            (L, M, R) = distance(A[i], B[j])
            cost[i, j] = (L + R) / (L + M + R)
            #cost[i, j] = d(A, B, i, j)
    row_ind, col_ind = linear_sum_assignment(cost)
    unpaired_A = selection_size(A, set(range(n)) - set(row_ind))
    unpaired_B = selection_size(B, set(range(k)) - set(col_ind))
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
    d = round(D/(L+M+R), 4)
    print(tagA, tagB, L, M, R, D, d, sep='\t')
    
def compare_corefs(A, B, uA, rx, cx, uB):
    for i in range(len(rx)):
        print_set_distance(A[rx[i]], tag(A, rx[i]), B[cx[i]], tag(B, cx[i]))
    for i in uA:
        print_set_distance(A[i], tag(A, i), set(), '-')
    for i in uB:
        print_set_distance(set(), '-', B[i], tag(B, i))

def sort_this(l, dic):
    '''
    Sorts a list of mention strings of the form 'Mention 1 5'. 
    Sorts the end index (5), before the start index (1). 
    Returns list of sorted mention strings.
    '''
    
    words_list = []
    l_2 = sorted(l, key=lambda s: int(s.split()[2]))
    l_3 = sorted(l_2, key=lambda s: int(s.split()[1]))
    for i in l_3:
        words_list.append(dic[i])
    
    return words_list
        
def get_ndiff(A, B):
    '''
    Prints the difference between A's and B's annotations 
    which are contained in strings.
    '''
    
    diff_a = []
    diff_b = []
    i_A = 0
    i_B = 0
    
    for s in ndiff(A, B):
        
        #if s[0]==' ': continue # ignore the common annotations of A and B
        if s[0]=='-':
            diff_a.append((s[2:], i_A)) # A.index(s[2:])
            i_A += 1
        elif s[0]=='+': 
            diff_b.append((s[2:], i_B)) # B.index(s[2:])
            i_B += 1
        else:
            i_A += 1
            i_B += 1
        
    if diff_a == diff_b:
        pass
    else:
        print('A diff', diff_a, '\n', sep='\t')
        print('B diff', diff_b, '\n', sep='\t')        

def retrieve_corefs(A, B, uA, rx, cx, uB, m2wDict_A, m2wDict_B):
    divide = '-'*60
    
    print('ann_A','ann_B', 'L', 'M', 'R', 'D', 'd', '\n', sep='\t')
    
    for i in range(len(rx)):
        print(divide)
        print_set_distance(A[rx[i]], tag(A, rx[i]), B[cx[i]], tag(B, cx[i]))
        print(divide)
        
        coList_A = []
        for Ae in A[rx[i]]:
            coList_A.append(Ae)
        A_list = sort_this(coList_A, m2wDict_A)
        print('A', A_list, '\n', sep='\t')
        
        coList_B = []
        for Be in B[cx[i]]:
            coList_B.append(Be)
        B_list = sort_this(coList_B, m2wDict_B)
        print('B', B_list, '\n', sep='\t')
        get_ndiff(A_list, B_list)
    
    for i in uA:
        print(divide)
        print_set_distance(A[i], tag(A, i), set(), '-')
        print(divide)
        
        coList_uA = []
        for uAe in A[i]:
            coList_uA.append(uAe)
        print('unp A', sort_this(coList_uA, m2wDict_A), '\n', sep='\t')
    
    for i in uB:
        print(divide)
        print_set_distance(set(), '-', B[i], tag(B, i))
        print(divide)
        
        coList_uB = []
        for uBe in B[i]:
            coList_uB.append(uBe)
        print('unp B', sort_this(coList_uB, m2wDict_B), '\n', sep='\t')        

def retrieve_ann(pathA, pathB):
    '''
    Executes the comparison between the brat annotation files of annotator A and B.
    '''
    
    annFileA = os.path.expanduser(pathA)
    annFileB = os.path.expanduser(pathB)
    
    results_array_A, m2wDict_A = parse_ann(annFileA)
    results_array_B, m2wDict_B = parse_ann(annFileB)
    
    make_r(results_array_B)
    cost, rx, cx, uA, uB = match(results_array_A, results_array_B, distance)
    
    #compare_corefs(results_array_A, results_array_B, uA, rx, cx, uB)
    
    retrieve_corefs(results_array_A, results_array_B, uA, rx, cx, uB, m2wDict_A, m2wDict_B)