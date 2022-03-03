from syntaxdb.db import Database

db = Database(input("Enter database name . . . "))
db.load()
    
while True:
    data = db.query(input("Enter a SyntaxDB command . . . "))
    if data != None:
        print(data)