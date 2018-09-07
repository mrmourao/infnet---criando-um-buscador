# -*- coding: utf-8 -*-
""" @author: Marcos Romero Mourão """

#------------------------------------------------------------------------------    
# Import libraries

import pandas   as pd

from utils.text_treatment      import Text
from nltk.probability          import FreqDist
from math                      import sqrt,log2

#------------------------------------------------------------------------------    

class VectorModel():
    
    def getCosineSimilarity(indexer,query):
                
        # building all terms from query
        terms_query = Text.token_treated(query)
        fd = FreqDist(terms_query)
        
        
        # calculating tf-idf to query
        res = {}
        for term in set(terms_query):
            frequence = fd[term]
            idf = 1
            try:
                idf = indexer[term]["idf"]
            except:
                pass
            tf = (frequence / len(terms_query))
            tf_idf = 1 + log2(tf)*log2(idf)
            res[term] =   tf_idf
        
        # calculating the weight for query
        weight_query = 0.0
        for k, v in res.items():
            weight_query += v ** 2
                        
        weight_query = sqrt(weight_query)
        
        
        # sum all tf-idf by document
        all_docs = {}
        for term, docs in indexer.items():
            for doc, values in docs.items():
                if doc == 'idf':
                    continue
                try:
                    all_docs[doc] += (values ** 2)
                except:
                    all_docs[doc] = (values ** 2)
        
        # calculating the weight for documents
        weight_docs = {}
        for doc, weight in all_docs.items():
            weight_docs[doc] = sqrt(weight)
            
        
        # calculating the similarity
        end_result = {}
        for doc, weight in weight_docs.items():
            total = 0.0
            for term, value in res.items():
                try:
                    total += value * indexer[term][doc]
                except:
                    pass
                
            r = total / (weight * weight_query)
            if r >= 0.01:
                end_result[doc] = r
            
            
        #ordering the result of query
        end_result = [(k, end_result[k]) for k in sorted(end_result, key=end_result.get, reverse=True)]
    
        #putting the result in a dataframe
        df = pd.DataFrame(data=end_result, columns=["Document","Order"]) 
        
        return df