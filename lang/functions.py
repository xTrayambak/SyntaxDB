from db.transmission import TransmissionServer
from db.receiver import DataReceiver

import socket
import ast

class Types:
    STRING = "string"
    INTEGER = "integer"
    ARRAY = "array"
    MAP = "map"

TypeToConvert = {
    Types.STRING: str,
    Types.INTEGER: int,
    Types.ARRAY: list,
    Types.MAP: dict
}

def create(args, db):
    name = args[0]
    db.data.update(
        {
            name: {}
        }
    )

    return db.data[name]

def pop(args, db):
    if args[0] in db.data:
        db.data.pop(args[0])

def instantiate(args, db):
    structure = args[0]
    name = args[1]
    vargs = args[2].split("@")

    value = vargs[0]
    type = vargs[1]

    value = ast.literal_eval(value)

    db.data[structure].update(
        {
            name: value
        }
    )

    db.logp(f"New value '{name}' added to database '{structure}'; call [DUMP] to save changes to live database.")

def dump(args, db):
    try:
        db.save()
    except:
        return 'An error occured whilst saving.'

    return 'Saved Successfully.'

def all(args, db):
    """for arg in args:
        idx = args.index(arg)
        if idx != 0:
            if '.' in arg:
                if args[0] in db.data:
                    if arg in db.data[args[0]]:
                        return db.data[args[0]]"""

    if len(args) > 0:
        if args[0] in db.data:
            return db.data[args[0]]
        else:
            return f"No structure was found with the name '{args[0]}'; did you make a typo?"
    else:
        return db.data

def help(args, db):
    return """
    SyntaxDB, a fast, scalable, effortless to setup, cheap and flexible serverless database library for Python.

    All commands can be typed both in lowercase (command), uppercase (COMMAND) and other formats (cOmMaND)

    * CREATE
    \t-Create a data structure inside the database.
    \t-Warning: this data structure will not be saved until DUMP is called!

    * POP
    \t-"Pop", or remove a structure or key inside a structure.

    * DUMP
    \t-Perform binary serialization and save the current database to [databasename].scaledb

    * JSONLOAD
    \t-Load data from a JSON file. Useful for porting your JSON files to SyntaxDB.

    * JSONDUMP
    \t-Dump data to a JSON file. Useful for transferring data to another database easily.

    * TRANSMIT
    \t-Start a server with a password, if the password given is correct by a client request, then the data from this database is transferred to them.

    * TRANSMITSTOP
    \t-Stop a file transmitter session.

    * RECEIVE
    \t-Receive a stream of JSON data from a given URL and password.
    """

def jsonDUMP(args, db):
    return db.toJSON(args[0])

def jsonLOAD(args, db):
    return db.jsonport(args[0])

def transmissionserverstart(args, db):
    host = str(args[0])
    port = int(args[1])
    password = str(args[2])

    server = TransmissionServer(
        db, password, host, port
    )

    db.server = server

def transmissionserverstop(args, db):
    server = db.server_pool

    if server is None:
        db.logp("No transmission server is active that can be disabled!")
        return -1

    server.kill()
    db.logp("Stopped transmission service.")

def receive(args, db):
    url = str(args[0])
    port = int(args[1])
    password = str(args[2])

    db.logp(f"Locating [{url}]... This may take a minute.")

    ip = socket.gethostbyname(url)

    db.logp(f"URL: {url}")
    db.logp(f"IP: {ip}")

    if not url.startswith("http"):
        url = "http://" + url

    dataReceiver = DataReceiver(url, port, password)

    db.logp(f"Now, asynchronously requesting {url}/sdbdatatransfer [DataReceiver instantiated.]")
    results = dataReceiver.run()

    db.logp(results)

    db.logp("Results have been modified to the non-live database. Call [DUMP] to save changes.")

    db.data = results