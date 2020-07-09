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
    
    results_array = np.array(results_list)

    return results_array

def ds(s1, s2):
    ''' 
    Return the L, M, R triple on which the Jaccard distance between
    the sets s1 and s2 is based.
    '''
    return (len(s1 - s2), len(s1 & s2), len(s2 - s1))

def match_nk(l1, l2):
    '''
    Return the distance between two lists of sets,
    provided that n >= k 
    '''
    n = len(l1)
    k = len(l2)
    lost = np.zeros((n, n), dtype=int)
    held = np.zeros((n, n), dtype=tuple)
    #held = matrix of tuples(l, m, r)
    for i in range(n):
        for j in range(k):
            L, M, R = ds(l1[i], l2[j])
            lost[i, j] = L + R
            held[i, j] = (L, M, R)
        for j in range(k, n):
            L, M, R = (len(l1[i]), 0, 0) # unpaired
            lost[i, j] = L + R
            held[i, j] = (L, M, R)
    rx, cx = linear_sum_assignment(lost)
    scores = held[rx, cx]
    return scores, rx, cx

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
    
def make_tags(list1, list2, rx, cx):
    '''
    Makes class and singleton tags per matching. 
    Returns list of tuples with two elements:
    tag1 for list1, tag2 for list2. 
    [(tag1, tag2)]
    '''
    tags = [] 
    n = len(list1) # array A
    k = len(list2) # array B
    
    for i in range(n):
        if cx[i] < k:
            tags.append((tag(list1, rx[i]), tag(list2, cx[i])))
        else:
            tags.append((tag(list1, rx[i]), '-'))
    return tags
    
def match(l1, l2):
    '''
    Returns the comparison between two sets of sets, 
    represented as lists of sets, in the form of a 
    list of matched tags, and a list of scores per coref. 
    '''
    n = len(l1) # array A
    k = len(l2) # array B
    if n < k:
        scores, rx, cx = match_nk(l2, l1)  #(b, a)
        tags = make_tags(l2, l1, rx, cx)
        scores = [t[::-1] for t in scores]
        tags = [t[::-1] for t in tags]
    else:
        scores, rx, cx = match_nk(l1, l2)  #(a, b)
        tags = make_tags(l1, l2, rx, cx)
        
    return tags, scores

def write_results(tags, scores):
    # tags = [(), ()]
    # scores = [(l, m, r), ()]
    for i in range(len(tags)):
        t = tags[i]
        l, m, r = scores[i]
        D = l + r
        d = round(D / (l + m + r), 4)
        print(t[0], t[1], l, m, r, D, d, sep='\t')

def compare_ann(pathA, pathB):
    '''
    Executes the comparison between the brat annotation files 
    of annotator A and B per chapter. 
    Writes to standard output. 
    '''
    
    annFileA = os.path.expanduser(pathA)
    annFileB = os.path.expanduser(pathB)
    
    results_array_A = parse_ann(annFileA)
    results_array_B = parse_ann(annFileB)
    
    tags, scores = match(results_array_A, results_array_B)
    write_results(tags, scores)
    
if __name__ == "__main__":
    compare_ann(argv[1], argv[2])
