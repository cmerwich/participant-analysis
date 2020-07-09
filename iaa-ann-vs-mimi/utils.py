import os
from sys import argv, stderr
import numpy as np
import pandas as pd

def ExportToLatex(output_loc, file_name, data_frame, indx = True):
    with open(f'{output_loc}{file_name}.tex','w') as texf:
        texf.write(data_frame.to_latex(index=indx))
        
def ParseMentions(path):
    
    errors = 0
    mentions_list = []
    mlist = []
    dataPartsList = []

    firstChars = {'T', '#', '*'}
    cClass = 0
    
    files = [i for i in os.listdir(path) if i.endswith(".ann")]
    
    for file in sorted(files):
        with open(f'{path}/{file}') as fh:
            mentionSet = set()
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
                    mentionSet.add(mentionStr)
                    mentions_list.append(mentionStr)
                    
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
                    
        mlist.append(mentionSet)
        
    if errors:
        error(f'There are {errors} errors in annotation file')
            
    print(len(mentions_list))
    return mentions_list

def error(*args, **kwargs):
    '''
    Prints error messages.
    '''

    print(*args, file=stderr, **kwargs)
    exit(1)

def ParseClasses(path):
    '''
    Parses a plain text brat annotation files for a given repository
    specified in `path`, and returns an np.array of corefs and singletons
    for the total annotated corpus. 
    '''

    errors = 0

    results_list = []
    t2mDict = {}
    singletonSet = set()
    #dataPartsList = []

    firstChars = {'T', '#', '*'}
    cClass = 0

    files = [i for i in os.listdir(path) if i.endswith(".ann")]
    for file in sorted(files):
        dataPartsList = []
        with open(f'{path}/{file}') as fh:
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
    Return the L, M, R triple for the set difference 
    of s1 and s2 (L, R)
    and the intersection of s1 and s2 (M) 
    '''
    return (len(s1 - s2), len(s1 & s2), len(s2 - s1))

def Similarity(c, m):
    n = len(c)
    k = len(m)
    for i in range(n):
        for j in range(k):
            L, M, R = ds(c[i], m[j])
    return L, M, R

def Performance(L, M, R):
    '''
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    '''
    pr = M / (M + R)
    re = M / (M + L)
    f1 = 2 * pr * re / (pr + re)
    print(f"Precision: {round(pr, 2)}, recall: {round(re, 2)}, f1: {round(f1, 2)}")
    return round(pr, 2), round(re, 2), round(f1, 2)