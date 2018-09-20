from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
import os
import sys
import mysql.connector



# This function will get the data text directory in folder 'Project'
def getDirectoryOfData():
    dataDir = os.path.realpath('.') +'/data'
    dataFiles = os.listdir(dataDir)
    filesPath = []
    for files in dataFiles:
        filesPath.append(dataDir+"/"+files)
    return filesPath


class CS157ATokenizer(object):

    def __init__(self, debugLevel = 0, con= None):
        self.documentOrder = []
        self.debugLevel = debugLevel
        self.con = con


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
                            word = word.lower()
                            self.documentOrder.append(ps.stem(word))
                            if(self.debugLevel > 0):
                                print("Adding 1 >" + word + "<")
                            word=""
                        whiteSpaceStack.append(char)
                    # If it's a different symbol, it will be added as a token instead
                    else:
                        if(word):
                            word = word.lower()
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

    def recreateTable(self):
        if(self.con):
            cursor = self.con.cursor()
            try:
                cursor.execute("DROP TABLE Stem")
                self.con.commit()
            except:
                pass
            cursor.execute("CREATE TABLE Stem (name CHAR(60), freq INT, PRIMARY KEY (name))")
            self.con.commit()
            cursor.close()

    def updateDatabase(self):
        if(self.con):
            cursor = self.con.cursor()
            freqDict = self.freqStem()
            freqList = []
            for key in freqDict.keys():
                escapedKey = key.replace("'", "\\'") 
                if self.debugLevel > 1:
                    print("Adding " + " key = " + key + " escapedKey = " + escapedKey + " with freq " + str(freqDict[key]))
                cursor.execute("INSERT INTO Stem(name, freq) VALUES('%s', %d)" % (escapedKey, freqDict[key]))
                self.con.commit()
            cursor.close()
    

def main():
    documentsData = {}
    dataFilesPath = getDirectoryOfData()

    # if we passwd 3 arguments we connect to database
    con = None
    if len(sys.argv) == 4:
        dbUser = sys.argv[1]
        dbPassword = sys.argv[2]
        dbDatabase = sys.argv[3]
        con = mysql.connector.connect(user = dbUser, password = dbPassword,
                                      host = 'localhost', database = dbDatabase)
    
    tokenizer = CS157ATokenizer(debugLevel = 0, con = con);
    
    for dataFile in dataFilesPath:
        #print("Processing " + dataFile + "...")
        tokenizer.parseText(dataFile)
    #print(tokenizer.documentOrder)
    if con:
        # if we have database connection put the data in
        tokenizer.recreateTable()
        tokenizer.updateDatabase()
    else:
        # just print sorted list
        stemFreq = tokenizer.freqStemSorted()
        for stem in stemFreq:
            print("%40.40s %d" % (stem[1], stem[0]))
            #print(stemFreq)
    

main()
