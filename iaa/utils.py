import pandas as pd

column_names=('ann_A','ann_B', 'L', 'M', 'R', 'D', 'd') 
data_types={'ann_A': str, 'ann_B': str ,'L': int, 'M': int, 'R': int, 'D': int, 'd': float}

def MakeTable(iaa_file):
    iaa_table = pd.read_table(iaa_file, 
                           delim_whitespace=True, 
                           names=column_names,
                           dtype=data_types
                          )
    return iaa_table