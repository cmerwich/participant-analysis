import re, collections
from IPython.display import display, HTML, Markdown

from tf.app import use
from tf.fabric import Fabric

from utils import prs_set

def do(task):
    result = task
    md = f'''commit | release | local | base | subdir
    --- | --- | --- | --- | ---
    `{task[0]}` | `{task[1]}` | `{task[2]}` | `{task[3]}` | `{task[4]}`
    '''
    display(Markdown(md))


A = use(
    'bhsa:latest', version='2017',
    mod=(
        'cmerwich/bh-reference-system/tf'
    ),
    hoist=globals(),
    silent=True
)

def compute_text(my_book_name, from_chapter, to_chapter):

    results = []
    highlights = {}
    
    my_chapters = set(range(from_chapter, to_chapter+1))
    
    for book in F.otype.s('book'):
        book_name = T.bookName(book)
       
        for chn in L.d(book, 'chapter'):
            chapter = F.chapter.v(chn)
            tup = (chn,)
            if (
                (my_book_name and book_name not in my_book_name)
                or 
                (my_chapters and chapter not in my_chapters)
            ):
                continue
            for phrase in L.d(chn, 'phrase'):
                typ = F.typ.v(phrase)
                if typ == 'NP':
                    tup = tup + (phrase,)
                    highlights[phrase] = 'skyblue'

            for phr_atom in L.d(chn, 'phrase_atom'):
                if F.rela.v(phr_atom) == 'Appo':
                    tup = tup + (phr_atom,)
                    highlights[phr_atom] = 'yellow'

            for w in L.d(chn, 'word'):
                pdp = F.pdp.v(w)
                pgn_prps = F.pgn_prps.v(w)
                pgn_prde = F.pgn_prde.v(w)
                pgn_verb = F.pgn_verb.v(w)
                pgn_prs = F.pgn_prs.v(w)

                if pdp == 'verb':
                    tup = tup + (w,)
                    highlights[w] = 'springgreen'

                if pdp == 'subs':
                    tup = tup + (w,)
                    highlights[w] = 'skyblue'

                if pdp == 'art':
                    tup = tup + (w,)
                    highlights[w] = 'skyblue'

                if pdp == 'nmpr':
                    tup = tup + (w,)
                    highlights[w] = 'tomato' 

                if pdp == 'prps':
                    tup = tup + (w,)
                    highlights[w] = 'palegoldenrod'

                if pdp == 'prde':
                    tup = tup + (w,)
                    highlights[w] = 'royalblue'

                if pdp == 'prep' and pgn_prs in prs_set:
                    tup = tup + (w,)
                    highlights[w] = 'DarkGoldenrod'

            results.append(tup)
    return (results, highlights)

def show_text(results, highlights):
    A.displaySetup(withNodes=True, extraFeatures='pgn_prps pgn_prde pgn_verb pgn_prs pdp typ rela ls function det st lex:gloss nametype vs gn nu') #ps gn nu
    A.show(results, condensed=False, highlights=highlights)