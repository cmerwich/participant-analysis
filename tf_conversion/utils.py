def known(s):
    '''
    See function converse_pgn.
    '''
    
    if s == 'unknown':
        return 'u'
    elif s == 'NA':
        return ''
    else:
        return s

def converse_pgn(F, w):
    '''
    Concatenates features ps, gn, nu into one PGN property. Calls the function 'known' to check for unknown PGN first. 
    '''
    pgn = ''
    pgn += known(str(F.ps.v(w)))
    pgn += known(str(F.gn.v(w)))
    pgn += known(str(F.nu.v(w)))
    return pgn

def converse_pgn_suffix(sf):
    '''
    Concatenates features ps, gn, nu into one PGN property. 
    '''
    pgn = suffix_dict.get(sf, None)
    if pgn is None:
        return '-MISTAKE?' # the none returns are mostly and probably annotation mistakes
    return pgn[0]

def ExportToLatex(output_loc, file_name, data_frame, indx = True):
    with open(f'{output_loc}{file_name}.tex','w') as texf:
        texf.write(data_frame.to_latex(index=indx))

'''
This dict and set contain readable forms of Person, Gender and Number (PGN) information of the verb
'''

pgn_dict = {'p1upl': ['P1Cpl', 'We'],
             'p1usg': ['P1Csg', 'I'],
             'p2fpl': ['P2Fpl', 'You'],
             'p2fsg': ['P2Fsg', 'You'],
             'p2mpl': ['P2Mpl', 'You'],
             'p2msg': ['P2Msg' ,'You'],
             'p3fpl': ['P3Fpl', 'They'],
             'p3fsg': ['P3Fsg', 'She'],
             'p3mpl': ['P3Mpl', 'They'],
             'p3msg': ['P3Msg', 'He'],
             'p3upl': ['P3Cpl', 'They'],
             'ufpl': ['UFpl', 'They'],
             'ufsg': ['UFsg', 'She'],
             'umpl': ['UMpl', 'They'],
             'umsg': ['UMsg', 'He'],
             'uuu': ['UUU', 'U']
            }

pgn_set = {'P1Cpl',
           'P1Csg',
           'P2Fpl',
           'P2Fsg',
           'P2Mpl',
           'P2Msg',
           'P3Cpl',
           'P3Fpl',
           'P3Fsg',
           'P3Mpl',
           'P3Msg',
           'UFpl',
           'UFsg',
           'UMpl',
           'UMsg',
           'UUU'}


'''
This dict and set contain paradigmatic forms of the pronominal suffix (Hebrew and Aramaic) and converts it to a readable form
'''

suffix_dict_c = {'NJ': ['P1Csg','i'],
               'J': ['P1Csg', 'i'],
               'NW': ['P1Cpl', 'we'],
               'K': ['P2Msg', 'you'],
               'K=': ['P2Fsg', 'you'],
               'KM': ['P2Mpl', 'you'],
               'KN': ['P2Fpl', 'you'],
               'W': ['P3Msg', 'he'],
               'HW': ['P3Msg', 'he'],
               'H': ['P3Fsg', 'she'],
               'HM': ['P3Mpl', 'they'],
               'M': ['P3Mpl', 'they'],
               'MW': ['P3Mpl', 'they'],            
               'HN': ['P3Fpl', 'they'],
               'N': ['P3Fpl', 'they'],
               'HJ': ['P3Msg', 'he'],
               'H=': ['P3Fsg', 'she'],
               'KWN': ['P2Mpl', 'you'],
               'HWN': ['P3Mpl', 'they'],
               'N>': ['P1Cpl', 'we']
              }

suffix_dict = {'NJ': ['p1usg','i'],
               'J': ['p1usg', 'i'],
               'NW': ['p1upl', 'we'],
               'K': ['p2msg', 'you'],
               'K=': ['p2fsg', 'you'],
               'KM': ['p2mpl', 'you'],
               'KN': ['p2fpl', 'you'],
               'W': ['p3msg', 'he'],
               'HW': ['p3msg', 'he'],
               'H': ['p3fsg', 'she'],
               'HM': ['p3mpl', 'they'],
               'M': ['p3mpl', 'they'],
               'MW': ['p3mpl', 'they'],            
               'HN': ['p3fpl', 'they'],
               'N': ['p3fpl', 'they'],
               'HJ': ['p3msg', 'he'],
               'H=': ['p3fsg', 'she'],
               'KWN': ['p2mpl', 'you'],
               'HWN': ['p3mpl', 'they'],
               'N>': ['p1upl', 'we']
              }


prs_set = {'P1Cpl',
          'P1Csg',
          'P2Fpl',
          'P2Fsg',
          'P2Mpl',
          'P2Msg',
          'P3Fpl',
          'P3Fsg',
          'P3Mpl',
          'P3Msg'}


'''
This dict and set contain paradigmatic forms of the personal pronoun (Hebrew) and converts it to a readable form
'''

prps_dict = {'>NXNW': ['P1Cpl', 'we'],
             '>NJ': ['P1Csg', 'i'],
             '>NKJ': ['P1Csg', 'i'],
             '>T=': ['P2Fsg', 'you'],
             '>TH': ['P2Msg', 'you'],
             '>TM': ['P2Mpl', 'you'],
             '>TN': ['P2Fpl', 'you'],
             '>TNH': ['P2Fpl', 'you'],
             'HW>': ['P3Msg', 'he'],
             'HJ>': ['P3Fsg', 'she'],
             'HM': ['P3Mpl', 'they'],
             'HMH': ['P3Mpl', 'they'],
             'HNH=': ['P3Fpl', 'they'],
            }

prps_set = {'P1Cpl',
           'P1Csg',
           'P2Fpl',
           'P2Fsg',
           'P2Mpl',
           'P2Msg',
           'P3Fpl',
           'P3Fsg',
           'P3Mpl',
           'P3Msg'}


'''
This dict and set contain paradigmatic forms of the demonstrative pronoun (Hebrew) and converts it to a readable form
'''
 
prde_dict = {'>L===': ['Cpl-1', 'these'],
             '>LH': ['Cpl-2', 'these'], 
             'Z>T': ['Fsg-1', 'this'],
             'ZH': ['Msg-1', 'this'],
             'ZH=': ['Fsg-2', 'this'],
             'ZW=': ['Fsg-3', 'this'],
             'LZ': ['Csg', 'thisthere'],
             'LZH': ['Msg', 'thisthere'],
             'LZW': ['Fsg', 'thisthere']
            }

prde_set = {'Cpl-1', 'Cpl-2', 'Csg', 'Fsg', 'Fsg-1', 'Fsg-2', 'Fsg-3', 'Msg', 'Msg-1'}


'''
This set contains all unique possible forms of pgn, suffix, prs, prps and prde.
'''

all_pgn_set = {'Cpl-1', 'P2Msg', 'Msg-1', 'UUU', 'P2Fpl', 'Msg', 'P3Fsg', 'P1Cpl', 'P2Fsg', 'UFsg', 'P3Msg', 'Fsg-1', 'Cpl-2', 'Csg', 'Fsg', 'P1Csg', 'P2Mpl', 'Fsg-3', 'Fsg-2', 'UMpl', 'P3Fpl', 'P3Mpl', 'UFpl', 'UMsg', 'P3Cpl'}
