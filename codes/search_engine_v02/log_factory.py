# -*- coding: utf-8 -*-
"""
Created on Sat Aug 25 10:08:02 2018

@author: marcos.romero
"""
import logging

class Log():
    
    def setLog(name, logFile):
        
        logger = logging.getLogger(name)
        
        if (logger.hasHandlers()):
            logger.handlers.clear()
            
        logger.setLevel(logging.INFO)
        # create a file handler
        handler = logging.FileHandler(logFile)
        handler.setLevel(logging.INFO)
        # create a logging format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)
        # add the handlers to the logger
        logger.addHandler(handler)
        logger.addHandler(streamHandler)