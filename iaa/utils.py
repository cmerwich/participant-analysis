from collections import defaultdict
import pandas as pd
from tf.app import use

A = use(
    'bhsa', version='2017',
    hoist=globals(),
    silent=True
)

column_names=('ann_A','ann_B', 'L', 'M', 'R', 'D', 'd') 
data_types={'ann_A': str, 'ann_B': str ,'L': int, 'M': int, 'R': int, 'D': int, 'd': float}

def MakeTable(iaa_file):
    iaa_table = pd.read_table(iaa_file, 
                           delim_whitespace=True, 
                           names=column_names,
                           dtype=data_types
                          )
    return iaa_table


def ExportToLatex(output_loc, file_name, data_frame, indx = True):
    with open(f'{output_loc}{file_name}.tex','w') as texf:
        texf.write(data_frame.to_latex(index=indx))
        

def CountVersesWords():
    
    text_list = ['Psalms 138', 'Psalms 88', 'Psalms 11', 'Psalms 129', 'Psalms 70', 
             'Psalms 32', 'Psalms 20', 'Psalms 17', 'Psalms 101', 'Psalms 67',
             'Numbers 8', 'Numbers 9', 'Numbers 10'
            ]
    
    object_count_dict = {}
    
    for book in F.otype.s('book'):
        book_name = T.bookName(book)
        for chn in L.d(book, 'chapter'):
            chapter = F.chapter.v(chn)
            if book_name == 'Psalms' or book_name == 'Numbers':
                which_text = f'{book_name} {chapter}'
                
                if which_text in text_list:
                    object_count_dict[which_text] = defaultdict(int)
                
                    for verse in L.d(chn, 'verse'):
                        object_count_dict[which_text]['Verses'] += 1
                
                    for word in L.d(chn, 'word'):
                        object_count_dict[which_text]['Words'] += 1
    
    # calculate average 
    for k, v in object_count_dict.items():
        avg = round(v['Words']/v['Verses'], 1)
        object_count_dict[k]['Average'] = avg
        
    return object_count_dict