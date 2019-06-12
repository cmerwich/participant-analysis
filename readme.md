# Participant Analyis 

This repository contains (Python) code and data that I have created for my NWO funded PhD research project 'Who is Who is in the Psalms?'

The 'who is who?' question that always comes up when one reads a text can be solved by analysing all entities, or participants, in that text. The identification of entities enables a better informed interpretation process of the text.  

The focus of the research project is to set up a methodology to analyse participants in the Ancient Hebrew Poetry of the Psalms, but the goal is also to make that methodology reproducible and applicable to any genre in the Hebrew Bible for other researchers. 

Analysing participants is a notoriously hard Natural Langauge Processing task. In this research project participant analysis is cast as a coreference resolution problem. Accordingly, this repository is built up in the following way:

### 1. Annotation 
In `annotation` a method is set up to annotate Biblical Hebrew for coreference. 

### 2. Text-Fabric Conversion
With the code in `tf_conversion` the coreference annotations can be converted to Text-Fabric. This means that the annotations are enriched with other features that are not included in the annotations. 

### 3. Participant Data
In `coreference` the converted data can be found. This data can be loaded into your notebook. 

### 4. Inter-annotator Agreement
The `iaa` folder contains code and data to calculate and analyse inter-annotator agreement of the coreference annotations. 

### 5. Programs 
In `programs` I have started to develop a deterministic coreference resolver. Like all repositories, this work in progress and very unfinished. 

### 6. Test
The `test` folder contains the data that `programs` has produced.  

