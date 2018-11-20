from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import *
from openpyxl import Workbook
import mysql.connector
import os
import sys
import math
import time
import multiprocessing as mp


def getDirectoryOfDocument():
    '''
        This function will get the /document directory from current root folder to translate over
    '''
    dataDir = os.path.realpath('.') +'/document'
    dataFiles = os.listdir(dataDir)
    filesPath = []
    for files in dataFiles:
        filesPath.append(dataDir+"/"+files)
    return filesPath

def writeToDocuments(filesPath):
    '''
        This function will write the to /sentence directory from current root folder
    '''
    for path in filesPath:
        with open(path,"r",encoding="UTF-8",errors='ignore') as document:
            text = document.read()
        tokenized_text = sent_tokenize(text)
    for index,sentence in enumerate(tokenized_text):
        path = os.path.realpath('.')+'/sentence'
        docName = "/s" + str(index) + ".txt"
        docPath = path+docName
        with open(docPath, 'w') as document:
            document.write(sentence)


def getDirectoryOfSentence():
    '''
        This function will get the 'data' directory of current folder
    '''
    dataDir = os.path.realpath('.') +'/sentence'
    dataFiles = os.listdir(dataDir)
    filesPath = []
    for files in dataFiles:
        filesPath.append(dataDir+"/"+files)
    return filesPath

def main():
    filePaths = getDirectoryOfDocument()
    writeToDocuments(filePaths)
    sentencePath = getDirectoryOfSentence()
    for documents in sentencePath:
        print(documents)

main()
