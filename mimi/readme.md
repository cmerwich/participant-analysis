<img align="right" src="images/tf-small.png" width="90"/>
<img align="right" src="images/etcbc.png" width="100"/>

# Deterministic Coreference Resolution

This directory contains a deterministic - i.e. rule-driven - coreference resolution resolver called MiMi. MiMi is the concatenation of *Mi Mi* in Biblical Hebrew (BH) meaning 'Who? Who?' MiMi is used as a tool to identify and analyse participants or entities in a text. MiMi operates on hand-coded BHSA data. MiMi's architecture is loosely based on Stanford's deterministic multi-sieve algorithm (links to [ACL](https://www.aclweb.org/anthology/J13-4004/) and the [pdf](https://www.aclweb.org/anthology/J13-4004.pdf)). 

## MiMi - The Algorithm

In this folder the actual algorithm is found. In [MiMi.ipynb](https://github.com/cmerwich/participant-analysis/blob/master/mimi/MiMi.ipynb) the agorithm is explained and its performance is demonstrated. 

To run MiMi:

1. Make sure you have [Text-Fabric](https://annotation.github.io/text-fabric/) and the BHSA data up and running on your computer. To install Text-Fabric follow the [installation](https://annotation.github.io/text-fabric/About/Install/) instructions.
2. The command is `[your python 3 version] mimi.py bible_book from_chapter [to_chapter]` where the last argument is optional. 
3. Do in your terminal for example: `python3 mimi.py Psalms 1 50` this will resolve coreference for the first 50 Psalm chapters. 
Another example: `python3 mimi.py Isaiah 40` will resolve coreference for only Isaiah 40. 

MiMi produces three kinds of files per chapter:

* `.txt` file with the transliterated Hebrew text;
* `.ann` file with the coreference data;
* `.tsv` file for data administration purposes. 

After MiMi has been run, the data can be visualised and analysed with the functions in `mimi_visualise.py` for example in the the notebook [mimi-analyse](https://github.com/cmerwich/participant-analysis/blob/master/mimi/mimi-analyse.ipynb). The `.ann` files can be imported into annotation tool *brat*.

## MiMi for the Hebrew Bible - A Demonstration

In the [mimi-hb](https://github.com/cmerwich/participant-analysis/tree/master/mimi/mimi-hb) folder is demonstrated that MiMi operates on the entire Hebrew Bible. Various performance statistics are presented here. See the [mimi-hb.ipynb](https://github.com/cmerwich/participant-analysis/blob/master/mimi/mimi-hb/mimi-hb.ipynb) notebook for this demonstration. 

## Experiments

In the directory [preparation-experiments](https://github.com/cmerwich/participant-analysis/tree/master/mimi/preparation-experiments) two experimental notebooks are found. They were used as preparation for the development of a deterministic approach for coreference resolution for the Hebrew Bible and the Psalms in particular.
* [mentionMake.ipynb](mentionMake.ipynb): makes mentions, i.e. referring expressions, as new Text-Fabric object. 
* [mentionUse.ipynb](mentionUse.ipynb): tests if the mention maker has done its job. 
* [test](https://github.com/cmerwich/participant-analysis/tree/master/test/tf): contains the mention data as produced by `mentionMake`. 