<img align="right" src="images/tf-small.png" width="90"/>
<img align="right" src="images/etcbc.png" width="100"/>

# Creating a Coreference-annotated Corpus for Biblical Hebrew

#### An Analysis of Inter-annotator Agreement for Coreference Resolution Annotations in the Psalms and Beyond

This repository contains an inter-annotator agreement (abbreviated to IAA) analysis for coreference resolution annotations of ten Psalms and three Numbers texts. The IAA analyis has been done for two annotators: **A** and **B**.

### Inter-annotator Agreement Analysis
The notebook in which the actual IAA analysis is done is [iaa-analysis.ipynb](https://github.com/cmerwich/participant-analysis/blob/master/iaa/iaa-analysis.ipynb). Similar to the other directories a lot of the data and insights are used in my dissertation. Inter-annotator agreement analysis is not only calculating (dis)agreement measures, but also interpreting these measures. The iaa-analysis NB contains an extensive explanations of what IAA is, how the algorithms work and how the IAA analysis is done. The code and data that is used in the iaa-analysis NB is also found in this directory. 

### Code
The code that produces the IAA measures is contained in [`iaa.py`](https://github.com/cmerwich/participant-analysis/blob/master/iaa/iaa.py) and [`acc.py`](https://github.com/cmerwich/participant-analysis/blob/master/iaa/acc.py). The [`Makefile`](https://github.com/cmerwich/participant-analysis/blob/master/iaa/Makefile) executes the algorithms.

In the directory [declustering](https://github.com/cmerwich/participant-analysis/tree/master/iaa/declustering) an algorithm is found to decluster the cluster of Numbers chapters 8-10. This cluster was annotated for coreference by **B**. 

### Files
* The annotation files on which `iaa.py` and `acc.py` operate are stored in annotator [A's](https://github.com/cmerwich/participant-analysis/tree/master/iaa/chris_A) directory and annotator [B's](https://github.com/cmerwich/participant-analysis/tree/master/iaa/gyus_B) directory. Psalm 11, 17, 20, 32, 67, 70, 88, 101, 129 and 138 and Numbers 8-10 are compared. 
* When `make` is executed it the IAA algorithms produce IAA measures per text and corpus. These are stored in IAA files in the current working directory. In this directory they are stored in [iaa-files](https://github.com/cmerwich/participant-analysis/tree/master/iaa/iaa-files).
* Like the other coreference annotations, the annotations of the cluster of Numbers chapters 8-10 is stored in the *brat* `.ann` format. The `.ann` cluster and the separate Numbers chapters that are processed by the declustering algorithm to produce separate `.ann` files per chapter are also stored in the [declustering](https://github.com/cmerwich/participant-analysis/tree/master/iaa/declustering) directory. 