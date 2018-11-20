from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import *
from openpyxl import Workbook
import mysql.connector
import os
import sys
import math
import time
import multiprocessing as mp


def getDirectoryOfData():
    '''
        This function will get the 'sentence' directory of current folder
    '''
    dataDir = os.path.realpath('.') +'/sentence'
    dataFiles = os.listdir(dataDir)
    filesPath = []
    for files in dataFiles:
        filesPath.append(dataDir+"/"+files)
    return filesPath

class TokenizerSentence(object):
    '''
        This class will store all the data into a dictionary. However, before running this
        make a folder called sentence and document. Then proceed to run SentenceSeparator.py.
        Then run this file or else you're going to be going insane.
    '''
    def __init__(self,file_paths):
        '''
            This initalizes the TokenizerSentenceClass.

            Class Variables:
            __data format:
             { Document0: {token1: total token count in doc,
                             token2: count,
                             token3: count,
                             ...
                         }
               Document1: {token1: count,
                               token2: count,
                               token3: count,
                               ...
                           }
             }

             __tfdata format:
              { Document0: {token1:tf,
                              token2: tf,
                              token3: tf,
                              ...
                          }
                Document1: {token1: tf,
                                token2: tf,
                                token3: tf,
                                ...
                            }
              }

            __totalWordsPerDoc format:
            [count1, count2,etc...]
        '''
        self.__file_paths=file_paths
        self.__data={}
        self.__tfdata={}
        self.__totalWordsPerDoc = []


    def run(self):
        self.getData(self.__file_paths)
        total_docs = len(self.__totalWordsPerDoc)
        for count in total_docs:
            getTFDataInDoc(count)




    def getTFDataInDoc(self,document_word_count):
        for key,value in self.__data.items():
            for key,value in value.items():
                self.__calculate_tf(value,document_word_count)


    def getData(self, filePaths):
        for index,path in enumerate(filePaths):
            with open(path,"r",encoding="UTF-8",errors='ignore') as document:
                sentence = document.read()
            length = len(sentence.split(" "))
            self.__totalWordsPerDoc.append(length)
            # print('Document' + str(index))
            dictionary = self.store_data_into_dict(sentence,length)
            docName = 'Document' + str(index)
            self.__data[docName] = dictionary
        return self.__data







    def store_data_into_dict(self,sentence,length):
        '''
            Store stem word, Token position, document id, and TF into class variable dictionary
            What is stored during this operation:
                { Document: {token1: count,
                             token1: count,
                             token1: count,
                            }
                }

            Parameters:
                sentence (String): The sentence to store with paired words
        '''
        dictionary = {}
        # print(sentence)
        words = sentence.split(" ")
        for index,word in enumerate(words):
            # print('Word' + ":" + word)
            nextWordIndex = index+1
            for i in range(nextWordIndex,length):
                pair = word + " " + words[i]
                # print('Pair' +":" + pair)
                if pair in dictionary:
                    dictionary[pair] = dictionary.get(pair) + 1
                else:
                    dictionary[pair] = 1
        return dictionary




    def __calculate_tf(self,total_tokens,document_word_count):
        '''
            Calculates the token frequency (TF) in a document

            Parameters:
                total_tokens (int): the total amount of that specific word
                in a document that appeared

                document_word_count (int): the total word count in current document

            Return:
                (int) : Token Frequency Calculation
        '''
        return total_tokens/document_word_count




    def __calculate_df(self,total_num_of_doc, num_of_doc_with_token):
        '''
            Calculates the document frequency (DF)

            Parameters:
                total_num_of_doc (int): the total amount of documents

                num_of_doc_with_tokens (int): the total documents containing the token

            Return:
                (int) : Document frequency calculation
        '''
        return math.log(total_num_of_doc/num_of_doc_with_token) * 1.0


    def __calculate_tfidf(self,tf_value, df_value):
        '''
            Calculates the TFiDF to find key words

            Parameters:
                tf_value (int): Token frequency
                df_value (int): Document Frequency

            Return:
                (int) : TFiDF Calculation
        '''
        return tf_value * df_value



def main():
    data_path = getDirectoryOfData()
    tokenizersent1 = TokenizerSentence(data_path)
    data = tokenizersent1.run()
    for key,value in data.items():
        print(key + ": " + str(value))

main()
