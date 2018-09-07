# -*- coding: utf-8 -*-
""" @author: Marcos Romero Mourão """

#------------------------------------------------------------------------------    
# Import libraries

import logging
import time

from query_processor_generator import QueryProcessorGenerator
from indexer_generator         import IndexerGenerator
from utils.log_factory         import Log
from vector_models             import VectorModel
from os.path                   import dirname, abspath, join

#------------------------------------------------------------------------------    
# Globals variables
PATH = dirname(abspath(__file__))
log = ''

#------------------------------------------------------------------------------ 

class SearcherGenerator():
    
    def process():
        global log
        
        begin = time.time()
        
        # starting log
        logPath = join(PATH,"searcher","searcher.log")
        Log.setLog(__name__, logPath)
        log = logging.getLogger(__name__)
        
        log.info('Processing searcher generator module...')
        
        log.info("Reading the configuration file")
        config = SearcherGenerator.readConfig(join(PATH,"searcher","busca.cfg"))
        
        log.info("Loading indexer file")
        ini = time.time()
        indexer = IndexerGenerator.getIndexer(PATH+config["MODELO"])
        log.info('%s records read succesfully.' % str(len(indexer)))
        log.info('Load operation finished with %s' % str(time.time()-ini))
        
        log.info("Loading query file")
        ini = time.time()
        queries = QueryProcessorGenerator.getQueryFile(PATH+config["CONSULTAS"])
        log.info('%s records read succesfully.' % str(len(queries)))
        log.info('Load operation finished with %s' % str(time.time()-ini))
        
        log.info("Calculating the cosine similarity")
        ini = time.time()
        cnt = 0
        accumulated = 0
        
        for query in queries.keys():
            ini_y = time.time()
            df = VectorModel.getCosineSimilarity(indexer,queries[query])
            SearcherGenerator.saveResult(PATH+config["RESULTADOS"],query,df)
            accumulated += time.time() - ini_y
            cnt += 1
                                        
        log.info('Method cosine similarity  operation finished with %s of time average by query.' % str(accumulated / cnt))
        log.info('End of calculate the cosine similarity. Total of %s elapsed.' % str(time.time()-ini))
        
        log.info('End of searcher generator module. Total of %s elapsed.' % str(time.time()-begin))
        
#------------------------------------------------------------------------------
    
    def readConfig(filepath):
        
        file = open(join(PATH,filepath))
        
        dict_config = {}
        for line in file:
            key, value = line.replace(" ","").replace("\n","").split("=")
            dict_config[key] = value
            
        return dict_config

#------------------------------------------------------------------------------

    def saveResult(filepath,num_query, df):
        file = open(filepath, 'a')
        
        for key, obj in df.iterrows():
            file.write(num_query +";%s\n" % [key+1,obj.Document,obj.Order])
        file.close()
        
#------------------------------------------------------------------------------