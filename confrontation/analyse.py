import os
from sys import exit, stderr
from collections import defaultdict, Counter
from glob import glob
from pprint import pprint
from operator import itemgetter, attrgetter

import pandas as pd

from tf.app import use
from tf.fabric import Fabric
from utils import converse_pgn, suffix_dict

A = use(
    'bhsa', version='2017',
    mod=(
        'cmerwich/participant-analysis/coreference/tf:clone,'
        'cmerwich/bh-reference-system/tf'
    ), 
    hoist=globals(),
    silent=True)

class ValueData:
    def __init__(self, quintuple):
        self.ct = quintuple[0]
        self.seqNum = int(quintuple[1])
        self.isSuffix = quintuple[3] == 's'
        self.wordPart = quintuple[4]
        if quintuple[2] == '':
            self.size = 1
        else:
            self.size = int(quintuple[2])

class Mention:
    def __init__(self, name='', start=0, end=0, surface='', isSuffix = False, size=1):
        self.name = name          # Identifier of the mention, e.g. T32
        self.start = start        # Start of the word position (=node) in the text
        self.end = end            # End of the word position (=node) in the text
        self.surface = surface    # Surface text
        self.note = ''            # AnnotatorNotes
        self.typ = ''             # Reconstructed phrase type 
        self.isSuffix = isSuffix  # Boolean if mention is suffix
        self.size = size          # wordsize of mention
        
    def __str__(self):
        return self.surface 
    
    def __repr__(self):
        return self.surface
        
class Coref:
    def __init__(self):
        self.id = ''
        self.terms = []

    def add(self, term):
        self.terms.append(term)

    def first(self):
        # Dit is niet per se goed, bij nested mentions moet er ook naar
        # t.end gekeken worden  
        #sorteer eerst op t.isSuffix dan op t.start, omdat sorteren op start conservatief is. 
        # want False < True, dus suffix komt na word in tekstvolgorde
        # sorteer of twee keys
        
        #return sorted(self.terms, key=lambda t: t.start)[0] #print first element in list
        
        lst = sorted(self.terms, key=lambda t: t.isSuffix)
        return sorted(lst, key=lambda t: t.start)[0]
    
def error(*args, **kwargs):
    print(*args, file=stderr, **kwargs)
    exit(1)
    
def Get(node, fName):
    '''
    Helper function to parse the mention and coref 
    features stored in TF files in a structured way. 
    '''
    valueStr = Fs(fName).v(node)
    if not valueStr:
        return None
    parts = valueStr.split('|')
    if len(parts) > 2:
        error(f'There are more than 2 parts.')
        
    vd_list = []
    vd_list.append(ValueData(parts[0].split(',')))
    
    if len(parts) > 1:
        vd_list.append(ValueData(parts[1].split(',')))
    else:
        vd_list.append(ValueData(('', '0', '', '', ''))) # make empty tuple
        vd_list[1].isSuffix = not vd_list[0].isSuffix # assign opposite Boolean of isSuffix

    #check for isSuffix
    if vd_list[0].isSuffix: 
        return (vd_list[1], vd_list[0])
    else:
        return (vd_list[0], vd_list[1])
    
    
def FindMentionIndexByName(mention_list, name):
    for i in range(len(mention_list)):
        if mention_list[i].name == name:
            return i
    return None

def UpdateMentionNotes(mention_list, mention_notes):
    notes_list = mention_notes.split("|")
    for note in notes_list:
        (key, value) = note.split("-", 1)
        i = FindMentionIndexByName(mention_list, key)
        mention_list[i].note = value
        
        
def add_mention_to_coref(d, k, m):
    '''
    d = coref dict
    k = key: 0 for singleton, or chapter:classnumber for coreference 
    m = mention
    Check if key is in coref dict.
    '''
    
    if not k in d:
        d[k] = Coref()
    d[k].add(m)

def TexFabricParse(my_book_name, from_chapter, to_chapter):
    suffix_error = []
    coref_dict = {}
    Mentions = []
    singletons = Coref()
    singletons.id = 'Singletons'
    coref_dict[0] = singletons
    
    my_chapters = set(range(from_chapter, to_chapter+1))
    for book in F.otype.s('book'):
        book_name = T.bookName(book)
        
        for chn in L.d(book, 'chapter'):
            chapter = F.chapter.v(chn)
            if (
                (my_book_name and book_name not in my_book_name)
                or 
                (my_chapters and chapter not in my_chapters)
            ):
                continue
            for phrase in L.d(chn, 'phrase'): 
                for word in L.d(phrase, 'word'):
                    phr_atom = L.u(word, 'phrase_atom')[0]
                    pa_words = L.d(phr_atom, 'word')
                    last_word = pa_words[-1]
                    boo, cha, ver = T.sectionFromNode(word)
                    mentions = Get(word, 'mention') #tuple pair
                    mention_notes = F.mentionNote.v(word)
                    c = F.coref.v(word) 
                    mention_list = []
                    if mentions:
                        for i in range(len(mentions)):
                            assert(mentions[i].ct == 'T' or mentions[i].ct == '')
                            name = f'{mentions[i].ct}{mentions[i].seqNum}'
                            
                            #assert(mentions[i].isSuffix == (i == 1))
                            if mentions[i].isSuffix != (i == 1):
                                suffix_error.append((word, f'{cha}:{ver}', mentions[i].wordPart, 
                                                     f'T{mentions[i].seqNum}'))
                            if mentions[i].size == 1:
                                mention_list.append(Mention(name, word, word, mentions[i].wordPart, 
                                                            i == 1, mentions[i].size))
                            else:
                                mention_list.append(Mention(name, word, last_word, mentions[i].wordPart, 
                                                            i == 1, mentions[i].size))
                    
                    if mention_notes:
                        UpdateMentionNotes(mention_list, mention_notes)
          
                    corefs = Get(word, 'coref')
                    if corefs:
                        # check for empty corefs and singletons 
                        for i in range(len(corefs)):
                            if corefs[i].ct == '':
                                continue
                            if corefs[i].ct == 'T':
                                key = 0
                            else:
                                key = f'{chapter}:{corefs[i].seqNum}'
                            add_mention_to_coref(coref_dict, key, mention_list[i])
                            Mentions.append(mention_list[i])
        
    return Mentions, coref_dict, suffix_error

def EnrichMentions(mentions):
    '''
    Takes mention_list and assigns correct 
    phrase atom type (`pa_typ`) to m.typ. 
    - Uses the word node of m.start to retrieve relevant 
    phrase atom information. 
    - If mention node is the same as the phrase atom, 
    then the same `pa_typ` is assigned. 
    - If it is not the same, the m.typ is 
    taken from the phrase dependent part of speech (`pdp`). 
    - reconstructed phrase types (`rpt`) that seem to be wrong,
    i.e. mentions that are `prep` or `adverb` or `art' are stored
    in the list: reconsider_rpt. 
    '''
    
    reconsider_rpt = []
    
    for m in mentions:
        boo, cha, ver = T.sectionFromNode(m.start)
        phr_atom = L.u(m.start, 'phrase_atom')[0]
        pa_typ = F.typ.v(phr_atom)
        pa_text = T.text(phr_atom, fmt='text-trans-plain')
        pa_words = L.d(phr_atom, 'word')
        pdp = F.pdp.v(m.start)
        vt = F.vt.v(m.start)#'ptca'
        
        if m.isSuffix:
            m.typ = 'Sffx'
        # if mention nodes are the same as phrase atom nodes 
        elif len(pa_words) == 1 and not m.isSuffix:
            m.typ = pa_typ
        
        elif len(pa_words) > 1 and pa_typ == 'NP':
            m.typ = pa_typ
        elif pa_typ == 'VP' and vt == 'ptca':
            m.typ = 'PtcP'
        elif pa_typ == 'VP':
            m.typ = pa_typ
        elif pdp == 'nmpr':
            m.typ = 'PrNP'
        elif pdp == 'subs':
            m.typ = 'NP'
        elif pdp == 'prde':
            m.typ = 'DPrP'
        elif pdp == 'prps':
            m.typ = 'PPrP'
        #reconsider these annotations, stored in reconsider_rpt
        elif pdp == 'adjv':
            m.typ = 'AdjP'  
        else:
            m.typ = pdp
            reconsider_rpt.append((f'{cha}:{ver}', m.start, m.end, m.surface, pdp, pa_words, pa_text, pa_typ))
        #print(m.start, m.end, m.surface, '\t', pdp, m.typ, '\t', (pa_words, pa_text, pa_typ))
    return reconsider_rpt


def FindMentionByRPT(c, typ):
    for m in c.terms:
        if m.typ == typ:
            return m
    
def Identify(c):
    rpt_order = ['PrNP', 'NP', 'PtcP', 'VP', 'PPrP', 'Sffx', 'DPrP']
    for typ in rpt_order:
        m = FindMentionByRPT(c, typ)
        if m:
            c.id = m.surface
            return 
    c.id = c.first()

def AssignIdentity(corefs):
    for key, c in corefs.items():
        if key != 0:
            Identify(c)

def ParseAnnotations(my_book_name, from_chapter, to_chapter):
    mentions, corefs, suffix_errors = TexFabricParse(my_book_name, from_chapter, to_chapter)
    reconsider_rpt = EnrichMentions(mentions)
    AssignIdentity(corefs)
    return mentions, corefs, suffix_errors, reconsider_rpt



def GetOverallData(corefs, mentions):
    overall_dict = Counter()
    
    for k, c in corefs.items():
        if k != 0:
            overall_dict['classes'] += 1
        for m in c.terms:
            if k == 0:
                overall_dict['singletons'] += 1
            overall_dict['mentions'] += 1
    for m in mentions:
        if m.note:
            overall_dict['notes'] += 1
            
    return overall_dict

def GetGraphData(corefs):
    annotation_errors = []
    pos_dict = defaultdict(lambda: defaultdict(int))
    pronoun_dict = defaultdict(lambda: defaultdict(int))
    pronoun_pos_class_dict = defaultdict(lambda: defaultdict(int))
    pronoun_pos_sing_dict = defaultdict(lambda: defaultdict(int))
    
    for k, c in corefs.items():
        if k != 0:
            pos_dict['first in chain'][c.first().typ] += 1     
        for m in c.terms:
            # Not necessary anymore, but left here to make explicit that suffix 
            # is made into a separate mention type
            pa_typ = 'Sffx' if m.isSuffix else m.typ 
            if k != 0:
                pos_dict['in class'][pa_typ] += 1
                if pa_typ in {'VP', 'PPrP'}:
                    if converse_pgn(F, m.start) != '':
                        pronoun_dict['in class'][converse_pgn(F, m.start)] += 1
                        pronoun_pos_class_dict[pa_typ][converse_pgn(F, m.start)] += 1
                elif m.isSuffix:
                    if m.surface not in suffix_dict:
                        annotation_errors.append((k, m.start, m.surface, m.isSuffix))
                    else:
                        pronoun_dict['in class'][suffix_dict[m.surface][0]] += 1
                        pronoun_pos_class_dict[pa_typ][suffix_dict[m.surface][0]] += 1
            else: #'Singletons'
                pos_dict['singleton'][pa_typ] += 1
                if pa_typ in {'VP', 'PPrP'}:
                    if converse_pgn(F, m.start) != '':
                        pronoun_dict['singleton'][converse_pgn(F, m.start)] += 1
                        pronoun_pos_sing_dict[pa_typ][converse_pgn(F, m.start)] += 1
                elif m.isSuffix:
                    if m.surface not in suffix_dict:
                        annotation_errors.append((k, m.start, m.surface, m.isSuffix))
                    else:
                        pronoun_dict['singleton'][suffix_dict[m.surface][0]] += 1
                        pronoun_pos_sing_dict[pa_typ][suffix_dict[m.surface][0]] += 1
            
            pos_dict['total'][pa_typ] += 1
            
    return pos_dict, pronoun_dict, pronoun_pos_class_dict, pronoun_pos_sing_dict

def MakePandasTables(corefs, mentions):
    
    overall_dict = GetOverallData(corefs, mentions) 
    pos_dict, pronoun_dict, pronoun_pos_class_dict, \
    pronoun_pos_sing_dict = GetGraphData(corefs)
     
    overall_df = pd.DataFrame.from_dict(overall_dict, 
                            orient='index',
                            columns = ['total'],
                            ).fillna(0).astype(int).sort_values(
                            by=['total'], ascending=False)
    
    # part of speech for class and singletons data frame
    pos_df = pd.DataFrame.from_dict(pos_dict, 
                                      orient='index', 
                                      ).fillna(0).astype(int)
    
    pos_df = pos_df.sort_values(by=['first in chain', 'in class', 'singleton'], 
                                ascending=False, axis=1)
    
    pos_df['total_type'] = pos_df.sum(axis=1)
    pos_df = pos_df.sort_values(by=['total_type'], ascending=False)
    
                # percentage
    tot_chain = pos_df.loc['first in chain']['total_type']
    tot_chain
    pos_df.loc['% chain',:] = round((pos_df.loc['first in chain',:] / 
                                              tot_chain) * 100)
    tot_tot = pos_df.loc['total']['total_type']
    pos_df.loc['% total',:] = round((pos_df.loc['total',:] / 
                                              tot_tot) * 100)
    pos_df = pos_df.fillna(0).astype(int)
    pos_df = pos_df.reindex(['in class', 'singleton', 'total', '% total', 'first in chain', '% chain'])
    
    
    # pronoun for class and singletons data frame 
    pronoun_df = pd.DataFrame.from_dict(pronoun_dict, 
                                      orient='index',
                                      ).fillna(0).astype(int)
    
    pronoun_df = pronoun_df.reindex(sorted(pronoun_df.columns), axis=1)
    pronoun_df['total_pgn'] = pronoun_df.sum(axis=1)
    pronoun_df = pronoun_df.sort_values(by=['total_pgn'], ascending=False)
                # percentage
    tot_pron = pronoun_df['total_pgn'].sum(axis=0)
    pronoun_df.loc['total',:] = pronoun_df.sum(axis=0)
    pronoun_df.loc['% total',:] = round((pronoun_df.loc['total',:] / tot_pron) * 100)
    
    pronoun_df = pronoun_df.fillna(0).astype(int)
    
    # part of speech and pronouns for class data frame
    pronoun_pos_class_df = pd.DataFrame.from_dict(pronoun_pos_class_dict, 
                                                       orient='index').fillna(0).astype(int)
    pronoun_pos_class_df = pronoun_pos_class_df.reindex(sorted(pronoun_pos_class_df.columns), 
                                                        axis=1)
    pronoun_pos_class_df['total_pgn'] = pronoun_pos_class_df.sum(axis=1)
    pronoun_pos_class_df = pronoun_pos_class_df.sort_values(by=['total_pgn'], 
                                                            ascending=False)
                # percentage
    tot_pronoun_pos_class = pronoun_pos_class_df['total_pgn'].sum(axis=0)
    pronoun_pos_class_df.loc['total',:] = pronoun_pos_class_df.sum(axis=0)
    pronoun_pos_class_df.loc['% total',:] = round((pronoun_pos_class_df.loc['total',:] / 
                                                   tot_pronoun_pos_class) * 100)
    pronoun_pos_class_df = pronoun_pos_class_df.fillna(0).astype(int)
    
    # part of speech and pronouns for singletons data frame
    pronoun_pos_sing_df = pd.DataFrame.from_dict(pronoun_pos_sing_dict, 
                                                       orient='index').fillna(0).astype(int)
    pronoun_pos_sing_df = pronoun_pos_sing_df.reindex(sorted(pronoun_pos_sing_df.columns), 
                                                      axis=1)
    pronoun_pos_sing_df['total_pgn'] = pronoun_pos_sing_df.sum(axis=1)
    pronoun_pos_sing_df = pronoun_pos_sing_df.sort_values(by=['total_pgn'], 
                                                          ascending=False)
                # percentage
    tot_pronoun_pos_sing = pronoun_pos_sing_df['total_pgn'].sum(axis=0)
    pronoun_pos_sing_df.loc['total',:] = pronoun_pos_sing_df.sum(axis=0)
    pronoun_pos_sing_df.loc['% total',:] = round((pronoun_pos_sing_df.loc['total',:] / 
                                                  tot_pronoun_pos_sing) * 100)
    pronoun_pos_sing_df = pronoun_pos_sing_df.fillna(0).astype(int)
    
    
    return overall_df, pos_df, pronoun_df, pronoun_pos_class_df, pronoun_pos_sing_df

#MakePandasTables(coref_dict, mentions_list)

def PrintThisTable(df):
    return df 

def PrintPossibleCorrections(suffix_errors, reconsider_rpt):
    
    if len(suffix_errors) == 0:
        print(f'There are {len(suffix_errors)} annotation errors for the specified corpus', '\n')
    else:
        print(f'There are {len(suffix_errors)} possible annotation errors you may need to reconsider:', '\n')
        print(f'The order is: node, text, lexeme, brat id')  
        for i in suffix_errors:
            print(i, '\n')
    
    if len(reconsider_rpt) == 0:
        print(f'There are {len(reconsider_rpt)} reconstructed phrase type errors for the specified corpus', '\n')
    else:
        print(f'There are {len(reconsider_rpt)} possible erroneous reconstructed phrase types you may need to reconsider:', '\n')
        print(f'The order is: text, start node, end node, lexeme, pdp, (phrase atom nodes), lexeme(s), type')
        for i in reconsider_rpt:
            print(i, '\n')
            
divide = '-'*70

def PrintCorefPattern(c, k, suffix_errors):
    print(f'C{k} Who/what: {c.id} /', end=' ')
    if c.id != 'Singletons':
        print(f'first: {c.first().surface}, type: {c.first().typ}', end='\n')
    print(divide)
    bad_words = [e[2] for e in suffix_errors]
    for m in c.terms:
        if m.typ in {'VP', 'PPrP'} and not m.isSuffix:
            pgn = converse_pgn(F, m.start)
            print(f'{m.surface} -{m.typ} {pgn}', f'{m.note}  ', end=' ')
        
        elif m.isSuffix and m.surface in bad_words:
            print(f'{m.surface} -{m.typ} !CORRUPT ANN', f'{m.note}  ', end=' ')
        
        elif m.isSuffix:
            pgn_suffix = suffix_dict[m.surface][0]
            print(f'{m.surface} -{m.typ} {pgn_suffix}', f'{m.note}  ', end=' ')
        else:
            print(f'{m.surface} -{m.typ}', f'{m.note}  ', end=' ')
    print('\n')

def PrintPatternsAndNotes(cd, suffix_errors):
    for k in cd:
        if k != 0:
            PrintCorefPattern(cd[k], k, suffix_errors)
    PrintCorefPattern(cd[0], '0', suffix_errors)
    
def PrintCorefID(corefs):
    '''
    Print coref class that is sorted 
    by alef-betical order on coref id.
    '''
    
    tr_asc = '#/<=>BCDFGHJKLMNPQRSTVWXYZ_'
    tr_heb = '/=_>BGDHWZXVJKLMNS<PYQRF#CT'
    
    etcbc_table = str.maketrans(tr_heb, tr_asc)
    
    classes = {k:v for (k,v) in corefs.items() if k != 0}
    
    keys = sorted(classes, key=lambda c: classes[c].id.translate(etcbc_table))
    
    for k in keys:
        PrintCoref(classes[k], k)
    #PrintCoref(classes[0], '0')

def PrintCoref(c, k):
    print(f'C{k} Who/what: {c.id} /', end=' ')
    if c.id != 'Singletons':
        print(f'first: {c.first().surface}, type: {c.first().typ}', end='\n')
    print(divide)
    print(c.terms, '\n')

def PrintSurvey(cd):
    for k in cd:
        if k != 0:
            PrintCoref(cd[k], k)
    PrintCoref(cd[0], '0')
    
def ExportToLatex(output_loc, file_name, data_frame, indx = True):
    with open(f'{output_loc}{file_name}.tex','w') as texf:
        texf.write(data_frame.to_latex(index=indx))