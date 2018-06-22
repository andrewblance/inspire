import numpy as np
import json
from inspire_utils.record import get_value
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.util import ngrams

def read_json(filename):
    '''filename is a string= /path/to/file'''
    with open(filename) as f:
        for line in f:
            try:
                yield json.loads(line)
            except:
                continue

def removeNonAscii(string):
    return "".join( char for char in string if ord(char)<128 )

# Import some important datafiles which contain the list of core articles.
core_list = pd.read_csv("./datfiles/core_arxiv.txt", names=["core"])
noncore_list = pd.read_csv("./datfiles/noncore_arxiv.txt", names=["noncore"])
core, noncore = [],[]

# read the core arXiv list
for line in core_list['core']:
    name = line.split(":")[2]
    core.append(name)
core = set(core) #pd.DataFrame(core, columns=["core"])

# read the noncore arXiv list.
for line in noncore_list['noncore']:
    name = line.split(":")[2]
    noncore.append(name)
noncore = set(noncore) #pd.DataFrame(noncore)

inspire_core_set = set(np.genfromtxt("./datfiles/inspire_core.txt").tolist())


### CORENESS

def get_coreness(listing, which_listing=0):
    arXiv_id = get_value(listing,"extra_data.source_data.data.arxiv_eprints[%d].value" %which_listing)
    if arXiv_id in core:
        return 2
    elif arXiv_id in noncore:
        return 1
    else:
        return 0

###TEXT BASED STUFF.

def get_title(listing,which_version=0):
    '''Get the title. If there are >1 versions, which_ver selects that version.'''
    title = get_value(listing,"extra_data.source_data.data.titles[%d].title" % which_version)
    title = removeNonAscii(title)
    return title

def get_abstract(listing,which_version=0):
    #                             look at this location in "example_api"
    abstract = get_value(listing,"extra_data.source_data.data.abstracts[%d].value" %which_version)
    abstract = removeNonAscii(abstract)
    return abstract

def get_category(listing,which_version=0):
    category = get_value(listing,"extra_data.source_data.data.arxiv_eprints[%d].categories[0]" %which_version)
    return category

### NGRAMS FUNCTIONS.

# read in the HEP keywords.
keysfile = np.loadtxt("./datfiles/KeyWords.csv", dtype="str") # load the keywords.
keywords = [word.lower() for word in keysfile]     # lowercase them all.

def make_ngrams(string, N):
    '''what size if ngram to look at? N'''
    tokens = nltk.word_tokenize(string)
    ngram_tuples = list( ngrams(tokens,N) )
    ngram_list = [''.join(words) for words in ngram_tuples]
    return ngram_list

def ngram_search(ngram_list,keywords=keywords):
    ngram_list = [word.lower() for word in ngram_list]
    ''' find the intersection of the ngram-ed string and the keyword list.'''
    matches = list( set(ngram_list).intersection( set(keywords) ) )
    return matches


### REFERENCES

def get_reference_fractions(listing):
    if get_value(listing, "data.references"):
        refs = get_value(listing, "data.references")
    else:
        return [0.0,0.0]
    
    core_refs = 0.0
    noncore_refs = 0.0
    N_refs = float(len(refs))
    for ref in refs:
        if get_value(ref, "record.$ref"):
            inspire_id = int(get_value(ref, "record.$ref").split("/")[5])
            if inspire_id in inspire_core_set:
                core_refs = core_refs + 1.0
            else:
                noncore_refs = noncore_refs + 1.0
    
    f_core = core_refs/N_refs
    f_noncore = noncore_refs/N_refs
    
    return [f_core, f_noncore]

def get_ref_median_year(listing):
    if get_value(listing, "data.references"):
        refs = get_value(listing, "data.references")
    else:
        return 0.0

    Nrefs = len(refs)
    ref_no_year_count = 0.0
    years = []
    
    for ref in refs:
        if get_value(ref, "reference.publication_info.year"):
            year = int(get_value(ref, "reference.publication_info.year"))
            years.append(year)
        else:
            ref_no_year_count = ref_no_year_count + 1.0
    return np.median(years)

#def read_refs2o():
#    with open("./datfiles/reference_coreness.txt") as reffile:
#        for line in reffile:
#            yield np.array(line.replace("\n","").split(), dtype="float")

def get_Nrefs(listing):
    if get_value(listing, "data.references"):
        refs = get_value(listing, "data.references")
        N_refs = float(len(refs))
        return N_refs
    else:
        return 0.0




### OUTDATED:

def get_references(listing):
    '''replaced with get_references_fractions()'''
    if get_value(listing, "data.references"):
        refs = get_value(listing, "data.references")
    else:
        return [0.0,0.0]
    
    core_refs = 0.0
    noncore_refs = 0.0
    N_refs = float(len(refs))
    for ref in refs:
        if get_value(ref, "record.$ref"):
            inspire_id = int(get_value(ref, "record.$ref").split("/")[5])
            if inspire_id in inspire_core_set:
                core_refs = core_refs + 1.0
            else:
                noncore_refs = noncore_refs + 1.0
    
    f_core = core_refs/N_refs
    f_noncore = noncore_refs/N_refs
    
    return [f_core, f_noncore]
































