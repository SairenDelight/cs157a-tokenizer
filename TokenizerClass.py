from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from openpyxl import Workbook
import os
import sys
import math



def getDirectoryOfData():
    '''
        This function will get the 'data' directory of current folder
    '''
    dataDir = os.path.realpath('.') +'/data'
    dataFiles = os.listdir(dataDir)
    filesPath = []
    for files in dataFiles:
        filesPath.append(dataDir+"/"+files)
    return filesPath

class Tokenizer(object):
    '''
        This class will store all the data into a spreadsheet
        instead of a console or database. 
    '''
    
    def __init__(self,file_paths,excel_sheet):
        '''
            This initializes the Tokenizer Class

            Class Variables:
            __tokenized_words {} and __key_words {} format:
                { 'Token1': [ { DocumentID : [ [TokenPos,TokenPos,...], TF, TFIDF ] },  DF] }
            __variation_of_stem_forms {} format:
                { 'Stem Word' : [Variation1, Variation2, Variation3...] }

            
            Parameters:
                file_paths (String): Array of document path
                excel_sheet (Workbook): Spreadsheet to input data
        '''
        self.__tokenized_words = {}
        self.__key_words = {}
        self.__variation_of_stem_forms = {}
        self.data_excel_sheet = excel_sheet
        self.__file_paths = file_paths
        self.__total_num_of_doc = len(file_paths)






    def run(self):
        # This will collect all of the TF first
        for docID,path in enumerate(self.__file_paths):
            # print("Current path is: " + path)
            tokenized_text = self.start_tokenizing_document(path)
            self.store_data_into_dict(tokenized_text, docID, self.__tokenized_words)

        # This will collect DF and TFiDF
        for token_value in self.__tokenized_words.values():
            num_of_doc_with_token = len(token_value[0])
            self.store_df_calc(token_value,self.__total_num_of_doc,num_of_doc_with_token)
            self.store_tfidf_calc(token_value)
        self.__store_data_into_excel(self.__tokenized_words)

        



    







    def start_stemming_document(self,file_path_of_doc):
        '''
            Stems the text for each word from the document

            Parameters:
                file_path (String): the current document path to perform stem operation
            
            Return:
                (List): an array of tokenized words
        '''
        with open(file_path_of_doc,"r",encoding="UTF-8",errors='ignore') as document:
            text = document.read()
        return word_tokenize(text)
    





    def start_tokenizing_document(self,file_path_of_doc):
        '''
            Tokenizes the text for each word from the document

            Parameters:
                file_path (String): the current document path to perform stem operation
            
            Return:
                (List): an array of tokenized words
        '''
        with open(file_path_of_doc,"r") as document:
            text = document.read()
        return word_tokenize(text)
        





    def store_data_into_dict(self, stemmed_text, doc_ID, word_dict = {}):
        '''
            Store stem word, Token position, document id, and TF into class variable dictionary
            What is stored during this operation:
                {  'Token' : [{ DocumentID : [[TokenPos,TokenPos,...], TF] }   ]   }

            Parameters:
                file_path (String): the current document path to perform stem operation
                stemmed_text (List): the array of tokenized words
                doc_ID (int): the current document ID
            Return:
                (Dictionary): Return a dictionary of values in the format above
        '''
        current_doc_word_count = len(stemmed_text)
        for tokenPos, word in enumerate(stemmed_text):
            if word in word_dict:
                value = word_dict[word][0]
                if doc_ID in value:
                    value[doc_ID][0].append(tokenPos)
                else:
                    value[doc_ID] = [[tokenPos]]
            else:
                word_dict[word] = [{ doc_ID : [[tokenPos]] }]
        for doc in word_dict.values():
            length_of_doc = len(doc[0])
            for currentDoc in doc[0].values():
                if len(currentDoc) != 2:
                    self.store_tf_calc(currentDoc,current_doc_word_count)
                else: 
                    continue
        return word_dict

    





    def store_tf_calc(self, document_id_value,doc_word_count):
        '''
            Stores the token frequency (TF) in given dictionary
            Before:
                {  'Token' : [{ DocumentID : [[TokenPos,TokenPos,...]]  }       }]

            After:
                {  'Token' : [{ DocumentID : [[TokenPos,TokenPos,...], TF] }     }]

            Parameters:
                document_id_value (Dictionary): the DocumentID value
        '''
        total_tokens = len(document_id_value[0])
        document_id_value.append(self.__calculate_tf(total_tokens,doc_word_count))








    def store_tfidf_calc(self, document_id_value):
        '''
            Stores the token frequency (TF) in given dictionary
            Before:
                {  'Token' : [ { DocumentID : [[TokenPos,TokenPos,...], TF] }, DF  ]   }

            After:
                {  'Token' : [   {DocumentID : [[TokenPos,TokenPos,...], TF,TFIDF]}     ,      DF     ]   }

            Parameters:
                document_id_value (Dictionary): the DocumentID value
        '''
        for current_doc_values in document_id_value[0].values():
            tf = current_doc_values[1]
            df = document_id_value[1]
            current_doc_values.append(self.__calculate_tfidf(tf,df))







    def store_df_calc(self,document_id_value,total_num_of_doc, num_of_doc_with_token):
        '''
            Stores the document frequency (DF) in given dictionary per token

            Before:
                {  'Token' : [ { DocumentID : [[TokenPos,TokenPos,...], TF] }   ]   }

            After:
                {  'Token' : [ { DocumentID : [[TokenPos,TokenPos,...], TF] }, DF ] }

            Parameters:
                document_id_value (List): the DocumentID value containing the List for token
        '''
        document_id_value.append(self.__calculate_df(total_num_of_doc,num_of_doc_with_token))









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





    def __store_data_into_excel(self,word_dict={}):
        '''
            Stores value into Excel Spreadsheet

            Parameters:
                word_dict (Dictionary): the data of all the correctly formatted as shown in init
        '''
        count_row = 1
        self.data_excel_sheet.cell(row = count_row,column = 1, value="token")
        self.data_excel_sheet.cell(row = count_row,column = 2, value="document_ID")
        self.data_excel_sheet.cell(row = count_row,column = 3, value="token_Position")
        self.data_excel_sheet.cell(row = count_row,column = 4, value="tf")
        self.data_excel_sheet.cell(row = count_row,column = 5, value="df")
        self.data_excel_sheet.cell(row = count_row,column = 6, value="tfidf")
        count_row = count_row + 1
        for token,documents in enumerate(word_dict.values()):
            for key,val in documents[0].items():
                # print("Token: " +str(token) + " Value: "+ str(val))
                document_ID = key
                token_Position = val[0]
                tf = val[1]
                df = documents[1]
                tfidf = val[2]
                self.data_excel_sheet.cell(row = count_row,column = 1, value=token)
                self.data_excel_sheet.cell(row = count_row,column = 2, value=document_ID)
                self.data_excel_sheet.cell(row = count_row,column = 3, value=str(token_Position))
                self.data_excel_sheet.cell(row = count_row,column = 4, value=tf)
                self.data_excel_sheet.cell(row = count_row,column = 5, value=df)
                self.data_excel_sheet.cell(row = count_row,column = 6, value=tfidf)
                count_row = count_row + 1






    def print_data(self):
        print(self.__tokenized_words)





    def get_tokenized_words_data(self):
        return self.__tokenized_words





    def get_key_words_data(self):
        return self.__key_words







def main():
    '''
        Runs the entire tokenizer process.
    '''
    data_Files_Path = getDirectoryOfData()
    wb = Workbook()
    data_excel_sheet = wb.active


    tokenizer1 = Tokenizer(data_Files_Path,data_excel_sheet)
    tokenizer1.run()
    # tokenizer1.print_data()
    wb.save('Tokenizer_data.xlsx')

main()