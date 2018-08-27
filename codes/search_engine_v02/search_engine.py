# -*- coding: utf-8 -*-
""" @author: Marcos Romero Mourão """

#-----------------------------------------------------------------------------#    
# Import libraries
from os.path import dirname, abspath, join
from log_factory import Log

import logging
import time
from inverted_index_generator import InvertedIndexGenerator
from indexer_generator import IndexerGenerator


#-----------------------------------------------------------------------------#    
# Globals variables
PATH = dirname(abspath(__file__))

#-----------------------------------------------------------------------------#    
# Main method
def main():
    # starting the time of process
    begin = time.time()
    
    # starting log
    logPath = join(PATH,"main.log")
    Log.setLog(__name__, logPath)
    log = logging.getLogger(__name__)
    log.info("System started")
    
    # In this cfg you can choose each module will be run
    main_config = readConfig("main.cfg")
    
    if main_config["InvertedIndexGenerator"]:
        InvertedIndexGenerator.process()
        
    if main_config["Indexer"]:
        IndexerGenerator.process()
        
    if main_config["QueryProcessor"]:
        print("QueryProcessor")
        
    if main_config["Searcher"]:
        print("Searcher")
        
    end = time.time() - begin
    log.info('End of System. Total of %s elapsed.' % str(end))
    
#-----------------------------------------------------------------------------#    
# Auxiliary method

def readConfig(filepath):
    
    file = open(join(PATH,filepath))
    
    dic = {}
    for line in file:
        key, value = line.replace(" ","").split("=")
        dic[key] = (True if "True" in value else False)
           
    return dic

#-----------------------------------------------------------------------------#    
# Start main method
if __name__ == "__main__":
    main()