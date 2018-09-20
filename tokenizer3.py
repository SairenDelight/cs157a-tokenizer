from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
import os
import sys
import mysql.connector
import math


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
        self.curDocID = 0
        self.curWordID = 1
        self.words = {}
        self.cursor = None

        if self.con:
            self.cursor = self.con.cursor()


    # This method will parse the text into an array of words
    def parseText(self, documentPath):
        self.curDocID = self.curDocID + 1

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
                            word = ps.stem(word)
                            self.documentOrder.append(word)
                            self.updateWords(word, self.curDocID)

                            if(self.debugLevel > 0):
                                print("Adding 1 >" + word + "<")
                            word=""
                        whiteSpaceStack.append(char)
                    # If it's a different symbol, it will be added as a token instead
                    else:
                        if(word):
                            word = word.lower()
                            word = ps.stem(word)
                            if(self.debugLevel > 0):
                                print("Adding 2 >" + word + "<")

                            self.documentOrder.append(word)
                            self.updateWords(word, self.curDocID)

                        if(self.debugLevel >0):
                            print("Adding 3 >" + char + "<")
                        word1 = ps.stem(char)
                        self.documentOrder.append(word1)
                        self.updateWords(word1, self.curDocID)
                        word=""

        if(not not word):
            self.documentOrder.append(ps.stem(word))

    def updateWords(self, token, did):
        if token in self.words:
            temp_dic = self.words[token]
            if did in temp_dic:
                temp_dic[did] = temp_dic[did] + 1
                self.words[token] = temp_dic
            else:
                temp_dic[did] = 1
                self.words[token] = temp_dic
        else:
            self.words[token] = {did: 1}

        if self.con:
            statement = "INSERT INTO Tokens(DID, TID, Word) VALUES(%s, %s, %s)"
            values = (did, self.curWordID, token)
            self.cursor.execute(statement, values)
            self.con.commit()
            self.curWordID += 1

    def tfidfCalc(self, token, did):
        tf = self.words[token][did]
        df = len(self.words[token])
        return tf * math.log(self.curDocID/df) * 1.0

    def tfidfTableFill(self):
        if self.con:
            for token in self.words:
                for doc_id in self.words[token]:
                    statement = "insert into TFIDF(Word, DID, TFIDF) values(%s, %s, %s)"
                    values = (token, doc_id, self.tfidfCalc(token, doc_id))
                    self.cursor.execute(statement, values)
                    self.con.commit()
            self.con.commit()


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
            try:
                self.cursor.execute("DROP TABLE Stem")
                self.con.commit()
            except:
                pass
            self.cursor.execute("CREATE TABLE Stem (name CHAR(60), freq INT, PRIMARY KEY (name))")
            self.con.commit()

            try:
                self.cursor.execute("DROP TABLE Tokens")
                self.con.commit()
            except:
                pass
            self.cursor.execute("CREATE TABLE Tokens(DID INT, TID INT, Word CHAR(60))")
            self.con.commit()

            try:
                self.cursor.execute("DROP TABLE TFIDF")
                self.con.commit()
            except:
                pass
            self.cursor.execute("CREATE TABLE TFIDF(Word CHAR(60), DID INT, TFIDF FLOAT)")
            self.con.commit()

    def updateDatabase(self):
        if(self.con):
            freqDict = self.freqStem()
            freqList = []
            for key in freqDict.keys():
                escapedKey = key.replace("'", "\\'")
                if self.debugLevel > 1:
                    print("Adding " + " key = " + key + " escapedKey = " + escapedKey + " with freq " + str(freqDict[key]))
                self.cursor.execute("INSERT INTO Stem(name, freq) VALUES('%s', %d)" % (escapedKey, freqDict[key]))
                self.con.commit()


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

    if con:
        # if we have database create tables
        tokenizer.recreateTable()

    for dataFile in dataFilesPath:
        #print("Processing " + dataFile + "...")
        tokenizer.parseText(dataFile)
    #print(tokenizer.documentOrder)
    if con:
        # if we have database connection put the data in
        tokenizer.updateDatabase()
        tokenizer.tfidfTableFill()
    else:
        # just print sorted list
        stemFreq = tokenizer.freqStemSorted()
        for stem in stemFreq:
            print("%40.40s %d" % (stem[1], stem[0]))
            #print(stemFreq)


main()
