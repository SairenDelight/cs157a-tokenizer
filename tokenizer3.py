from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
import os




# This function will get the data text directory in folder 'Project'
def getDirectoryOfData():
    dataDir = os.path.realpath('.') +'/data'
    dataFiles = os.listdir(dataDir)
    filesPath = []
    for files in dataFiles:
        filesPath.append(dataDir+"/"+files)
    return filesPath


class CS157ATokenizer(object):

    def __init__(self, debugLevel = 0):
        self.documentOrder = []
        self.debugLevel = debugLevel


    # This method will parse the text into an array of words
    def parseText(self, documentPath):
        ps = PorterStemmer()
        word = ""
        whiteSpaceStack=[]

        with open(documentPath,"r") as document:
            text = document.read()

        # This will loop through all the characters in the text
        for index, char in enumerate(text):
            asciiCode = int(ord(char))
            # This will not include non-printable characters
            if (asciiCode > 31 and asciiCode != 127):
                if(self.debugLevel > 2):
                    print("index = " +  str(index) + " char = >" + char +  "< word = >" + word + "< whiteSpaceStack = " + str(whiteSpaceStack))
                # Check if it is A-Z, a-z, 0-9, '-' , and '''
                if(asciiCode == 39 or \
                   asciiCode == 45 or \
                   (asciiCode > 47 and asciiCode < 58) or \
                   (asciiCode > 64 and asciiCode < 91) or \
                   (asciiCode > 96 and asciiCode < 123) \
                ):
                    if not not whiteSpaceStack:
                        whiteSpaceStack=[]
                    word+=char
                else:
                    # If there's a space between words add to the whiteSpaceStack and add the word to the array
                    if(asciiCode == 32):
                        if(not whiteSpaceStack and word):
                            self.documentOrder.append(ps.stem(word))
                            if(self.debugLevel > 0):
                                print("Adding 1 >" + word + "<")
                            word=""
                        whiteSpaceStack.append(char)
                    # If it's a different symbol, it will be added as a token instead
                    else:
                        if(word):
                            if(self.debugLevel > 0):
                                print("Adding 2 >" + word + "<")
                                
                            self.documentOrder.append(ps.stem(word))

                        if(self.debugLevel >0):
                            print("Adding 3 >" + char + "<")

                        self.documentOrder.append(ps.stem(char))
                        word=""
        if(not not word):
            self.documentOrder.append(ps.stem(word))

    def freqStem(self):
        freqDict = {}
        for stem in self.documentOrder:
            if(stem in freqDict):
                freqDict[stem] = freqDict[stem] + 1
            else:
                freqDict[stem] = 1
        return freqDict

    def freqStemSorted(self):
        freqDict = self.freqStem()
        freqList = []
        for key in freqDict.keys():
            freqList.append((freqDict[key], key))
        freqList.sort(reverse=True)
        return freqList
    

def main():
    documentsData = {}
    dataFilesPath = getDirectoryOfData()
    tokenizer = CS157ATokenizer(debugLevel = 0);
    
    for dataFile in dataFilesPath:
        #print("Processing " + dataFile + "...")
        tokenizer.parseText(dataFile)
    #print(tokenizer.documentOrder)

    stemFreq = tokenizer.freqStemSorted()
    for stem in stemFreq:
        print("%40.40s %d" % (stem[1], stem[0]))
    #print(stemFreq)
    

main()
