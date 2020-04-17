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


def ExportToLatex(output_loc, file_name, data_frame, indx = True):
    with open(f'{output_loc}{file_name}.tex','w') as texf:
        texf.write(data_frame.to_latex(index=indx))