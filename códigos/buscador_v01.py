from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer

from os import listdir
from os.path import isfile, join

# used to clear text
import re

def get_doc(file):
    docs = {} 

    ab = False
    abkey = ""
    abvalue = ""

    for line in open(file):

        if(ab):
            if (line[:2] == "  "):
                abvalue += line[2:]
            else:
                ab = False
                docs[abkey.replace(" ","")] = abvalue.replace("\n","").lower()
        else:
            if (line[:2] == "RN"):
                abkey = line[2:].rstrip()
            
            elif (line[:2] == "AB"):
                abvalue = line[2:]
                ab = True
    return docs
    

def get_all_docs(path_files):
    
    all_files = [f for f in listdir(path_files) if isfile(join(path_files, f))]
    
    all_docs = {}
    
    for file in all_files:
        all_docs.update(get_doc(join(path_files,file)))
        
    return all_docs
   

def token_treated(tx):
    sw = set(stopwords.words('english'))
    sb = SnowballStemmer("english")
    ps = PorterStemmer()
    
    # removing all characters different of a-zA-Z
    tx = re.sub('[^a-zA-Z]',' ',tx)
    
    words = word_tokenize(tx)

    wf = []
 
    for w in words:
        
        w = sb.stem(w)
        w = ps.stem(w)
        
        if w not in sw:
            wf.append(w)
   
    return wf


def main():
    
    path_files = 'D:\\git\\infnet-criando-um-buscador\\dados'
    
    final = {}
    
    docs = get_all_docs(path_files)

    # concating all text of all docs in just one
    all_text = ''
    for key, value in docs.items():
        all_text += value

    # building all possible tokens
    all_words = token_treated(all_text)

    # cleaning the memory
    del all_text

    # building all possible keys
    for w in all_words:
        final[w] = []

    # cleaning the memory
    del all_words

    # listing all docs and append to de main dict
    for key, value in docs.items():
        
        # building token of document
        aw = token_treated(value)
        
        # add to final document
        for w in aw:
            final[w].append(key)

    print(final["antibiot"])


if __name__ == '__main__':
    main()