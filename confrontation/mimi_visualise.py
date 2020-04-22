import pandas as pd
from operator import attrgetter
from tf.app import use
from tf.fabric import Fabric

VERSION = 'c'

A = use('bhsa', 
        version = VERSION,
        hoist=globals(),
        silent=True
       )
TF.load('g_prs', add=True)

def PrintCoref(Corefs):
    '''
    Visualises the coreference classes that MiMi has detected. 
    `Corefs` is a list of coreference sets and singleton sets. 
    The coreference sets contain mentions, that are stored in 
    the class `Mention`.
    '''
    
    i = 0 
    classes = []
    print( 'verse', 'id', 'mention', 'txttyp', '§', 'p', 'g', 'n', 'func', 'type', 'gloss', sep='\t', end='\n\n')
    for s in Corefs:
        if len(s) > 1:
            i+=1
            classes = sorted(s, key=attrgetter('node_tuple'))
            who = [m.who for m in classes if m.who != '']
            where = [T.sectionFromNode(m.node_tuple[0]) for m in classes]
            print(f'C{where[0][1]}:{i}', f'Who: {who[0]}', end='\n')
           
            for m in classes:
                which_verse = T.sectionFromNode(m.node_tuple[0])
                gloss = F.gloss.v(L.u(m.node_tuple[0], 'lex')[0]) if not m.issuffix else ''
                print(which_verse[2], m.name, m.text, m.txttype, m.pargr, m.person, m.gender, 
                      m.number, m.function, m.rpt, gloss,
                  sep='\t', end='\n')
            print('class: ', classes)
            print('\n')

def PrintMentions(Mentions, s):
    '''
    Visualises the singletons or mentions that MiMi has detected. 
    `Mentions` is a list of mention objects. 
    `s` is optional: if given an empty string '' the function
    will print mentions in tabular form, if given `singletons`
    it will print singletons. 
    '''

    sing_list = []
    sing_overview_df = pd.DataFrame()
    i = 0
    
    print('verse', 'C/S', 'who', 'id', 'mention', 'txttyp', '§', 'p', 'g', 'n', 'func', 'type', 'gloss',
          sep='\t', end='\n\n')
    for m in Mentions:
        gloss = F.gloss.v(L.u(m.node_tuple[0], 'lex')[0]) if not m.issuffix else ''
        which_verse = T.sectionFromNode(m.node_tuple[0])
        if s == '':
            if len(m.corefclass) > 1:
                i+=1
                print(which_verse[2], 'C', m.who, m.name, m.text, m.txttype, m.pargr, m.person, m.gender, 
                      m.number, m.function, m.rpt, gloss,
                      sep='\t')
            else:
                print(which_verse[2], '', '', m.name, m.text, m.txttype, m.pargr, m.person, m.gender, 
                  m.number, m.function, m.rpt, gloss,
                  sep='\t')
                
        elif s == 'singletons':
            if len(m.corefclass) == 1:
                i+=1
                print(which_verse[2], f'S{i}', '', m.name, m.text, m.txttype, m.pargr, m.person, m.gender, 
                      m.number, m.function, m.rpt, gloss,
                      sep='\t')

                sing_list.append({'v': which_verse[2],
                            'S#' : f'S{i}',
                            'id' : m.name,
                            'mention' : m.text,
                            'txt' : m.txttype, 
                            '§' : m.pargr, 
                            'p' : m.person, 
                            'g' : m.gender,
                            'n': m.number,
                            'func' : m.function,
                            'type' : m.rpt,
                            'gloss' : gloss
                            })
    
            sing_overview_df = pd.DataFrame(sing_list)
            sing_overview_df = sing_overview_df[['v', 'S#', 'id', 'mention', 
                                                 'txt', '§', 'p', 'g', 'n', 
                                                'func', 'type', 'gloss']]
    return sing_overview_df