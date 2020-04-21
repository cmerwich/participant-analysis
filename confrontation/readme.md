<img align="right" src="images/tf-small.png" width="90"/>
<img align="right" src="images/etcbc.png" width="100"/>

# Psalm 75 as Test Case

The directory is called 'confrontation' because the generated coreference data for the Psalms - specifically Psalm 75 - will be brought into discussion with the commentaries' analyses of Psalm 75. For an extensive discussion with the commentaries I refer to my dissertation which is forthcoming. The [`confrontation`](https://github.com/cmerwich/participant-analysis/blob/master/confrontation/confrontation-ps75.ipynb) notebook hence aims to analyse Psalm 75 with the coreference data that has been produced by the coreference annotation method and MiMi. The algorithms stored in `.py` files have been explained in the notebooks in other directories. 

* The functions in and `analyse.py` and `search.py` are explained in [analyseParticipants.ipynb](https://github.com/cmerwich/participant-analysis/blob/master/tf_conversion/analyseParticipants.ipynb). 
* The function `retrieve_ann` in `retrieve_iaa.py` is explained in [`iaa-analysis.ipynb`](https://github.com/cmerwich/participant-analysis/blob/master/iaa/iaa-analysis.ipynb). 
* The MiMi algorithm `mimi.py` is explained in [MiMi.ipynb](https://github.com/cmerwich/participant-analysis/blob/master/mimi/MiMi.ipynb). In [mimi-hb.ipynb](https://github.com/cmerwich/participant-analysis/blob/master/mimi/mimi-hb/mimi-hb.ipynb) is demonstrated that the algorithm works for the entire Hebrew Bible.

As is demonstrated in `confrontation.ipynb` the IAA algorithm is used to correct the manual coreference annotations. The corected manual annotations (and administration files) are stored in `Psalms_075.ann`. The uncorrected in the folder [annotation-uncorr](https://github.com/cmerwich/participant-analysis/tree/master/confrontation/annotation-uncorr). 