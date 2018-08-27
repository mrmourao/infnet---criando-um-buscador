# -*- coding: utf-8 -*-
"""
Created on Sat Aug 25 10:11:13 2018

@author: marcos.romero
"""
from inverted_index_generator import InvertedIndexGenerator
from os.path  import dirname, abspath, join
from math     import log2

from log_factory import Log
import logging
import time

#globals
PATH = dirname(abspath(__file__))
log = ''

class IndexerGenerator():
    
    def process():
        global log
        
        begin = time.time()
        
        # starting log
        logPath = join(PATH,"indexer","indexer.log")
        Log.setLog(__name__, logPath)
        log = logging.getLogger(__name__)
        
        log.info('Processing Indexer Generator Module...')
        
        log.info("loading the inverted index")
        inverted_index = InvertedIndexGenerator.getInvertedIndex(join(PATH,"InvertedIndex","InvertedIndex.csv"))
        
        log.info("create an auxiliary dictionary to help with calculations of tf-idf")
        all_docs = {}
        for termo, docs in inverted_index.items():
            for doc in docs:
                try:
                    all_docs[doc]["qte_termos_in_doc"] += 1
                    all_docs[doc]["termos"][termo]["qte_in_doc"] += 1
                except KeyError:
                    
                    try:
                        all_docs[doc]["termos"][termo] = {"qte_in_doc": 1}
                    except KeyError:
                        all_docs[doc] = {}
                        all_docs[doc]["qte_termos_in_doc"] = 1
                        all_docs[doc]["termos"] = {}
                        all_docs[doc]["termos"][termo] = {"qte_in_doc": 1}
                        
        indexer = {}
        
        log.info("Calculating values of tf * idf")
        for termo, docs in inverted_index.items():
            
            # log2( total of documents / total of documents that the term appears)
            idf = log2(len(all_docs.keys()) / float(len(set(docs))))
             
            indexer[termo] = {}
            for doc in docs:
                
                # number of times the terms appear in the document / total document terms
                tf = all_docs[doc]["termos"][termo]["qte_in_doc"] / float(all_docs[doc]["qte_termos_in_doc"])
                
                tf_ifd = 1 + log2(tf)*log2(idf)
                indexer[termo][doc] = {"tf_ifd":tf_ifd}
                 
        
        log.info('Writing Indexer on file...')
        ini = time.time()
        IndexerGenerator.saveIndexer(join(PATH,"indexer","indexer.csv"),indexer)
        
        timeElapsed = time.time()-ini
        log.info('Write operation finished with %s' % str(timeElapsed))
        
        end = time.time() - begin
        log.info('End of Indexer Generator Module. Total of %s elapsed.' % str(end))
        
    #--------------------------------------------------------------------------
    
    def saveIndexer(filepath, indexer):
        
        file = open(filepath, 'w')
        for key, value in indexer.items():
            file.write(key +";%s\n" % value)
        file.close()
