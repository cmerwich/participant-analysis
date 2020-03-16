# call within same repository as: `Translate' (makefile) as: 
# make -f Translate
# translate('Psalms_002-mimi.ann', 'Psalms_002_n.ann', ['Psalms_002-ann.txt', 'Psalms_002-mimi.txt'])

__author__ = 'erwich/sikkel'

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
    stderr.write('usage: translate -a input.ann -o output.ann old.txt new.txt\n')
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
                        ann_txt_list.append((i+m.start(), m.group()))                                    
    return ann_txt_list


def GetOffsetsMimi(chapter_text):
    
    i = 0
    mimi_txt_list = []
    
    with open(chapter_text) as fh:
        for (ln, line) in enumerate(fh):
            firstChar = line[0]
            for character in line: 
                #print(character, i)
                i += 1
                if character in {'+', '-'}:
                    mimi_txt_list.append((i-1, character))
                    
    return mimi_txt_list         

def elision(new, i):
    return new[i][1] == '+' or i > 0 and new[i-1][0] + 1 == new[i][0] and new[i-1][1] == '-'


def Merge(old, new):
    offset = 0
    jumps_list = [(0, 0)]
    
    i_old = 0
    i_new = 0
    in_old = i_old < len(old)
    in_new = i_new < len(new)
    while in_old or in_new:
        if not in_new or (in_old and old[i_old][0] - offset < new[i_new][0]):
            # add old 
            x = old[i_old][0] - offset
            offset += 2
            i_old += 1 
            in_old = i_old < len(old)
        else: 
            # add new
            x = new[i_new][0] + elision(new, i_new)
            offset -= 1
            i_new += 1
            in_new = i_new < len(new)
        jumps_list.append((x, offset))
            
    return jumps_list

def find_index(jumps_list, coor):
    i = 0
    while i + 1 < len(jumps_list) and jumps_list[i+1][0] <= coor:
        i += 1
    return i

def Offset(coor, jumps_list):
    i = find_index(jumps_list, coor)
    return jumps_list[i][1]

def TranslateMentions(mentions, jumps_list):
    for m in mentions:
        m.start += Offset(m.start, jumps_list)
        m.end += Offset(m.end, jumps_list)


def Parse(ann_file):
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
    
    ann_file = open(path, 'w')
    
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


def translate(new_ann, out, texts):
    # new_ann = mimi file.ann
    # out = mimi translated to chris file.ann
    # texts = list[old_file.txt, mimi_file.txt]
    
    old = GetOffsetsAnn(texts[0])
    new = GetOffsetsMimi(texts[1])
    jumps_list = Merge(old, new)
    Mentions, Corefs = Parse(new_ann)
    TranslateMentions(Mentions, jumps_list)
    mimi_ann_file = OpenAnn(out)
    WriteMentions(Mentions, mimi_ann_file)
    WriteCorefs(Corefs, mimi_ann_file)
    Close(mimi_ann_file)


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "a:o:", [])
    except getopt.GetoptError:
        Usage()
    ann = ''
    out = ''
    for opt, arg in opts:
        if opt == '-a':
            ann = arg
        elif opt == '-o':
            out = arg
    if ann == '' or out == '' or len(args) != 2:
        Usage()
    else:
        translate(ann, out, args)

if __name__ == "__main__":
    main(argv[1:])