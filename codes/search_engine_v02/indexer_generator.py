# -*- coding: utf-8 -*-
""" @author: Marcos Romero Mourão """

#------------------------------------------------------------------------------    
# Import libraries

import logging
import time

from inverted_index_generator import InvertedIndexGenerator
from log_factory              import Log
from os.path                  import dirname, abspath, join
from math                     import log2

#------------------------------------------------------------------------------    
#globals

PATH = dirname(abspath(__file__))
log = ''

#------------------------------------------------------------------------------    

class IndexerGenerator():
    
    def process():
        global log
        
        begin = time.time()
        
        # starting log
        logPath = join(PATH,"indexer","indexer.log")
        Log.setLog(__name__, logPath)
        log = logging.getLogger(__name__)
        
        log.info('Processing indexer generator Module...')
        
        log.info("Reading the configuration file")
        config = IndexerGenerator.readConfig(join(PATH,"indexer","index.cfg"))
        
        log.info("Loading the inverted index")
        ini = time.time()
        inverted_index = InvertedIndexGenerator.getInvertedIndex(PATH+config["LEIA"])
        log.info('%s records read succesfully.' % str(len(inverted_index)))
        log.info('Load operation finished with %s' % str(time.time()-ini))
        
        
        log.info("Creating an auxiliary dictionary to help with calculations of tf-idf")
        ini = time.time()
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
        
        log.info('Create operation finished with %s' % str(time.time()-ini))                
        
        indexer = {}
        
        log.info("Calculating values of tf * idf")
        ini = time.time()
        for termo, docs in inverted_index.items():
            
            # log2( total of documents / total of documents that the term appears)
            idf = log2(len(all_docs.keys()) / float(len(set(docs))))
             
            indexer[termo] = {}
            for doc in docs:
                
                # number of times the terms appear in the document / total document terms
                tf = all_docs[doc]["termos"][termo]["qte_in_doc"] / float(all_docs[doc]["qte_termos_in_doc"])
                
                tf_ifd = 1 + log2(tf)*log2(idf)
                indexer[termo][doc] = tf_ifd
        
        log.info('End of calculate tf-idf. Total of %s elapsed.' % str(time.time()-ini))         
        
        log.info('Writing Indexer on file...')
        ini = time.time()
        IndexerGenerator.saveIndexer(PATH+config["ESCREVA"],indexer)
        
        log.info('%s records created successfully.' % str(len(indexer)))
        log.info('Write operation finished with %s' % str(time.time()-ini))
        
        end = time.time() - begin
        log.info('End of indexer generator module. Total of %s elapsed.' % str(end))
        
#------------------------------------------------------------------------------
    
    def saveIndexer(filepath, indexer):
        
        file = open(filepath, 'w')
        for key, value in indexer.items():
            file.write(key +";%s\n" % value)
        file.close()

#------------------------------------------------------------------------------           
    
    def readConfig(filepath):
        
        file = open(join(PATH,filepath))
        
        dict_config = {}
        for line in file:
            key, value = line.replace(" ","").replace("\n","").split("=")
            dict_config[key] = value
            
        return dict_config

#------------------------------------------------------------------------------