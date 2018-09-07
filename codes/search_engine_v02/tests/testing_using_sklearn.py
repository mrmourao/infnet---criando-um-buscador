# -*- coding: utf-8 -*-
""" @author: Marcos Romero Mourão """

#------------------------------------------------------------------------------    
# Import libraries

import pandas as pd

import csv
import ast

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from xml.dom.minidom      import parse
from os.path              import dirname, abspath
from nltk.corpus        import stopwords

PATH = dirname(abspath(__file__))

class Test():
    
    def main():
        
        path_gli = PATH+"\\invertedIndex\\gli.cfg"
        path_gli = path_gli.replace("tests\\","")
        
        config_docs = Test.readConfig(path_gli)
        docs = Test.get_all_docs(config_docs["LEIA"])
        
        p_queries = PATH+"\\queryProcessor\\consulta.csv"
        p_queries = p_queries.replace("tests\\","")
        queries = Test.getQueryFile(p_queries)
        
        
        documents = list(docs.values())
        
        for query in queries.keys():
            
            documents.insert(0, queries[query])
            
            tfidf_vectorizer = TfidfVectorizer()
            tfidf_matrix = tfidf_vectorizer.fit_transform(documents, stopwords)
            res = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1:])
            
            resultado = {}
            cnt = 0
            for k, v in docs.items():
                resultado[k] = res[0][cnt]
                cnt += 1
            
            #ordering the result of query
            resultado = [(k, resultado[k]) for k in sorted(resultado, key=resultado.get, reverse=True)]
            
            #putting the result in a dataframe
            df = pd.DataFrame(data=resultado, columns=["Document","Order"])
            
            filepath = PATH+"\\resultados.csv"
            Test.saveResult(filepath,query, df)
            documents.pop(0)
            
        
    
#------------------------------------------------------------------------------
    
    def readXML(filename):
        dictionary = {}
        DOMTree = parse(filename)
        collection = DOMTree.documentElement
        
        records = collection.getElementsByTagName("RECORD")
        
        for record in records:
            recordNumber = str(record.getElementsByTagName('RECORDNUM')[0].childNodes[0].data).strip()
            
            
            try:
                dictionary[recordNumber] = record.getElementsByTagName('ABSTRACT')[0].childNodes[0].data
            except IndexError:
                try:
                    dictionary[recordNumber] = record.getElementsByTagName('EXTRACT')[0].childNodes[0].data
                except IndexError:
                    pass
        
                   
        return dictionary
    
#------------------------------------------------------------------------------
    
    def get_all_docs(list_of_files):
        all_docs = {}
        
        for file in list_of_files:
            p = (PATH+file).replace("tests\\","")
            dict_xml = Test.readXML(p)
            all_docs.update(dict_xml)
                                  
        return all_docs
    
#------------------------------------------------------------------------------
    
    def saveInvertedIndex(filepath, invertedIndex):
        
        file = open(filepath, 'w')
        for key, value in invertedIndex.items():
            file.write(key +";%s\n" % value)
        file.close()
        
#------------------------------------------------------------------------------
    
    def getInvertedIndex(filepath):
        dictionary = {}
        with open(filepath, 'r') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';')
            for row in spamreader:
                dictionary[row[0]] = ast.literal_eval(row[1])
        
        return dictionary
        
#------------------------------------------------------------------------------
        
    def readConfig(filepath):
        
        file = open(filepath)
        
        dict_config = {}
        for line in file:
            key, value = line.replace(" ","").replace("\n","").split("=")
            
            if key == 'LEIA':
                try:
                    dict_config[key].append(value)
                except KeyError:
                    dict_config[key] = [value]
            
            if key == 'ESCREVA':
                dict_config[key] = value
            
        return dict_config
    
#------------------------------------------------------------------------------    
    
    def getQueryFile(filepath):
        
        dictionary = {}
        with open(filepath, 'r') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';')
            for row in spamreader:
                dictionary[row[0]] = row[1]
        
        return dictionary    

#------------------------------------------------------------------------------     

    def saveResult(filepath,num_query, df):
        file = open(filepath, 'a')
        
        for key, obj in df.iterrows():
            file.write(num_query +";%s\n" % [key+1,obj.Document,obj.Order])
        file.close()

#------------------------------------------------------------------------------ 

Test.main()