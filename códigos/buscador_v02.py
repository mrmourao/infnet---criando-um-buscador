from nltk.corpus        import stopwords
from nltk.tokenize      import word_tokenize
from nltk.stem.porter   import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.probability   import FreqDist

from math     import log2

import re

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
def query(all_tokens, text):
    words = token_treated(text)
    fd = FreqDist(words)
    res = {}
    
    for w in set(words):
        calc = fd[w] / all_tokens[w]["qt_all_docs"] * all_tokens[w]["idf"]
        res[w] = calc
    
    print(res)
#------------------------------------------------------------------------------
def main():
    docs = {'d1': 'new york times','d2': 'new york post','d3': 'los angeles times'}
    
    all_key_docs = {}
    all_text = ''
    for key, value in docs.items():
        all_text += value + " "
        all_key_docs[key] = {"weight":0}
        
    all_words = token_treated(all_text)
    all_tokens = {}
    for word in all_words:
        try:
            qt = all_tokens[word]["qt_all_docs"]
            qt = qt + 1
            all_tokens[word]["qt_all_docs"] = qt
        except:
            opt = {}
            opt["qt_all_docs"] = 1
            all_tokens[word] = opt
        
        all_tokens[word]["idf"] = log2(len(docs.keys()) / all_tokens[word]["qt_all_docs"])
        
    
    for k_doc, v_doc in docs.items():
        words = token_treated(v_doc)
        fd = FreqDist(words)

        for w in set(words):
            itf = fd[w] #/ float(len(words)) # comentado temporariamente para ajustar ao exemplo
            all_tokens[w][k_doc] = { "itf": itf}
            print(k_doc,w,all_key_docs[k_doc], itf * all_tokens[w]["idf"])
            
    
    text = 'new new times'
    #query(all_tokens, text)
    #print(all_key_docs)
    #print(all_tokens)
    
#------------------------------------------------------------------------------
if __name__ == '__main__':
    main()