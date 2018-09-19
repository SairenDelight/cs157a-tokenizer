import mysql.connector
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')


def tokenizer(text):
    tokens = word_tokenize(text)
    con = mysql.connector.connect(user='root', host='localhost', database='Tokenizer')
    cursor = con.cursor()

    stemmer = SnowballStemmer('english')
    count = 0
    for token in tokens:
        token = stemmer.stem(token)
        if token != "":
            cursor.execute("INSERT INTO Tokens VALUES(%d, %d, '%s')" % (3, count, token))
            con.commit()
            count += 1
    con.commit()
    con.cursor().close()
    con.close()


if __name__ == "__main__":
    tokenizer("The brown cat ran away. He is running now.")
