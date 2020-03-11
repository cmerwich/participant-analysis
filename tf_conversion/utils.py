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

'''
This dict and set contain paradigmatic forms of the pronominal suffix (Hebrew and Aramaic) and converts it to a readable form
'''

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
