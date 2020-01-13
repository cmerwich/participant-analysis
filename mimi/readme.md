# Deterministic Coreference Resolution

The notebooks are experiments and work in progress for the development of a deterministic approach for coreference resolution for the Hebrew Bible and the Psalms in particular. These programs have been built on the insights that have been developed in the [annotation](https://github.com/cmerwich/participant-analysis/tree/master/annotation) and [iaa](https://github.com/cmerwich/participant-analysis/tree/master/iaa) processes. 

* [mentionMake.ipynb](mentionMake.ipynb): makes mentions, i.e. referring expressions, as new Text-Fabric object. 
* [mentionUse.ipynb](mentionUse.ipynb): tests if the mention maker has done its job. 
* [MentionUseExperiments.ipynb](MentionUseExperiments.ipynb): experiments with mentions. For now it's just cruft. 
* [test](https://github.com/cmerwich/participant-analysis/tree/master/test/tf): contains the mention data as produced by `mentionMake`. 