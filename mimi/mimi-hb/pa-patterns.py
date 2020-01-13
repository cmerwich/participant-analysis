from collections import Counter
from shutil import rmtree
from pprint import pprint

from tf.app import use
from tf.fabric import Fabric

def GetPaPatterns():
    '''
    This funtion has been used for:
    - studying phrase atom patterns for status, stored in `freq_dict'
    - retrieving unique tokens in the whole Hebrew Bible for MyLexer()
    '''
    
    freq_dict = Counter()
    token_set = set()
    typ_choice = {'NP', 'PP', 'PrNP', 'PPrP', 'VP', 'DPrP', 'IPrP'}
    word_prs_pattern = ''
    word_pattern = ''
    
    token_set.add('EOA') # add End Of Atom token
    token_set.add('CONJ_P') # special token for complex prepositional phrases: CONJ PREP to CONJ_P PREP 
    
    for pa in F.otype.s('phrase_atom'):
        pa_pattern = ''
        pa_typ = F.typ.v(pa)
        if pa_typ in typ_choice:
            pa_words = L.d(pa, 'word')
            pa_word = tuple(word for word in pa_words)
            for word in pa_word:
                pdp = F.pdp.v(word)
                st = F.st.v(word)
                if 'a' not in F.prs.v(word):
                    prs = f'prs'.upper()
                    token_set.add(prs)
                    pos = f'{pdp}_p'.upper() if pdp in {'subs', 'adjv'} else f'{pdp}'.upper()
                    token_set.add(pos)
                    word_prs_pattern = f'{pos} prs'.upper() 
                    pa_pattern += f'{word_prs_pattern} '            
                else:
                    if pdp not in {'subs', 'adjv'}:
                        pos = f'{pdp}'.upper()
                        pa_pattern += f'{pos} '
                        token_set.add(pos)
                    else:
                        if word == pa_word[-1] and st == 'c':
                            pos = f'{pdp}_a'.upper()
                            pa_pattern += f'{pos} '
                            token_set.add(pos)
                        else: 
                            pos = f'{pdp}_{st}'.upper()
                            pa_pattern += f'{pos} '
                            token_set.add(pos)

            freq_dict[pa_pattern] += 1
    
    #for i, (k, v) in enumerate(sorted(freq_dict.items(), reverse=True, key=lambda x: x[1])):
    #    print(i+1, k, v)
    
    pprint(token_set)