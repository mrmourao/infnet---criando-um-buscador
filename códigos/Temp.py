from nltk.corpus        import stopwords
from nltk.tokenize      import word_tokenize
from nltk.stem.porter   import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.probability   import FreqDist

from os       import listdir
from os.path  import isfile, join
from math     import log2
from datetime import datetime as dt

import re
import numpy  as np
import pandas as pd



def log(tx):
    print(dt.now() , tx)

#------------------------------------------------------------------------------
def get_doc(file):
    docs = {} 

    ab = False
    abkey = ""
    abvalue = ""

    for line in open(file):

        if(ab):
            if (line[:2] == "  "):
                abvalue += line[2:]
            else:
                ab = False
                docs[abkey.replace(" ","")] = abvalue.replace("\n","").lower()
        else:
            if (line[:2] == "RN"):
                abkey = line[2:].rstrip()
            
            elif (line[:2] == "AB"):
                abvalue = line[2:]
                ab = True
    return docs
    
#------------------------------------------------------------------------------
def get_all_docs(path_files):
    
    all_files = [f for f in listdir(path_files) if isfile(join(path_files, f))]
    
    all_docs = {}
    
    for file in all_files:
        all_docs.update(get_doc(join(path_files,file)))
        
    return all_docs
   
#------------------------------------------------------------------------------
def token_treated(tx):
    sw = set(stopwords.words('english'))
    sb = SnowballStemmer("english")
    ps = PorterStemmer()
    
    # removing all characters different of a-zA-Z
    tx = re.sub('[^a-zA-Z]',' ',tx)
    
    words = word_tokenize(tx)

    wf = []
    # removing stopwords and applying stemming
    for w in words:
        
        w = sb.stem(w)
        w = ps.stem(w)
        
        if w not in sw:
            wf.append(w)
   
    return wf

#------------------------------------------------------------------------------
def main():
    
    log("starting process...")
    
    path_files = 'D:\\git\\infnet-criando-um-buscador\\dados'
    
    inverted_index = {}
    
    #docs = get_all_docs(path_files)
    #docs = {"doc1":"Temer car bus driven travel bussines road","doc2":"Temer truck bus driven travel bussines highway"}
    docs = {'d1': 'new new york times','d2': 'new york post','d3': 'los angeles times'}
    
    tf = {}

    log("concating all text of all docs in just one")
    all_text = ''
    for key, value in docs.items():
        all_text += value + " "
        tf[key] = 0

    log("building all possible tokens")
    all_words = token_treated(all_text)

    # cleaning the memory
    del all_text

    log("building all possible keys")
    for w in all_words:
        inverted_index[w] = []

    # cleaning the memory
    del all_words

    log("listing all docs and append to de main dict...")
    for key, value in docs.items():
        
        # building tokens of document
        aw = token_treated(value)
        
        # counting words of document
        tf[key] =  len(aw)
        
        # adding the document on inverted index
        for w in aw:
            inverted_index[w].append(key)
            
        

    
    
    log("sorting the lists to build the df...")
    ix_docs = sorted(list(tf.keys()))
    col_tokens = sorted(list(inverted_index.keys()))
    
    log("building the idf's values...")
    idf = {}
    for key, value in inverted_index.items():
        print(key,value)
        idf["new"] = log2(len(ix_docs) / float(len(inverted_index["new"])))

    log("preparing the shape of df...")
    shape = (len(ix_docs),len(col_tokens))
    zeros = np.zeros(shape, dtype=int)
    
    log("building df...")
    df = pd.DataFrame(data=zeros,index=ix_docs,columns=col_tokens)
    
    log("calculating the values of tf and making rf * idf...")
    for i in ix_docs: # all df rowns
        for j in col_tokens: # all df columns 
            fd = FreqDist(inverted_index[j]) # counting frequence
            #df.loc[i,j] = (fd[i] / tf[i]) * float(idf[j])
            df.loc[i,j] =  fd[i] * float(idf[j])
    
    log("end process...")
    
    #df.to_csv("teste.csv")
    print(df.head())
    
    

#------------------------------------------------------------------------------
if __name__ == '__main__':
    main()