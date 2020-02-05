<img align="right" src="images/tf-small.png" width="90"/>
<img align="right" src="images/etcbc.png" width="100"/>

To cite this repository please use: [![DOI](https://zenodo.org/badge/106433812.svg)](https://zenodo.org/badge/latestdoi/106433812)

# Participant Analyis 

This repository contains (Python) code and data that I have created for my NWO funded PhD research project 'Who is Who is in the Psalms?'

The 'who is who?' question that always comes up when one reads a text can be solved by analysing all entities, or participants, in that text. The identification of entities enables a better informed interpretation process of the text.  

The focus of the research project is to set up a methodology to analyse participants in the Ancient Hebrew Poetry of the Psalms, but the goal is also to make that methodology reproducible and applicable to any genre in the Hebrew Bible for other researchers. 

Analysing participants is a notoriously hard Natural Language Processing task. In this research project participant analysis is cast as a coreference resolution problem. Coreference resolution is employed as a method to analyse participants in the Hebrew Bible. I refer to the notebooks, and the data and insights contained within them, in my dissertation. The repository is built up in the following way:

### 1. Introduction
This folder contains a notebook [intro](https://github.com/cmerwich/participant-analysis/blob/master/introduction/intro.ipynb) that produces informative statistics presented in tables and graphs about the kind of data that is important for participant analyis. I use some of the graphs and tables in the introduction of my dissertation. 

### 2. Annotation 
In `annotation` a method is set up to annotate Biblical Hebrew for coreference. The folder contains: 
1. A notebook that [produces annotation files](https://github.com/cmerwich/participant-analysis/blob/master/annotation/1.file_preparation_for_annotation.ipynb) that can be imported in annotation tool *brat*.
2. An [annotation aid](https://github.com/cmerwich/participant-analysis/blob/master/annotation/2.annotation_aid.ipynb) that can be used to annotate coreference data. The annotation aid visualises potential mentions and features and syntactic relations that are useful and informative for coreference annotation. 
3. A notebook '[counts](https://github.com/cmerwich/participant-analysis/blob/master/annotation/3.counts.ipynb)' that does some data exploration. 

### 3. Text-Fabric Conversion
With the code in `tf_conversion` the coreference annotations can be converted to data that can be processed with Text-Fabric. This means that the annotations are enriched with other features that are not included in the annotations. 
1. The notebook [corefMake](https://github.com/cmerwich/participant-analysis/blob/master/tf_conversion/corefMake.ipynb) converts the coreference annotations back to Text-Fabric data. 
2. The notebook [corefStatistics](https://github.com/cmerwich/participant-analysis/blob/master/tf_conversion/corefStatistics.ipynb) gives descriptive statistics of the coreference annotated corpus. Genesis 1, Isaiah, 42 and the book of Psalms have been annotated by Christiaan. Numbers has been annotated by Gyusang Jin. 
3. With the code in notebook [analyseParticipants](https://github.com/cmerwich/participant-analysis/blob/master/tf_conversion/analyseParticipants.ipynb) the coreference annotated corpus, converted with `corefMake`, can be analysed for participants for any given text. It also produces overviews of possible annotation errors and descriptive statistics in tables. 

### 4. Coreference Data
In `coreference` the converted coreference data is stored by `corefMake`. This coreference data can be loaded into a notebook. 

### 5. Inter-annotator Agreement
The `iaa` folder contains code and data to calculate and analyse inter-annotator agreement (abbreviated to: iaa) of the coreference annotations. An iaa analysis is done since mistakes are inherent to any annotation process. Annotations thus need to be scrutinised for quality and consistency. In the [iaa-analysis notebook](https://nbviewer.jupyter.org/github/cmerwich/participant-analysis/blob/master/iaa/iaa-analysis.ipynb) I explain what kind of inter-annotator agreement algorithm I have used. I also analyse and interpret the iaa measures. 

### 6. MiMi - A Deterministic Coreference Resolver for Biblical Hebrew
The `MiMi` folder contains a deterministic -- i.e. a rule-driven -- coreference resolver for Biblical Hebrew. MiMi is the concatenation of *Mi* *Mi* which means Who? Who? in Biblical Hebrew.  

1. In the `mimi-hb` folder the notebook [mimi-hb](https://github.com/cmerwich/participant-analysis/blob/master/mimi/mimi-hb/mimi-hb.ipynb) demonstrates MiMi's performance for the whole Hebrew Bible. Hence,`mimi-hb` cannot be used for actual qualitative coreference resolution analysis; [MiMi](https://github.com/cmerwich/participant-analysis/blob/master/mimi/MiMi.ipynb) can however (see point 2). In the notebook is explained how the algorithm works and what kind of files it produces. MiMi operates in two stages: mention detection and coreference resolution. 
* For the mention detection stage a Python implemention of the lex and yac parsers called [SLY](https://sly.readthedocs.io/en/latest/index.html) is implemented. 
* For the coreference resolution stage a sequence of five sieves is applied: predicates, 1P and 2P pronouns, vocatives, appositions and fronted elements. 
MiMi produces descriptive statistics in tables and graphs for both stages. It is important to note that MiMi operates on hand-coded [BHSA data](https://etcbc.github.io/bhsa/) that has been encoded over a period of about 30 years by the team at the Eep Talstra Centre for Bible and Computer (ETCBC). The BHSA database offers both parsed text objects such as words, phrases, clauses, etc., and a rich data set of features for all these text levels that can possiby contain implicit and explicit semantic information. MiMi gratefully makes use of both the boundaries of the text objects and the features. In that sense MiMi is not a strict application of a coreference resolver as may be formulated and understood by the computerised linguistics community (see for example: [coreference](https://en.wikipedia.org/wiki/Coreference), [Stanford's models](https://stanfordnlp.github.io/CoreNLP/coref.html) and [what is computational linguistics?](https://www.aclweb.org/portal/what-is-cl)). 

2. In the [MiMi](https://github.com/cmerwich/participant-analysis/blob/master/mimi/MiMi.ipynb) notebook MiMi can be used to resolve coreference for any given text in the Hebrew Bible. The notebook can also be used for actual qualitative coreference resolution analysis which in turn can be used for participant analysis. In the function `CreateCoref` a single text can be specified or a whole Bible Book. The program produces three files per specified chapter:
    * An `.ann` file that contains mentions and coreference classes. The data in the `ann` files is structured and can be parsed in any way. Since the structure is based on *brat*'s `ann` file format, the files can also be imported back into *brat* for further enhancement. This is important since MiMi resolves on average about 28.5% of the mentions in to coreference class. 
    * A plain `.txt` file with the [transliterated](https://annotation.github.io/text-fabric/Writing/Hebrew/) Hebrew Bible text.
    * A `.tsv` file that keeps track of the words, their positions and word nodes (unique TF identifiers).
MiMi produces descriptive statistics in tables and a graph for the mention detection and coreference resolution stages.

### Issues or fixes 
* (TO DO:) A qualitative validation of MiMi's results with the manual annotations with the `iaa` algorithm. In the folder `iaa-ann-vs-mimi` first experiments have been done. 
* (TO DO:) The mentions and coreference classes can be visualised and analysed with the following functions.