# Deterministic Coreference Resolution

This directory contains a deterministic - i.e. rule-driven - coreference resolution resolver called MiMi. MiMi is the concatenation of *Mi Mi* in Biblical Hebrew (BH) meaning 'Who? Who?' MiMi is used as a tool to identify and analyse participants or entities in a text. MiMi operates on hand-coded BHSA data. MiMi's architecture is loosely based on Stanford's deterministic multi-sieve algorithm (links to [ACL](https://www.aclweb.org/anthology/J13-4004/) and the [pdf](https://www.aclweb.org/anthology/J13-4004.pdf)). 

## MiMi - The Algorithm

In this folder the actual algorithm is found. [Add further description]

## MiMi for the Hebrew Bible - A Demonstration

In this folder is demonstrated that MiMi operates on the entire Hebrew Bible. Various performance statistics are presented here. [Add further description]

## Experiments

In the directory [preparation-experiments](https://github.com/cmerwich/participant-analysis/tree/master/mimi/preparation-experiments) two experimental notebooks are found. They were used as preparation for the development of a deterministic approach for coreference resolution for the Hebrew Bible and the Psalms in particular.
* [mentionMake.ipynb](mentionMake.ipynb): makes mentions, i.e. referring expressions, as new Text-Fabric object. 
* [mentionUse.ipynb](mentionUse.ipynb): tests if the mention maker has done its job. 
* [test](https://github.com/cmerwich/participant-analysis/tree/master/test/tf): contains the mention data as produced by `mentionMake`. 