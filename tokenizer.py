from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
import os




# This function will get the data text directory in folder 'Project'
def getDirectoryOfData():
    currentDir = os.path.realpath('.') +'/data'
    dataFiles = os.listdir(currentDir)
    filesPath = []
    for files in dataFiles:
        filesPath.append(currentDir+"/"+files)
    return filesPath





# This function will parse the text into an array of words
def parseText(documentPath):
    ps = PorterStemmer()
    documentOrder = []
    word = ""
    stack=[]
    with open(documentPath,"r") as document:
        text = document.read()
    # This will loop through all the characters in the text
    for index,char in enumerate(text):
        asciiCode = int(ord(char))
        # This will not include non-printable characters
        if (asciiCode > 31 and asciiCode != 127):
            # Check if it is A-Z, a-z, 0-9, '-',',', and '
            if(asciiCode == 39 or asciiCode == 45 or asciiCode == 44 or (asciiCode > 47 and asciiCode < 58) or (asciiCode > 64 and asciiCode < 91) or (asciiCode > 96 and asciiCode < 123) ):
                if not not stack:
                    stack=[]
                word+=char
            else:
                # If there's a space between words add to the stack and add the word to the array
                if(asciiCode == 32):
                    if(not stack):
                        documentOrder.append(ps.stem(word))
                        word=""
                    stack.append(char)
                # If it's a different symbol, it will be added as a token instead
                else:
                    documentOrder.append(ps.stem(word))
                    documentOrder.append(ps.stem(char))
                    word=""
    if(not not word):
        documentOrder.append(ps.stem(word))
    return documentOrder






documentsData = {}
dataFilesPath = getDirectoryOfData()
listed =parseText(dataFilesPath[0])
print(listed)
