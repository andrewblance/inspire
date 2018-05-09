from __future__ import division
import numpy as np
import string
import re
import nltk
from nltk import word_tokenize
from nltk.util import ngrams
from scipy import sparse
from scipy.sparse import csr_matrix

def load_keys(name):
    with open(name+".csv", "rb") as f:
        A = np.loadtxt(f,dtype=str)
    return A

def _removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

def load_data(name):
    Data = []
    with open(name+".txt", "r") as ins:
        for line in ins:
            line = _removeNonAscii(line)
            line = line.replace(",", "")
            line = line.replace(".", "")
            Data.append(line)
            
    return Data

def split_text(text):
    ETITLE = ["ENDTITLE"]
    entries = []
    j=0
    while (j <(len(text))):
        if (text[j].count('ENDTITLE') == 3):
            text_split = re.split("ENDTITLE|ENDTITLE|ENDTITLES|ENDABSTRACTS",text[j])
            title1 = text_split[0].strip()
            title2 = text_split[1].strip()
            title3 = text_split[2].strip()
            abstract = text_split[3].replace("\r\n"," ").strip()
            decision = text_split[4].strip()
            entries.append({u'title':title1,u'abstract':abstract,u'decision':decision})
            j = j +1
        elif (set(ETITLE).intersection(text[j].split()) == set(['ENDTITLE'])):
            text_split = re.split("ENDTITLES|ENDTITLE|ENDABSTRACTS",text[j])
            title1 = text_split[0].strip()
            title2 = text_split[1].strip()
            abstract = text_split[2].replace("\r\n"," ").strip()
            decision = text_split[3].strip()
            entries.append({u'title':title1,u'abstract':abstract,u'decision':decision})
            j = j +1
        else: 
            text_split = re.split("ENDTITLES|ENDABSTRACTS",text[j])
            title = text_split[0].strip()
            abstract = text_split[1].replace("\r\n"," ").strip()
            decision = text_split[2].strip()
            entries.append({u'title':title,u'abstract':abstract,u'decision':decision})
            j = j + 1
    return(entries)

def tokenize(text,n_files):
    #split=split_text(text)
    tokens=[]
    for i in range(0,n_files):
        title_tokens=nltk.word_tokenize(split[i].get('title').lower()) 
        abstract_tokens=nltk.word_tokenize(split[i].get('abstract').lower())
        tokens.append({u'title':title_tokens,u'abstract':abstract_tokens})
    return (tokens)

def find_keywords(n,token,keys,freq_on):
    n_gram=list(ngrams(token,n))
    smush=["" for x in range(len(token))]
    for i in range(len(n_gram)):
        for j in range(0,n):
            smush[i]+=n_gram[i][j]          
    key_freq=[]
    if freq_on==False:
        for i in range(len(keys)):
            if keys[i] in  smush:
                key_freq.append(1)
            else:
                key_freq.append(0)
    else:
        for i in range(len(keys)):
            if keys[i] in  smush:
                key_freq.append(smush.count(keys[i]))
            else:
                key_freq.append(0)
            
    return sparse.lil_matrix(key_freq)

def key_tot(text,keys,freq_on):
    #split=split_text(text)
    #title_tokens=[]
    abstract_tokens=[]
    key_freq=sparse.lil_matrix((len(text),len(keys)))
    #key_freq_title=[]
    for i in range(len(text)):
        #title_tokens.append(tokenize(split,len(data))[i].get('title'))
        abstract_tokens.append(tokenize(split,len(text))[i].get('abstract'))
    for j in range(len(text)):
        key_freq[j]=(find_keywords(1,abstract_tokens[j],key,freq_on)+find_keywords(2,abstract_tokens[j],key,freq_on)+find_keywords(3,abstract_tokens[j],key,freq_on)+find_keywords(4,abstract_tokens[j],key,freq_on))
        
    return key_freq

def save(name,output):
    with open(name+".npz",'wb') as f:
        sparse.save_npz(f,output)
    

if __name__ == "__main__":
    import time
    start_time = time.time()

    key=load_keys("KeyWords")
    q=0
    while (q < len(key)):
        key[q] = key[q].lower()
        q = q + 1
    
    data=load_data('/Users/parisa/Documents/inspires_project/inspire/small')
    split=split_text(data)
    #token=tokenize(split,len(data))[0].get('abstract')
    
    #print(find_keywords(1,token,key)+find_keywords(2,token,key))
    result1= key_tot(data,key,True)
    result2= key_tot(data,key,False)
    save('bag_of_keys',result2.tocsr())
    save('bag_of_keys_freq',result1.tocsr())
    
    
    
    print("--- %s seconds ---" % (time.time() - start_time))
