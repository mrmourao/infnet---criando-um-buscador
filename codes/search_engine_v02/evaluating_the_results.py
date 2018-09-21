# -*- coding: utf-8 -*-
""" @author: Marcos Romero Mourão """

#------------------------------------------------------------------------------    
# Import libraries

import matplotlib.pyplot as plt
import csv, ast

from os.path import dirname, abspath, join

#------------------------------------------------------------------------------    
# Globals variables
PATH = dirname(abspath(__file__))

#------------------------------------------------------------------------------    
# Main method
def main():
    
    path_expected = join(PATH,"queryProcessor","resultados.csv")
    path_result = join(PATH,"searcher","resultados.csv")
    
    
    dic_expected = {}
    with open(path_expected, 'r') as csvfile:
        file = csv.reader(csvfile, delimiter=';')
        for row in file:
            dic_expected[row[0]] = ast.literal_eval(row[1])
            
    dic_result = {}
    with open(path_result, 'r') as csvfile:
        file = csv.reader(csvfile, delimiter=';')
        for row in file:
            dic_result[row[0]] = ast.literal_eval(row[1])
            
    result_query = getPrecisionRecall(dic_expected,dic_result)
    
    result_query_red = getInterpolationPoints(result_query)
    
    getPlots(result_query)

#------------------------------------------------------------------------------    

# if wants to use Precision @ K, just set k value
def getPrecisionRecall(dic_expected,dic_result, k= -1):
    
    result_query = {}
    for query_number, doc_list in dic_result.items():
        result_query[query_number] = {}
        result_query[query_number]["precision"] = []
        result_query[query_number]["recall"] = []
        
        list_expected = []
        
        for score,doc in dic_expected[query_number]:
            list_expected.append(doc)
        
        qt_item = 1
        qt_right = 0
        
        for doc in doc_list:
            doc_number = str(int(doc[0]))
            precision = 0
            recall = 0
            
            if doc_number in list_expected:
                qt_right += 1
            
            precision = qt_right / qt_item
            recall = qt_right / len(list_expected)
            result_query[query_number]["precision"].append(precision)  
            result_query[query_number]["recall"].append(recall)
            
            if not(qt_item <= k or k == -1):
                break
            qt_item += 1
    
    return result_query

#------------------------------------------------------------------------------

def getInterpolationPoints(result_query):
    res_query_red = {}
    
    for query, result in result_query.items():
        res_query_red[query] = {}
        res_query_red[query]["precision"] = []
        res_query_red[query]["recall"] = []
        
        for pos in range(1,11):
            try:
                res_query_red[query]["precision"].append(result["precision"][pos * 10])
            except Exception as e:
                break
            
            try:
                res_query_red[query]["recall"].append(result["recall"][pos * 10])
            except Exception as e:
                break
    return res_query_red
#------------------------------------------------------------------------------       

def getPlots(result_query):
    
    for query,result in result_query.items():
        precision = result["precision"]
        recall = result["recall"]
        
        plt.figure()
        plt.step(recall, precision, color='b', alpha=0.2, where='post')
        plt.fill_between(recall, precision, step='post', alpha=0.2, color='b')
        
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.ylim([0.0, 1.05])
        plt.xlim([0.0, 1.0])
        plt.title('Busca para a query '+query)
        
        plt.savefig(join(PATH,"images",query+'.png'))

#------------------------------------------------------------------------------    
# Start main method

if __name__ == "__main__":
    main()

#------------------------------------------------------------------------------
