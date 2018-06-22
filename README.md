# Inspire Core Classifier Project
When Inspire collects papers from arXiv they are classified Core or Non-Core, or they are Rejected from the database based on their relevance to high energy physics. Our project was to build a classifier that would carry this out. We settled on a SVM that uses the references of the papers as features then we determine if we can trust the results based on the distances from the decision boundary.

## Getting Started
Included in this repository is the notebook required to extract data from a ```.json``` file containing INSPIRE records. The file we used is very large, to aquire it email aidan.sedgewick@dur.ac.uk. Two premade extractions are available in ```/datfiles``` titled ```INSPIRE.df``` and ```INSPIREpy2.df```. The rest of the files in ```/datfiles``` and ```json_tools.py``` are required to run ```ExtractDataFromJSON.ipynb```. Also included for reference is ```example_record``` - this is a copy of 1 INSPIRE entry.

We have also included our presentation on our final results, this is ```inspire_talk_original.pdf```

## Running
The file ```inspire_classifer.ipynb``` contains all the major attempts we made at solving the problem. Therefore, running the entire file will take time. Only the sections titled 'Initial dataframe import', 'SVM with fractions' and 'Decision Boundary Cuts' need to be run to produce our final results. 

## Authors
Andrew Blance
Aidan Sedgewick
Parisa Gregg
  
 
