%load_ext autoreload
%autoreload 2

import re
from collections import defaultdict, Counter
from IPython.display import display, HTML
from pprint import pprint
from functools import reduce

import pandas as pd
import matplotlib.pyplot as plt

from tf.app import use

A = use(
    'bhsa', version='c',
    mod=(
        'etcbc/lingo/heads/tf,'
        #'cmerwich/bh-reference-system/tf'
        'etcbc/bh-reference-system/tf:clone'
    ),
    hoist=globals(),
    silent=True
)

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

def CountPgnCategories():
    info(f'Start counting in the Hebrew Bible: \n \
         - all features or categories that contain person, gender and number information.\n \
         - all sorts of person, gender and number information within those features.\n \
         This may take a while... \n\n'
        )
    
    pgn_count = {}
    all_pgn_count = {}

    for book in F.otype.s('book'):
        book_name = T.bookName(book)
        for chn in L.d(book, 'chapter'):
            chapter = F.chapter.v(chn)
            pgn_count[book_name] = defaultdict(int)
            all_pgn_count[book_name] = defaultdict(int)
            for w in L.d(book, 'word'):
                pgn_prps = F.pgn_prps.v(w)
                pgn_prde = F.pgn_prde.v(w)
                pgn_verb = F.pgn_verb.v(w)
                pgn_prs = F.pgn_prs.v(w)
                
                # Count all categories of PGN
                if pgn_prps:
                    pgn_count[book_name]['pgn_prps'] += 1
                if pgn_prde:
                    pgn_count[book_name]['pgn_prde'] += 1
                if pgn_verb:
                    pgn_count[book_name]['pgn_verb'] += 1
                if pgn_prs:
                    pgn_count[book_name]['pgn_prs'] += 1
                
                # Count all sorts of PGN within all PGN categories
                for pgn in all_pgn_set:

                    if pgn == pgn_prps:
                        all_pgn_count[book_name][pgn] += 1
                    elif pgn not in all_pgn_count[book_name]:
                        all_pgn_count[book_name][pgn] = 0 

                    if pgn == pgn_prde:
                        all_pgn_count[book_name][pgn] += 1
                    elif pgn not in all_pgn_count[book_name]:
                        all_pgn_count[book_name][pgn] = 0 

                    if pgn == pgn_verb:
                        all_pgn_count[book_name][pgn] += 1
                    elif pgn not in all_pgn_count[book_name]:
                        all_pgn_count[book_name][pgn] = 0 

                    if pgn == pgn_prs:
                        all_pgn_count[book_name][pgn] += 1
                    elif pgn not in all_pgn_count[book_name]:
                        all_pgn_count[book_name][pgn] = 0
    
    info(f'Done counting features in {len(pgn_count)} books: \n \
                - prps (independent personal pronoun), \n \
                - prde (demonstrative pronoun), \n \
                - verb (person, gender number), \n \
                - and prs (suffix). \n'
        )
    info(f'Done counting all sorts of person, gender and number information within all features in {len(all_pgn_count)}.'
        )
    
    return pgn_count, all_pgn_count

def CountTypPdp(my_book, from_chapter, to_chapter):
    my_chapters = set(range(from_chapter, to_chapter+1))
    phr_typ_count = {}
    phr_typ_pdp_count = {}
    phr_typ_st_count = {}
    
    # Create dictionaries with Phrase Types of Choice
    for phrase in F.otype.s('phrase'):
        typ = F.typ.v(phrase)
        if typ not in {'NegP', 'InrP', 'InjP', 'CP'}:
            phr_typ_count[typ] = defaultdict(int)
            phr_typ_pdp_count[typ] = defaultdict(int)
            phr_typ_st_count[typ] = defaultdict(int)
    
    for book in F.otype.s('book'):
        book_name = T.bookName(book)
        for chn in L.d(book, 'chapter'):
            chapter = F.chapter.v(chn)
            if (
                (my_book and book_name not in my_book)
                or 
                (my_chapters and chapter not in my_chapters)
            ): 
                continue
                
            for phrase in L.d(chn, 'phrase'):
                typ = F.typ.v(phrase)
                det = F.det.v(phrase)

                if typ not in {'NegP', 'InrP', 'InjP', 'CP'}:
                    for w in L.d(phrase, 'word'):
                        pdp = F.pdp.v(w)
                        if pdp:
                            phr_typ_pdp_count[typ][pdp] += 1
    
    return phr_typ_pdp_count

def get_all_pgn():

    pgn_prps_dict = {}
    pgn_prde_dict = {} 
    pgn_verb_dict = {} 
    pgn_prs_dict = {}

    for book in F.otype.s('book'):
        book_name = T.bookName(book)
        pgn_prps_dict[book_name] = defaultdict(int)
        pgn_prde_dict[book_name] = defaultdict(int)
        pgn_verb_dict[book_name] = defaultdict(int)
        pgn_prs_dict[book_name] = defaultdict(int)
        
        for w in L.d(book, 'word'):
            pdp = F.pdp.v(w)
            pgn_prps = F.pgn_prps.v(w)
            pgn_prde = F.pgn_prde.v(w)
            pgn_verb = F.pgn_verb.v(w)
            pgn_prs = F.pgn_prs.v(w)
            pgn_verb_prs = F.pgn_verb_prs.v(w)

            if pgn_prps:

                pgn_prps_dict[book_name][pgn_prps] += 1
                for prps in prps_set:
                    if prps not in pgn_prps_dict[book_name]:
                        pgn_prps_dict[book_name][prps] = 0

            if pgn_prde:

                pgn_prde_dict[book_name][pgn_prde] += 1 
                for prde in prde_set:
                    if prde not in pgn_prde_dict[book_name]:
                        pgn_prde_dict[book_name][prde] = 0     
            elif book_name == 'Nahum':
                for prde in prde_set:
                    pgn_prde_dict[book_name][prde] = 0

            if pgn_verb:

                pgn_verb_dict[book_name][pgn_verb] += 1
                for pgn in pgn_set:
                    if pgn not in pgn_verb_dict[book_name]:
                        pgn_verb_dict[book_name][pgn] = 0

            if pgn_prs:

                pgn_prs_dict[book_name][pgn_prs] += 1
                for prs in prs_set:
                    if prs not in pgn_prs_dict[book_name]:
                        pgn_prs_dict[book_name][prs] = 0
    
    return pgn_prps_dict, pgn_prde_dict, pgn_verb_dict, pgn_prs_dict

def CountVersesWords():

    info('Counting all verses and words per book in the Hebrew Bible')

    object_count_dict = {}

    for book in F.otype.s('book'):
        book_name = T.bookName(book)
        object_count_dict[book_name] = defaultdict(int)

        for verse in L.d(book, 'verse'):
            object_count_dict[book_name]['verse_cnt'] += 1

        for word in L.d(book, 'word'):
            object_count_dict[book_name]['word_cnt'] += 1

    info(f'Counting of {len(object_count_dict)} books is done')
    
    return object_count_dict

def GetGenres():

    prose = ['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy', 'Joshua', 'Judges', '1_Samuel', '2_Samuel', 
             '1_Kings', '2_Kings', 'Jonah', 'Ruth', 'Esther', 'Daniel', 'Ezra', 'Nehemiah', '1_Chronicles', '2_Chronicles']
    prophecy = ['Isaiah', 'Jeremiah', 'Ezekiel', 'Hosea', 'Joel', 'Obadiah', 'Micah', 'Zephaniah', 'Haggai', 'Zechariah', 
                'Malachi', 'Amos', 'Nahum', 'Habakkuk']
    poetry = ['Song_of_songs','Proverbs','Ecclesiastes', 'Lamentations', 'Psalms', 'Job']
    genre_dict = defaultdict()


    for genre in [prose, prophecy, poetry]:
        for book in genre:
            if book in prose:
                genre_dict[book] = 'prose'
            elif book in prophecy:
                genre_dict[book] = 'prophecy'
            elif book in poetry:
                genre_dict[book] = 'poetry'
    info(f'Done retrieving three genres in the Hebrew Bible: \n\n \
        Prose:     {prose} \n\n \
        Prophecy:  {prophecy} \n\n \
        Poetry:    {poetry}'
        )
    return genre_dict