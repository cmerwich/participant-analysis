<img align="right" src="images/tf-small.png" width="90"/>
<img align="right" src="images/etcbc.png" width="100"/>

# Annotating the Psalms for Coreference

These Jupyter notebooks enable annotation for coreference in the Biblical Hebrew poetry of the Psalms and other Hebrew Bible books. In the notebooks themselves is explained what function they have and what data is used. 

### Generate files 

The needed annotation files are produced with notebook `1.file_preparation_for_annotation.ipynb`. The NB produces three kinds of files. 

* [text-trans-plain](https://dans-labs.github.io/text-fabric/Api/General/#text-representation) .txt files for annotation of the Biblical Hebrew text. These text-trans-plain .txt files can be imported into annotation tool [brat](http://brat.nlplab.org). 
* [text-orig-full](https://dans-labs.github.io/text-fabric/Api/General/#text-representation) .txt files for easy reading of the Biblical Hebrew text. This is a ETCBC transliteration of Ancient Hebrew. Reading the transliterated Hebrew Bible text may need some getting used to. The text-orig-full .txt files can be used as an extra aid. 
* stand-off .tsv files for future Text-Fabric administration. The stand-off .tsv files are needed to convert the brat annotation `.ann` files back into brat. This is done with [corefMake.ipynb](https://github.com/cmerwich/participant-analysis/blob/master/tf_conversion/corefMake.ipynb) in the `tf_conversion` repository.

### Annotation Aid and Resources

Notebook `2.annotation_aid.ipynb` contains a number of functions that display the morphological, syntactical and semantic information that is needed for proper annotation of coreference in the text of the Hebrew Bible in an informative way. 

The folder [annotation_resources](https://github.com/cmerwich/participant-analysis/tree/master/annotation/annotation_resources) contains resources that can help with analysing the ETCBC transliterated forms. How this is done is explained in `2.annotation_aid.ipynb`. 

### Counts and Graphs of Reference Data

The `3.counts.ipynb` notebook contains counts and graphs of occurences of the referring expressions that are being annotated. 

### brat
Follow the instructions on [brat](http://brat.nlplab.org) to download and install the package. The text-trans-plain .txt files need to be imported in brat before they can be annotated. This can be done by simply storing the txt files in the directory on which brat operates. After storage, in the same directory `.ann` files need to be made. The web server also needs to have read and write permissions for all files. 
* First create zero-sized a `.ann` file for each `.txt` file in the directory. In `bash`: `for i in *.txt; do touch ${i%.txt}.ann; done`
* then do:`chmod 664 *.txt and chmod 664 *.ann` 

### Configuration Files for brat

To be able to annotate coreference information in the text-trans-plain files as defined in the 'Who is Who in the Psalms' project, the following brat configutation files are needed: 
* `annotation.conf`: defines the kind of relations, i.e. coreference relations, that are being annotated. 
* `tools.conf`: defines the tools that operate on the annotated data in brat, e.g. a exact string search tool. 
* `visual.conf`: defines the visualisation configuration of the data. 
To maintain interoperabilityt, all .conf files have been taken from the brat download package. 