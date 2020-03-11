from utils import converse_pgn, suffix_dict

from tf.app import use
from tf.fabric import Fabric

A = use(
    'bhsa', version='2017',
    mod=(
        'cmerwich/participant-analysis/coreference/tf:clone,'
        'etcbc/bh-reference-system/tf:clone'
    ), 
    hoist=globals(),
    silent=True)

# All searches in the following functions are done with capitalised transliterated Hebrew
# See: https://annotation.github.io/text-fabric/Writing/Hebrew/

def GetPatterns(i, lst, c, k, suffix_errors, who):

    bad_words = [e[2] for e in suffix_errors]
    if c.id != 'Singletons':
        if c.id in who:# and c.first().surface == pgn:
            i+=1
            print(f'C{k} Who: {c.id}, first: {c.first().surface}, type: {c.first().typ}, corpus class: {i}', 
                  end='\n\n')
            print('verse', 'type', 'pgn', 'ann', '', 'gloss', 'note', sep='\t', end='\n')
            lst.append(f'C{k}')
            pattern_list = []
            for m in c.terms:
                gloss = F.gloss.v(L.u(m.start, 'lex')[0])
                book, chapter, verse = T.sectionFromNode(m.start)
                
                if m.typ in {'VP', 'PPrP'} and not m.isSuffix:
                    pgn = converse_pgn(F, m.start)
                    pattern_list.append(f'{m.typ} {pgn}')
                    print(verse, m.typ, pgn, f'{m.surface}     ', f'{gloss}', m.note, sep='\t', end='\n')
                
                elif m.isSuffix and m.surface in bad_words:
                    print(verse, m.typ, ' ', f'{m.surface}    ', '', f'{gloss}', '!CORRUPT ANN', m.note, sep='\t', end='\n')
                    pattern_list.append(f'Sfx')
                
                elif m.isSuffix:
                    pgn_suffix = suffix_dict[m.surface][0]
                    print(verse, m.typ, pgn_suffix, f'{m.surface}    ','',  '    ', m.note, sep='\t', end='\n')
                    pattern_list.append(f'Sfx {pgn_suffix}')
                
                else:
                    print(verse, m.typ, '', f'{m.surface}     ', f'{gloss}', m.note, sep='\t', end='\n')
                    pattern_list.append(m.typ)
            print('Pattern: ', pattern_list)
            print('\n')
            
def FindWho(cd, suffix_errors, who):
    '''
    Finds classes that are identified as an entity. 
    `who`: is a list that can take multiple strings, e.g. '>LHJM' and '>L' 
    and finds and prints all classes identified as '>LHJM' and '>L'. 
    The actual searching and printing is done with `GetPatterns()`.
    `cd`: a coreference dictionary as parsed by ParseAnnotations()
    in `analyse.py`. 
    `suffix_errors`: a list with potential suffix errors.
    '''
    i = 0
    results_lst = []
    for k in cd:
        if k != 0:
            i+= 1
            GetPatterns(i, results_lst, cd[k], k, suffix_errors, who)
    print('Results: ', len(results_lst))
    return results_lst


def Pattern(i, lst, c, k, suffix_errors, mention_type, pgn_form):
    bad_words = [e[2] for e in suffix_errors]
    
    heading = f'C{k} Who: {c.id}, first: {c.first().surface}, type: {c.first().typ}, corpus class: {i}'
    
    if c.id != 'Singletons':
        if c.first().typ == mention_type and c.first().surface in pgn_form:
            i+=1
            print(heading, end='\n\n')
            print('verse', 'type', 'pgn', 'ann', '', 'gloss', 'note', sep='\t', end='\n')
            lst.append(f'C{k}')
            pattern_list = []
            for m in c.terms:
                gloss = F.gloss.v(L.u(m.start, 'lex')[0])
                book, chapter, verse = T.sectionFromNode(m.start)
                
                if m.isSuffix and m.surface in bad_words:
                    print(verse, m.typ, ' ', f'{m.surface}    ', '', f'{gloss}', '!CORRUPT ANN', m.note, sep='\t', end='\n')
                    pattern_list.append(f'Sfx')
                
                elif m.isSuffix:
                    pgn_suffix = suffix_dict[m.surface][0]
                    print(verse, m.typ, pgn_suffix, f'{m.surface}    ','',  '', m.note, sep='\t', end='\n')
                    pattern_list.append(f'Sfx {pgn_suffix}')
                
                elif not m.isSuffix:
                    det = converse_pgn(F, m.start) if m.typ in {'VP', 'PPrP'} else ''
                    pattern_list.append(f'{m.typ} {det}')
                    print(verse, m.typ, det, f'{m.surface}     ', f'{gloss}', m.note, sep='\t', end='\n')
            print('Pattern: ', pattern_list)
            print('\n')
        
        elif (c.first().typ == mention_type and pgn_form == []) or \
            (c.first().surface in pgn_form and mention_type == ''):
            i+=1
            print(heading, end='\n\n')
            print('verse', 'type', 'pgn', 'ann', '', 'gloss', 'note', sep='\t', end='\n')
            lst.append(f'C{k}')
            pattern_list = []
            for m in c.terms:
                book, chapter, verse = T.sectionFromNode(m.start)
                gloss = F.gloss.v(L.u(m.start, 'lex')[0])
                
                if m.isSuffix and m.surface in bad_words:
                    print(verse, m.typ, ' ', f'{m.surface}    ', '', f'{gloss}', '!CORRUPT ANN', m.note, sep='\t', end='\n')
                    pattern_list.append(f'Sfx')
                
                elif m.isSuffix:
                    pgn_suffix = suffix_dict[m.surface][0]
                    print(verse, m.typ, pgn_suffix, f'{m.surface}    ','',  '    ', m.note, sep='\t', end='\n')
                    pattern_list.append(f'Sfx {pgn_suffix}')
                
                elif not m.isSuffix:
                    det = converse_pgn(F, m.start) if m.typ in {'VP', 'PPrP'} else ''
                    pattern_list.append(f'{m.typ} {det}')
                    print(verse, m.typ, det, f'{m.surface}     ', f'{gloss}', m.note, sep='\t', end='\n')
            print('Pattern: ', pattern_list)
            print('\n')

def FindFirst(cd, suffix_errors, mention_type, pgn):
    '''
    Retrieves classes for a chosen mention_type and or pgn. 
    `mention_type`: is a string, e.g. 'VP' and finds and 
    prints all classes that start with that mention_type. 
    `pgn`: is a list that can take multiple strings of transliterated 
    pgn froms, e.g. P1usg: 'NJ', 'J'. 
    The actual searching and printing is done with `Pattern()`.
    `cd`: a coreference dictionary as parsed by ParseAnnotations()
    `suffix_errors`: a list with potential suffix errors.
    '''
    
    i = 0
    results_lst = []
    for k in cd:
        if k != 0:
            i+= 1
            Pattern(i, results_lst, cd[k], k, suffix_errors, mention_type, pgn)  
    print('Results: ', len(results_lst))
    return results_lst


def Search(i, lst, c, k, suffix_errors, what):
    
    for m in c.terms:
        book, chapter, verse = T.sectionFromNode(m.start)
        gloss = F.gloss.v(L.u(m.start, 'lex')[0])
        if c.id != 'Singletons':
            book, chapter, verse = T.sectionFromNode(m.start)
            gloss = F.gloss.v(L.u(m.start, 'lex')[0])
            if m.surface == what:
                det = converse_pgn(F, m.start) if m.typ in {'VP', 'PPrP'} else ''
                lst.append(f'C{k}')
                print(f'{chapter}:{verse}', f'C{k}', m.typ, det, m.surface, '', gloss, m.note, sep='\t', end='\n')
        else:
            if m.surface == what:
                det = converse_pgn(F, m.start) if m.typ in {'VP', 'PPrP'} else ''
                lst.append(f'{chapter}:{verse}-Sing')
                print(f'{chapter}:{verse}', 'Sing', m.typ, det, m.surface, '', gloss, m.note, sep='\t', end='\n')


def FindMention(cd, suffix_errors, what):
    '''
    Finds and prints all occurrences, singletons and in classes, 
    of a specified mention in `what`. 
    `what`: is a mention string, e.g. '>SP' (Asaph)
    The actual searching and printing is done with `Search()`.
    `cd`: a coreference dictionary as parsed by ParseAnnotations()
    `suffix_errors`: a list with potential suffix errors.
    '''
    
    i = 0
    results_lst = []
    print('ch:v class/sing', 'type', 'pgn', 'ann', '', 'gloss', 'note', sep='\t', end='\n\n')
    for k in cd:
        if k != 0:
            i+= 1
            Search(i, results_lst, cd[k], k, suffix_errors, what)
        i+=1
        Search(i, results_lst, cd[k], k, suffix_errors, what)
    print('\n')
        
    print('Results: ', len(results_lst))
    return results_lst