import os

def Parse(path):
    
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