from nltk.corpus        import stopwords
from nltk.tokenize      import word_tokenize
from nltk.stem.porter   import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.probability   import FreqDist

from os       import listdir
from os.path  import isfile, join
from math     import log2, sqrt
from datetime import datetime as dt

import re
import pandas as pd

#------------------------------------------------------------------------------

def log(tx):
    print(dt.now() , tx)

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

def get_docs(file):
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
        all_docs.update(get_docs(join(path_files,file)))
        
    return all_docs

#------------------------------------------------------------------------------
def get_cosine_similarity(docs,query):
    
    log("concatenating all text of all docs in just one")
    all_key_docs = {}
    all_text = ''
    
    for key, value in docs.items():
        all_text += value + " "
        
        #initializing "length" of each documents
        all_key_docs[key] = {"length":0}
        
    
    log("getting all possible words of all texts")
    all_words = token_treated(all_text)
    
    log("building all possible tokens, counting words of each documents, and calculating values to 'idf'")
    all_tokens = {}
    for word in all_words:
        try:
            #if exists the key "qt_all_docs", is add more one value
            qt = all_tokens[word]["qt_all_docs"]
            qt = qt + 1
            all_tokens[word]["qt_all_docs"] = qt
        except:
            #if not, the "qt_all_docs" is created and initialized
            all_tokens[word] = {"qt_all_docs": 1}
        
        #calculating value to "idf" of document
        all_tokens[word]["idf"] = log2(len(docs.keys()) / all_tokens[word]["qt_all_docs"])
        
    log("calculating 'tf', 'idf_tf', and 'length' of each document")
    for k_doc, v_doc in docs.items():
        words = token_treated(v_doc)
        fd = FreqDist(words)

        for w in set(words):
            tf = fd[w] / float(len(words))
            idf_tf = tf * all_tokens[w]["idf"]
            all_tokens[w][k_doc] = {"tf": tf, "tf-idf": idf_tf}
            all_key_docs[k_doc]["length"] += idf_tf ** 2
        
        all_key_docs[k_doc]["idf_tf"] = sqrt(all_key_docs[k_doc]["length"])
        
    words = token_treated(query)
    fd = FreqDist(words)
    res = {}
    res["length"] = 0
    
    log("calculating 'length' of query ")
    for w in set(words):
        calc = fd[w] / all_tokens[w]["qt_all_docs"] * all_tokens[w]["idf"]
        
        res[w] = {"tf-idf": calc}
        
        res["length"] += calc ** 2
    res["length"] = sqrt(res["length"])
    
    
    log("calculating cosine")
    cosSim = {}
    for doc in all_key_docs.keys():
        for word in set(words):
            try:
                try:
                    cosSim[doc] += res[word]["tf-idf"] * all_tokens[word][doc]["tf-idf"]
                except:
                    cosSim[doc] = res[word]["tf-idf"] * all_tokens[word][doc]["tf-idf"]
            except:
                pass
    
    for doc in cosSim.keys():
        cosSim[doc] = cosSim[doc] / (all_key_docs[doc]["length"] * res["length"])
        
    #ordering the result of query
    cosSim = [(k, cosSim[k]) for k in sorted(cosSim, key=cosSim.get, reverse=True)]
    
    #putting the result in a dataframe
    df = pd.DataFrame(data=cosSim, columns=["Document","Order"])
        
    return df
#------------------------------------------------------------------------------

def get_jaccard_similarity(docs, query):
    jacSim = {}
    words_query = set(token_treated(query))
    
    log("calculating jaccard")
    for key, value in docs.items():
        words_docs = set(token_treated(value))
        intersect = words_query.intersection(words_docs)
        union = words_query.union(words_docs)
        
        jacSim[key] = len(intersect)/ float(len(union))
    
    #ordering the result of query
    jacSim = [(k, jacSim[k]) for k in sorted(jacSim, key=jacSim.get, reverse=True)]
    
    #putting the result in a dataframe
    df = pd.DataFrame(data=jacSim, columns=["Document","Order"])
    
    return df

#------------------------------------------------------------------------------

def main():
    
    log("starting the process...")
    
    path_files = 'D:\\git\\infnet-criando-um-buscador\\dados'
    
    log("getting all documents...")
    docs = get_all_docs(path_files)
    
    #used for test "cosine_tf_idf_example.pdf"
    #docs = {'d1': 'new york times','d2': 'new york post','d3': 'los angeles times'}
        
    log("testing query")
        
    #put here the text of consult
    query = 'new new times'
    
    
    log("printing the result")
    
    
    cosine_similarity = get_cosine_similarity(docs,query)
    
    print('-'*50)
    print(cosine_similarity.head(10))
    print('-'*50)
    
    jaccard_similarity = get_jaccard_similarity(docs,query)
    
    print('-'*50)
    print(jaccard_similarity.head(10))
    print('-'*50)
    
    log("end process...")
    
    
#------------------------------------------------------------------------------
if __name__ == '__main__':
    main()