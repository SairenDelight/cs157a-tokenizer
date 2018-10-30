
dbUser = "root"
dbPass = ""
host = 'localhost'
dbName = "db_stem"
mydb = mysql.connector.connect(
                                     user = self.__dbUser,
                                     password = self.__dbPassword,
                                     host = 'localhost',
                                     database = self.__dbDatabase)
mycursor = mydb.cursor(buffered=True)