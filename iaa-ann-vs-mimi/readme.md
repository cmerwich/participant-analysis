<img align="right" src="images/tf-small.png" width="90"/>
<img align="right" src="images/etcbc.png" width="100"/>

# Validating Manual Annotations and MiMi's results

In the [validation](https://github.com/cmerwich/participant-analysis/blob/master/iaa-ann-vs-mimi/validation.ipynb) notebook the manual coreference annotations and the coreference data produced by the deterministic coreference resolution algorithm MiMi are compared. The comparison is done in two ways. Firstly, the inter-annotator (IAA) algorithm that is presented in the [iaa](https://github.com/cmerwich/participant-analysis/tree/master/iaa) directory used again. Important to note is that running the IAA algorithm merely gives an indication of what the quality of the MiMi data. MiMi has a near perfect mention detection system, but a coreference resolution success rate that needs enhancement. This has to do with the basic implementation of the coreference resolver. Secondly, a mention detection comparison is done. Since the manual `.ann` files and MiMi's `.ann` files are based on transliterated texts that are structured in a slightly different way, they first need to be 'translated'. 

## Translate

The makefile `Translate` 'translates' (or aligns) the mention boundaries in the MiMi `.ann` files with those in the manual `.ann` files. It produces `diff` files per chapter and calls the `translate` algorithm in `translate.py` to align the mention boundaries, i.e. start and end index of the mention. For each chapter a new, translated MiMi `.ann` file is produced. 

1. Specify in `Translate` the old and new directory. In `Old` the manual annotations should be stored. In `New` the MiMi annotations should be stored. 
2. Make sure the `Translate`, `translate.py` and `mentiondiff.sh` are all in the same directory in which you also want to store the new MiMi `.ann` files. 
3. Then do in the same directory in your terminal: `make -f Translate`. All `.ann` files are translated and `diff` files are made. 


## Inter-annotator agreement analysis

Now the desired files have been translated, the IAA algorithm can be run. 

1. Place the `iaa.py`, `acc.py` and `Makefile` in that same folder as the `Translate` makefile, etc. 
2. Change the file locations for the `.ann` files under `PS_A` and `PS_B` in the `Makefile`. Make sure the **A** location is for the manual annotations and that **B** locations is for MiMi; 
3. Give the command `make`;
4. `iaa.py` will do its work and the IAA measures are printed per Hebrew Bible chapter in separate txt files with extension `.iaa` and it prints one total IAA measure for all compared texts. All files are stored in the working directory.

## Parse

The algorithm in `parse.py` parses the `.ann` for mentions to facilitate a comparison of the mention detection of both the manual annotations and MiMi's results. 