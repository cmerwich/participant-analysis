# command in terminal is:
# [your python 3 version] declust.py -a [.ann file cluster] [.txt files of Numbers chapters]
# example: python3 declust.py -a Nu22--24.ann Nu22.txt Nu23.txt Nu24.txt
# shorter: python3 declust.py -a Nu22--24.ann Numbers_02[2-4].txt

__author__ = 'erwich/sikkel'

import getopt
import os, sys
from sys import argv, exit, stderr

TAB = '\t'
NL = '\n'

def error(*args, **kwargs):
    print(*args, file=stderr, **kwargs)
    exit(1)
    
def Usage():
    stderr.write('usage: declust -a input.ann input.txt...\n')
    exit(1)
    
class Mention:
    def __init__(self, name, start=0, end=0, lex='', note='', file=0):
        self.name = name    # Identifier of the mention, e.g. T32
        self.start = start  # Start of the position in the file
        self.end = end      # End of the position in the file
        self.lex = lex      # Lexical information
        self.note = note    # AnnotatorNotes
        self.file = file    # Index of the file to which it is to be written
        
def GetOffsets(texts):
    '''
    The offsets of the
    Makes the cumulative sizes of the text files 
    for which the corresponding .ann files are generated.  
    '''
    
    lst = []
    offset = 0
    for f in texts:
        lst += [offset]
        offset += os.stat(f).st_size    # check file size in bytes 
    lst += [offset]
    return lst

def CreateAnns(texts):
    '''
    Makes file list (AnnFileTable) of .ann file objects.
    One .ann file will contain coreference annotations of one Bible book chapter.
    'texts' is a list of strings as pathnames, e.g.:
    ['Numbers_001.txt', 'Numbers_009.txt', 'Numbers_017.txt']. 
    The created .ann files will be filled below in functions:
    RelocateMentions() and RelocateCorefs()
    '''
    
    AnnFileTable = []
    
    for f in texts:
        path = f.replace('.txt', '.ann')
        try:
            file = open(path, 'w')
        except OSError as e:
            errno, strerror = e.args
            print(f'Could not create file: {path}: {strerror}')
            sys.exit()
        AnnFileTable.append(file)
        
    return AnnFileTable

def Parse(annFile):
    '''
    Parses a plain text annotation file of a cluster of Bible Book chapters 
    (e.g. Numbers 1--11) that has been annotated for coreference information.
    Returns a list of lists of coref-mention objects and 
    a list of mention objects. 
    '''
    
    errors = 0
    t2mDict = {}
    Mentions = []
    Corefs = []
    MentionIndexDict = {}
    mentionNote = {}
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
                m = Mention(tPart, aStart, aEnd, aWord)
                MentionIndexDict[tPart] = len(Mentions)
                Mentions.append(m)
                
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
            
            elif firstChar == '#':
                (code, spec, note) = parts
                sParts = spec.split()
                if len(sParts) != 2:
                    error(f'{epos}#-line spec does not have exactly 2 parts: "{line}"')
                    errors += 1
                    continue
                tPart = sParts[1]
                if tPart in MentionIndexDict:
                    Mentions[MentionIndexDict[tPart]].note = note
                else:
                    error(f'Annotatornote "{note}": {tPart}: Mention not found')
                    sys.exit(1)
                
                mentionNote.setdefault(tPart, set()).add(note)
                   
        for l in dataPartsList:
            corefSets = set() # for error analysis 
            corefLists = []
            for tPart in l[1:]:
                if tPart in corefSets:
                    error(f'{epos}*-"{tPart} occurs in multiple classes "{corefSets[tPart]}" in "{line}"')
                    errors += 1
                    continue
                corefSets.add(t2mDict[tPart]) # for error analysis 
                if tPart in MentionIndexDict:
                    corefLists.append(Mentions[MentionIndexDict[tPart]])
                else:
                    error(f'Coref: {tPart}: Mention not found')
                    sys.exit(1)
            Corefs.append(corefLists) # list of lists, one list is one coreference class. 
            
    if errors:
        error(f'There are {errors} errors in annotation file(s)')
    
    return Mentions, Corefs

def WriteCoref(mention_list, file_object):
    '''
    Writes a coref class with mentions to .ann file object.
    '''
    
    file_object.write(f'*{TAB}Coreference')
    for m in mention_list:
        file_object.write(f' {m}')
    file_object.write('\n')
    
def FindIndex(off_sets, coor):
    i = 0
    while off_sets[i+1] < coor:
        i+= 1
    return i

def Reindex(mentions, offsets):
    '''
    Reindexes the start and end indices of the mention boundaries 
    from the .ann cluster files so that they are placed 
    in the right declustered .ann file. 
    '''
    for m in mentions:
        i = FindIndex(offsets, m.start)
        j = FindIndex(offsets, m.end)
        if i != j:
            error(f'Mention {m.name} lies across a file border')
        else:
            m.start -= offsets[i]
            m.end -= offsets[j]
            m.file = i
            
def RelocateMentions(mentions, file_table):
    '''
    Relocates the mentions and annotatornotes on mentions to the corresponding ann file. 
    '''
    
    i = 0
    for m in mentions:
        file_table[m.file].write(f'{m.name}{TAB}Mention {str(m.start)} {str(m.end)}{TAB}{m.lex}{NL}')
        
        if m.note != '':
            i += 1
            file_table[m.file].write(f'#{str(i)}{TAB}AnnotatorNotes {m.name}{TAB}{m.note}{NL}')
            
def RelocateCorefs(corefs, file_table):
    '''
    Creates a 'table' with an empty list of mentions 
    for each *.ann file to be written.
    Relocates the mentions to the ann file 
    in which the Mention.name occurs. 
    'table[i]' is a list with Mention.names.
    '''
   
    for c in corefs:
        table = []
        for i in range(len(file_table)):
            table.append([])   
        for m in c:
            table[m.file].append(m.name)
        for i in range(len(table)):
            if len(table[i]) > 1:
                WriteCoref(table[i], file_table[i])

def CloseAnns(AnnFileTable): 
    '''
    Close all ann file objects.
    '''
    
    for file in AnnFileTable:
        file.close()
        
def decluster(ann, texts):
    Offsets = GetOffsets(texts)
    AnnFileTable = CreateAnns(texts)
    Mentions, Corefs = Parse(ann) 
    Reindex(Mentions, Offsets)
    RelocateMentions(Mentions, AnnFileTable)
    RelocateCorefs(Corefs, AnnFileTable)
    CloseAnns(AnnFileTable)
    
def main(argv):
    try:
        opts, args = getopt.getopt(argv, "a:", [])
    except getopt.GetoptError:
        Usage()
    ann = ''
    for opt, arg in opts:
        if opt == '-a':
            ann = arg
    if ann == '' or len(args) == 0:
        Usage()
    else:
        decluster(ann, args)

if __name__ == "__main__":
    main(argv[1:])
