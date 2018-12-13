from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import *
import os
import sys
import math
import time


def getDirectoryOfDocument(folder):
    '''
        This function will get the /document directory from current root folder to translate over
    '''
    dataDir = os.path.realpath('.') +'/' + folder
    dataFiles = os.listdir(dataDir)
    filesPath = []
    for files in dataFiles:
        filesPath.append(dataDir+"/"+files)
    return filesPath

def writeToDocuments(filesPath,name,txt_branch_name):
    '''
        This function will write the to /sentence directory from current root folder
    '''
    for path in filesPath:
        with open(path,"r",errors='ignore') as document:
            print(path)
            text = document.read()
        tokenized_text = sent_tokenize(text)
        for index,sentence in enumerate(tokenized_text):
            path = os.path.realpath('.')+'/' + name
            if not os.path.exists(path):
                os.makedirs(path)
            docName = "/"+ txt_branch_name + str(index) + ".txt"
            docPath = path+docName
            with open(docPath, 'w') as document:
                document.write(sentence)


def getDirectoryOfSentence(folder):
    '''
        This function will get the 'data' directory of current folder
    '''
    dataDir = os.path.realpath('.') +'/' + folder
    dataFiles = os.listdir(dataDir)
    filesPath = []
    for files in dataFiles:
        filesPath.append(dataDir+"/"+files)
    return filesPath



def main(folder,name,txt_branch_name):
    filePaths = getDirectoryOfDocument(folder)
    writeToDocuments(filePaths,name,txt_branch_name)
    sentencePath = getDirectoryOfSentence(name)
    for documents in sentencePath:
        print(documents)


folder = input("Which data folder would you like to run to separate files in sentences? /separate\n")
name = input("What would you like to name the folder with the results?\n")
txt_branch_name = input("What would you like to name the text files?\n")
print("Separating data from folder /"+ folder +" to put into folder /"+ name+" ...")
main(folder,name, txt_branch_name)
