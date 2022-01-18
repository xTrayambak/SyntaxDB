from db import Database

if __name__ == "__main__":

    db = Database(input("Enter database name . . . "))
    db.load()
    
    while True:
        data = db.query(input("Enter a SyntaxDB command . . . "))
        if data != None:
            print(data)