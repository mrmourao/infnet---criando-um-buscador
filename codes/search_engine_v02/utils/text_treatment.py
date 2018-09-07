# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------    
# Import libraries

import re

from nltk.stem.snowball import SnowballStemmer
from nltk.stem.porter   import PorterStemmer
from nltk.corpus        import stopwords
from nltk.tokenize      import word_tokenize

class Text():
    
    def token_treated(tx):
        sw = set(stopwords.words('english'))
        sb = SnowballStemmer("english")
        ps = PorterStemmer()
        
        # removing all characters different of a-zA-Z and keeping '-' for compound words
        tx = re.sub('[^a-zA-Z\-]',' ',tx)
        
        words = word_tokenize(tx)
    
        wf = []
        # removing stopwords and applying stemming
        for w in words:
            
            # removing words with less of 2 characters
            if len(w.replace("-","")) < 3:
                continue
            
            w = w.lstrip( "-" )
            w = w.rstrip( "-" )
            
            w = sb.stem(w)
            w = ps.stem(w)
            
            if w not in sw:
                wf.append(w)
       
        return wf