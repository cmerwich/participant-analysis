<img align="right" src="images/tf-small.png" width="90"/>
<img align="right" src="images/etcbc.png" width="100"/>

# Importing Coreference Data into Text-Fabric

With the code in this directory the coreference annotations can be converted to data that can be processed with Text-Fabric. This means that the annotations are enriched with other features that are not included in the annotations. 

### Make Coreference Data

The notebook [corefMake](https://github.com/cmerwich/participant-analysis/blob/master/tf_conversion/corefMake.ipynb) converts the coreference annotations back to Text-Fabric data. This NB needs to be run first before it can be analysed with NB's `corefStatistics` and `analyseParticipants`. 

### Analyse and Search the Data

In the notebooks `corefStatistics` and `analyseParticipants` three kinds of `.py` files are imported that are used for analysis. 

* `analyse.py`: parses the Text-Fabric converted coreference annotations into readable data and enriches it with features that are informative such as which mention (type) starts a coreference chain. `analyse.py` contains functions to print-visualise the coreference data and annotator notes in an insightful way; fuctions to correct annotation errors; and functions to generate descriptive statistics of the coreference annotated corpus. In `analyseParticipants` the functions are explained further. 
* `search.py` : offers a number of functions that can search for entities in the annotations; find the coreference chains that start with a certian mention type; find mentions within a coreference chain and singletons. In `analyseParticipants` the functions are explained further.
* `export_utils.py`: converts Pandas tables into a LateX table and exports to the desired export location. 

### Make Statistics 

The notebook [corefStatistics](https://github.com/cmerwich/participant-analysis/blob/master/tf_conversion/corefStatistics.ipynb) gives descriptive statistics of the coreference annotated corpus. Genesis 1, Isaiah, 42 and the book of Psalms have been annotated by Christiaan. Numbers has been annotated by Gyusang Jin. 

In the NB `export_utils.py` and `analyse.py` are imported. 

### Analyse Participant Data

With the code in notebook [analyseParticipants](https://github.com/cmerwich/participant-analysis/blob/master/tf_conversion/analyseParticipants.ipynb) the coreference annotated corpus, converted with `corefMake`, can be analysed for participants for any given text. It also produces overviews of possible annotation errors and descriptive statistics in tables. 

In the NB `analyse.py` and `search.py` are imported. 