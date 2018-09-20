import mysql.connector
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize
import nltk
import os
import math
nltk.download('punkt')

words = {}


def tfidf_calc(token, did, total_docs):
    tf = words[token][did]
    df = len(words[token])
    return tf * math.log(total_docs/df) * 1.0


def tfidf_tablefill(total_docs, con):
    cursor = con.cursor()
    for token in words:
        for doc_id in words[token]:
            statement = "insert into TFIDF(Word, DID, TFIDF) values(%s, %s, %s)"
            values = (token, doc_id, tfidf_calc(token, doc_id, total_docs))
            cursor.execute(statement, values)
            con.commit()
    con.commit()
    con.cursor().close()


def tokenizer(text, did, con):
    tokens = word_tokenize(text)
    cursor = con.cursor()

    stemmer = SnowballStemmer('english')
    count = 0
    for token in tokens:
        token = stemmer.stem(token)
        if token != "":

            if token in words:
                temp_dic = words[token]
                if did in temp_dic:
                    temp_dic[did] = temp_dic[did] + 1
                    words[token] = temp_dic
                else:
                    temp_dic[did] = 1
                    words[token] = temp_dic
            else:
                words[token] = {did: 1}

            statement = "INSERT INTO Tokens(DID, TID, Word) VALUES(%s, %s, %s)"
            values = (did, count, token)
            cursor.execute(statement, values)
            con.commit()
            count += 1

    con.commit()
    con.cursor().close()


def read_directory(dir_path):
    files = os.listdir(dir_path)
    con = mysql.connector.connect(user='root', host='10.0.0.238', database='Tokenizer')
    count = 0
    for file in files:
        count += 1
        tokenizer(open(dir_path + "/" + file).read(), count, con)
    tfidf_tablefill(count, con)

    con.close()


if __name__ == "__main__":
    read_directory(input("Enter a directory path relative to this program: "))
