# -*- coding: utf-8 -*-
""" @author: Marcos Romero Mourão """

#-----------------------------------------------------------------------------#    
# Import libraries

from nltk.corpus        import stopwords
from nltk.tokenize      import word_tokenize
from nltk.stem.porter   import PorterStemmer
from nltk.stem.snowball import SnowballStemmer

from xml.dom.minidom import parse
from log_factory import Log

import logging
import time
import csv
import re
import ast

from os       import listdir
from os.path  import isfile, join, dirname, abspath

#-----------------------------------------------------------------------------#    
# Globals variables
PATH = dirname(abspath(__file__))
log = ''

class InvertedIndexGenerator():
    
    #--------------------------------------------------------------------------  
    
    def process():
        global log
        
        begin = time.time()
        
        # starting log
        logPath = join(PATH,"invertedIndex","inverted_index.log")
        Log.setLog(__name__, logPath)
        log = logging.getLogger(__name__)
        
        log.info('Processing Inverted Index Generator Module...')
        
        inverted_index = {}
    
        docs = InvertedIndexGenerator.get_all_docs(join(PATH,"data"))
        
        log.info("concating all text of all docs in just one")
        all_text = ''
        for key, value in docs.items():
            all_text += value + " "
       
        log.info("building all possible tokens")
        all_words = InvertedIndexGenerator.token_treated(all_text)
    
        log.info("building all possible keys")
        for w in all_words:
            inverted_index[w] = []
    
        log.info("listing all docs and append to de main dict...")
        for key, value in docs.items():
            
            # building tokens of document
            aw = InvertedIndexGenerator.token_treated(value)
            
            # add the document on inverted index
            for w in aw:
                inverted_index[w].append(key)
        
        log.info('Writing Inverted Index on file...')
        ini = time.time()
        InvertedIndexGenerator.saveInvertedIndex(join(PATH,"InvertedIndex","InvertedIndex.csv"),inverted_index)
        
        timeElapsed = time.time()-ini
        log.info('Write operation finished with %s' % str(timeElapsed))
        
        end = time.time() - begin
        log.info('End of Inverted Index Generator Module. Total of %s elapsed.' % str(end))
    
    #--------------------------------------------------------------------------
    def readXML(filename):
        log.info('Reading '+filename+' file')
        
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
                    log.warning("Document["+recordNumber+"] doesn't have abstract neither extract!")
        
        log.info('%s records read succesfully.' % str(len(dictionary)))
        
        return dictionary
    
    #--------------------------------------------------------------------------
    
    def get_all_docs(path_files):
    
        all_files = [f for f in listdir(path_files) if isfile(join(path_files, f))]
        
        all_docs = {}
        
        for file in all_files:
            dict_xml = InvertedIndexGenerator.readXML(join(path_files,file))
            all_docs.update(dict_xml)
            
        return all_docs
    
    #--------------------------------------------------------------------------
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
    
    #--------------------------------------------------------------------------
    
    def saveInvertedIndex(filepath, invertedIndex):
        
        file = open(filepath, 'w')
        for key, value in invertedIndex.items():
            file.write(key +";%s\n" % value)
        file.close()
        
    #-------------------------------------------------------------------------- 
    
    def getInvertedIndex(filepath):
        dictionary = {}
        with open(filepath, 'r') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';')
            for row in spamreader:
                dictionary[row[0]] = ast.literal_eval(row[1])
        
        return dictionary
    
    #--------------------------------------------------------------------------           
    
    
        