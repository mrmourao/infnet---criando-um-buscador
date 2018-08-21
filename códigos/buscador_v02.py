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
def main():
    docs = {'d1': 'new york times','d2': 'new york post','d3': 'los angeles times'}
    
    all_text = ''
    for key, value in docs.items():
        all_text += value + " "
        
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
        
    all_text = ''
    
    for k_doc, v_doc in docs.items():
        words = token_treated(v_doc)
        fd = FreqDist(words)
        
        #for k_tk, v_tk in all_tokens.items():
            
        for w in words:
            #print(k_doc,w, fd[w], len(words), fd[w] / float(len(words)))
            all_tokens[word][k_doc] = fd[w] / float(len(words))

    
    #all_tokens["new"]["teste"] = 1245
    #fd = FreqDist(all_tokens)
    #print(all_words)
    #    fd = FreqDist(all_words)
    print(all_tokens["new"])
    
#------------------------------------------------------------------------------
if __name__ == '__main__':
    main()