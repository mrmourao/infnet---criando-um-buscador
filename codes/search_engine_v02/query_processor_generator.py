# -*- coding: utf-8 -*-
""" @author: Marcos Romero Mourão """

#------------------------------------------------------------------------------    
# Import libraries

import unidecode
import logging
import time
import csv

from utils.log_factory import Log
from xml.dom.minidom   import parse
from os.path           import dirname, abspath, join

#------------------------------------------------------------------------------
# Globals variables
PATH = dirname(abspath(__file__))
log = ''

#------------------------------------------------------------------------------

class QueryProcessorGenerator():
    
    def process():
        global log
        
        begin = time.time()
        
        # starting log
        logPath = join(PATH,"queryProcessor","query_processor.log")
        Log.setLog(__name__, logPath)
        log = logging.getLogger(__name__)
        
        log.info('Processing query processo generator module...')
        
        log.info("Reading the configuration file")
        config = QueryProcessorGenerator.readConfig(join(PATH,"queryProcessor","pc.cfg"))
        
        log.info("Getting all queries from xml files")
        queries, meanTimeXML = QueryProcessorGenerator.get_all_queries(config["LEIA"])
        log.info('XML reading operation finished with %s of time average.' % str(meanTimeXML))
        
        log.info('Writing files...')
        ini = time.time()
        QueryProcessorGenerator.saveFiles(config,queries)
        
        log.info('Write operation finished with %s' % str(time.time()-ini))
        
        log.info('End of query processor generator module. Total of %s elapsed.' % str(time.time() - begin))
        
#------------------------------------------------------------------------------
    
    def saveFiles(config, dic):
        path_query = PATH+config["CONSULTAS"]
        path_result = PATH+config["RESULTADOS"]
        
        file_query = open(path_query, 'w')
        file_result = open(path_result, 'w')
        for key, value in dic.items():
            
            # writing file query
            tx = value["query"].replace("\n","")
            tx = tx.replace("   "," ")
            tx = tx.lower()
            tx = unidecode.unidecode(tx)
            file_query.write(key +";%s\n" % tx)
            
            # writing file result
            file_result.write(key +";%s\n" % value["result"])
            
        file_query.close()
        file_result.close()

#------------------------------------------------------------------------------           
    
    def readConfig(filepath):
        file = open(join(PATH,filepath))

        dict_config = {}
        for line in file:
            key, value = line.replace(" ","").replace("\n","").split("=")
            
            if key == 'LEIA':
                try:
                    dict_config[key].append(value)
                except KeyError:
                    dict_config[key] = [value]
            else:
                dict_config[key] = value
            
        return dict_config

#------------------------------------------------------------------------------
        
    def readXML(filename):
        log.info('Reading '+filename+' file')
        
        dictionary = {}
        DOMTree = parse(filename)
        collection = DOMTree.documentElement
        
        queries = collection.getElementsByTagName("QUERY")
        
        for query in queries:
            queryNumber = str(query.getElementsByTagName('QueryNumber')[0].childNodes[0].data).strip()
            
            dictionary[queryNumber] = {}
            try:
                dictionary[queryNumber]["query"] = query.getElementsByTagName('QueryText')[0].childNodes[0].data
            except IndexError:
                log.warning("Query["+queryNumber+"] doesn't have the tag queryText!")
            
            try:
                    
                items = query.getElementsByTagName("Item")
                
                dictionary[queryNumber]["result"] = []
    
                for item in items:
                    score =item.getAttribute("score")
                    document = item.firstChild.nodeValue
                    dictionary[queryNumber]["result"].append((score,document))
            except Exception as e:
                log.warning("Query["+queryNumber+"] had an exception when tried to get item!")
                
        log.info('%s records read succesfully.' % str(len(dictionary)))
        
        return dictionary
    
#--------------------------------------------------------------------------
    
    def get_all_queries(list_of_files):
        meanTimeXML = 0
    
        all_queries = {}
        for file in list_of_files:
            ini = time.time()
            dict_xml = QueryProcessorGenerator.readXML(PATH+file)
            all_queries.update(dict_xml)
            meanTimeXML+=time.time()-ini
                                  
        return all_queries, (meanTimeXML / float(len(list_of_files)))
    
#------------------------------------------------------------------------------
    
    def getQueryFile(filepath):
        
        dictionary = {}
        with open(filepath, 'r') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';')
            for row in spamreader:
                dictionary[row[0]] = row[1]
        
        return dictionary
    
#------------------------------------------------------------------------------
