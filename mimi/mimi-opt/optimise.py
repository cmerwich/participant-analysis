from functools import lru_cache
import subprocess

import numpy as np
import math
from scipy.optimize import minimize, linear_sum_assignment
from translate import translate
from mimi import mimi

CHRIS_DIR = os.path.expanduser('~/Sites/brat/data/coref/Psalms/annotate')
MIMI_DIR = os.path.expanduser('~/github/cmerwich/participant-analysis/mimi/mimi-opt')

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
    
    results_array = np.array(results_list)

    return results_array

def ds(s1, s2):
    ''' 
    Return the L, M, R triple on which the Jaccard distance between
    the sets s1 and s2 is based.
    '''
    return (len(s1 - s2), len(s1 & s2), len(s2 - s1))

def d_nk(l1, l2):
    '''
    Return the distance between two lists of sets,
    provided that n >= k 
    '''
    n = len(l1)
    k = len(l2)
    lost = np.zeros((n, n), dtype=int)
    held = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(k):
            L, M, R = ds(l1[i], l2[j])
            lost[i, j] = L + R
            held[i, j] = M
        for j in range(k, n):
            lost[i, j] = len(l1[i])
            held[i, j] = 0
    rx, cx = linear_sum_assignment(lost)
    l = lost[rx, cx].sum()
    h = held[rx, cx].sum()
    # l / (l + h) distance per text
    return l, h

def dc(l1, l2):
    '''
    Return the distance between two sets of sets, represented as
    lists of sets. 
    '''
    n = len(l1)
    k = len(l2)
    if n < k:
        return d_nk(l2, l1)
    else:
        return d_nk(l1, l2)

def CompareAnn(pathA, pathB):
    '''
    Executes the comparison between the brat annotation files of annotator A and B.
    '''
    
    annFileA = os.path.expanduser(pathA)
    annFileB = os.path.expanduser(pathB)
    
    results_array_A = parse_ann(annFileA)
    results_array_B = parse_ann(annFileB)
    
    return dc(results_array_A, results_array_B)

def do_translate(book, c):
    ps = f'{book}_{c:>03}'
    mimi_ann = f'{ps}.ann'
    out_ann = f'{ps}_t.ann'
    chris_txt = f'{CHRIS_DIR}/{ps}.txt'
    mimi_txt = f'{ps}.txt'
    translate(mimi_ann, out_ann, [chris_txt, mimi_txt])
    return f'{CHRIS_DIR}/{ps}.ann', out_ann

@lru_cache(maxsize=100)
def distance_from_chris(w, book, from_chapter, to_chapter):
    '''
    w = weight_vector = []
    '''
    r = np.array([0, 0])
    mimi(book, from_chapter, to_chapter, w)
    for c in range(from_chapter, to_chapter +1):
        PATH_A, PATH_B = do_translate(book, c)
        r += CompareAnn(PATH_A, PATH_B)
    print(r, r[0] / sum(r), 'w: ', w)
    return r[0] / sum(r) # distance = l / (l + h)

def wrapper(w, book, from_chapter, to_chapter):
    return distance_from_chris(tuple(w), book, from_chapter, to_chapter)
    
def Optimise(w, book, from_chapter, to_chapter): 
    r = minimize(wrapper, w, 
                 args=(book, from_chapter, to_chapter), 
                 options={'disp': True, 'eps': 0.5} # 5.0, 2.5, 1.0, 0.5, 0.1
                )
    if r.success:
        print(f'Minimum found for w = [{r.x[0]}, {r.x[1]}]')
    else:
        print(f'Minimum not found for w = {w}')

Optimise([2.0, 5.6], 'Psalms', 1, 150)

print(distance_from_chris.cache_info())

# potential functions for text distance
def f1(a, d):
    v = 1 - 1/(1 + a*(d-1))**2
    return v

def f2(a, d):
    v = a * math.log(d)
    return v

def f3(a, d):
    v = math.tanh(a*(d-1))
    return v

print(f'f1: {f1(0.0460237, 10)}', f'f2: {f2(0.217147, 10)}', f'f3: {f2(0.061034, 10)}', sep = '\t')

f2(0.1, 300)