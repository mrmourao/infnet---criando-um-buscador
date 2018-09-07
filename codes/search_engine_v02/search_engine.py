# -*- coding: utf-8 -*-
""" @author: Marcos Romero Mourão """

#------------------------------------------------------------------------------    
# Import libraries

import logging
import time

from query_processor_generator import QueryProcessorGenerator
from inverted_index_generator  import InvertedIndexGenerator
from indexer_generator         import IndexerGenerator
from searcher_generator        import SearcherGenerator
from utils.log_factory         import Log
from os.path                   import dirname, abspath, join

#------------------------------------------------------------------------------    
# Globals variables
PATH = dirname(abspath(__file__))

#------------------------------------------------------------------------------    
# Main method
def main():
    
    # starting the time of application
    begin = time.time()
    
    # starting log
    logPath = join(PATH,"main.log")
    Log.setLog(__name__, logPath)
    log = logging.getLogger(__name__)
    log.info("System started")
    
    log.info("Reading the configuration file")
    # In this cfg you can choose each module will be run
    config = readConfig("main.cfg")
    
    if config["InvertedIndexGenerator"]:
        log.info("Calling inverted index generator ")
        ini = time.time()
        
        InvertedIndexGenerator.process()
        
        log.info('End of inverted index generator. Total of %s elapsed.' % str(time.time()-ini))
        
    if config["Indexer"]:
        log.info("Calling indexer generator ")
        ini = time.time()
        
        IndexerGenerator.process()
        
        log.info('End of indexer generator. Total of %s elapsed.' % str(time.time()-ini))
        
    if config["QueryProcessor"]:
        log.info("Calling query processor generator ")
        ini = time.time()
        
        QueryProcessorGenerator.process()
        
        log.info('End of query processor generator. Total of %s elapsed.' % str(time.time()-ini))
        
    if config["Searcher"]:
        log.info("Calling searcher generator ")
        ini = time.time()
        
        SearcherGenerator.process()
        
        log.info('End of searcher generator. Total of %s elapsed.' % str(time.time()-ini))
        
    end = time.time() - begin
    log.info('End of system. Total of %s elapsed.' % str(end))
    
#------------------------------------------------------------------------------    
# Auxiliary method

def readConfig(filepath):
    
    file = open(join(PATH,filepath))
    
    dic = {}
    for line in file:
        key, value = line.replace(" ","").split("=")
        dic[key] = (True if "True" in value else False)
           
    return dic

#------------------------------------------------------------------------------    
# Start main method

if __name__ == "__main__":
    main()

#------------------------------------------------------------------------------