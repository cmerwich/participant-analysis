import getopt
import os, sys
from sys import argv, exit, stderr
import re
from pprint import pprint
from collections import OrderedDict
from operator import attrgetter

PATTERN = re.compile('[0-9]{2}|_\|')
TAB = '\t'
NL = '\n'

class Mention:
    def __init__(self, name, start=0, end=0, lex='', note='', file=0):
        self.name = name    # Identifier of the mention, e.g. T32
        self.start = start  # Start of the position in the file
        self.end = end      # End of the position in the file
        self.lex = lex      # Lexical information
        self.note = note    # AnnotatorNotes
        self.file = file    # Index of the file to which it is to be written
        
def error(*args, **kwargs):
    print(*args, file=stderr, **kwargs)
    exit(1)
    
    
def Usage():
    stderr.write('usage: declust -a input.ann input.txt...\n')
    exit(1)
    
def GetOffsetsAnn(chapter_text):
    
    i = 0
    ann_txt_list = []
    with open(chapter_text) as fh:
        for (ln, line) in enumerate(fh):
            match = PATTERN.finditer(line)
            for character in line:
                i += 1
                for m in match:
                    # filter out psalms title on line 0, 
                    # and (0, 2) for verse numbers with two digits or more
                    if ln != 0 and m.span() != (0, 2):
                        ann_txt_list.append(i+m.start())
                                          
    return ann_txt_list

def GetOffsetsMimi(chapter_text):
    
    i = 0
    mimi_txt_list = []
    
    with open(chapter_text) as fh:
        for (ln, line) in enumerate(fh):
            firstChar = line[0]
            for character in line: 
                i += 1
                if character in {'+', '-'}:
                    mimi_txt_list.append(i-1)
               
    return mimi_txt_list

def Merge(ann_txt_list, mimi_txt_list):
    d = {}
    for i in ann_txt_list:
        d[i] = -2
    for e in mimi_txt_list:
        d[e] = 1
    od = OrderedDict(sorted(d.items()))
    return od

def MakeOffsets(od):
    offset = 0
    jumps_list = []
    for k, v in od.items():
        point = k + (offset if v == 1 else 0)
        offset += v
        jumps_list.append((point, offset))
    return jumps_list

def find_index(jumps_list, coor):
    i = 0
    while jumps_list[i+1][0] < coor:
        i += 1
    return i

def TranslateIndex(jumps_list, mentions): 
    for m in mentions: 
        i = find_index(jumps_list, m.start)
        print('i: ', i, 't0 ', jumps_list[i][0], 't1 ', jumps_list[i][1])
        if m.start == jumps_list[i][0]:
            m.start = m.start + jumps_list[i][1]
            m.end = m.end + jumps_list[i][1]
            
def Parse(ann_file, jumps_list):
    '''
    Parses a plain text annotation file per Bible Book chapter 
    (e.g. Psalms 001) that has been annotated for coreference information.
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

    with open(ann_file) as fh:
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
                start = int(aStart)
                end = int(aEnd)
                # adjust mention start and end indices for iaa analysis 
                #theStart, theEnd = TranslateIndex(jumps_list, start, end)
                #theStart = TranslateIndex(jumps_list, start)
                #theEnd = TranslateIndex(jumps_list, end)
                t2mDict[tPart] = mentionStr
                m = Mention(tPart, start, end, aWord)
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

def OpenAnn(path):
    '''
    Opens an annotation file with extension `.ann' for each chapter
    in current folder. 
    '''
    
    filename_w_ext = os.path.basename(path)
    filename, file_extension = os.path.splitext(filename_w_ext)
    filename_ann = f'{filename}_n{file_extension}'
    ann_file = open(filename_ann, 'w')
    
    return ann_file

def WriteMentions(mentions, ann_file):
    '''
    Writes the mentions and annotatornotes on mentions to the corresponding ann file. 
    '''
    
    i = 0
    sorted_mentions = sorted(mentions, key=attrgetter('start'))
    for m in sorted_mentions:
        ann_file.write(f'{m.name}{TAB}Mention {str(m.start)} {str(m.end)}{TAB}{m.lex}{NL}')
        
        if m.note != '':
            i += 1
            ann_file.write(f'#{str(i)}{TAB}AnnotatorNotes {m.name}{TAB}{m.note}{NL}')

def WriteCorefs(corefs, ann_file):
    '''
    Writes a coref class with mentions to .ann file object.
    '''
    
    for c in corefs:
        ann_file.write(f'*{TAB}Coreference')
        sorted_corefs = sorted(c, key=attrgetter('start'))
        for m in sorted_corefs:
            ann_file.write(f' {m.name}') 
        ann_file.write('\n')

def Close(file): 
    '''
    Close ann file object.
    '''
    
    file.close()

def Translate(ann_txt, mimi_txt, ann_file):
    # ann_txt: path to ann txt files
    # mimi_txt = path to mimi txt files 
    # ann_file = path to (chris) ann_file
    
    ann_offsets = GetOffsetsAnn(ann_txt)
    mimi_offsets = GetOffsetsMimi(mimi_txt)
    ordered_dict = Merge(ann_offsets, mimi_offsets)
    jumps_list = MakeOffsets(ordered_dict)
    pprint(jumps_list)
    Mentions, Corefs = Parse(ann_file, jumps_list)
    TranslateIndex(jumps_list, Mentions)
    new_ann_file = OpenAnn(ann_file)
    WriteMentions(Mentions, new_ann_file)
    WriteCorefs(Corefs, new_ann_file)
    Close(new_ann_file)
    
    
#Translate('Psalms_002-ann.txt', 'Psalms_002-mimi.txt', 'Psalms_002.ann')