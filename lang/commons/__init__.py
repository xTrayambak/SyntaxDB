from lang.functions import *

class ArgumentTag:
    OPTIONAL = 1
    REQUIRED = 0

class FUNCTIONS:
    CREATE = {
            "cmd": "create", 
            "args": 
            [
                {   "name": "structure", 
                    "tags": [ArgumentTag.REQUIRED], 
                    "function": create,
                    "help": "The structure name."
                }
            ]
        }

    POP = {"cmd":"pop", 
        "args": [
            {
            "name": "structure", 
            "tags": [ArgumentTag.REQUIRED], 
            "help": "The structure to pop."
            }
        ],
        "function": pop,
        "help": "Pop a value inside a database."
    }

    GET = {"cmd": "get", 
            "args": [
                        {
                        "name": "structure", 
                        "tags": [ArgumentTag.OPTIONAL], 
                        "help": "The structure to get from (optional)"
                        }
                    ], 

            "function": all,
            "help": "Get either all the structures in a database or just one structure."
        }

    DUMP = {"cmd": "dump", "args": [], "function": dump,
            "help": "Save or 'dump' all the data inside the data (including structures and their children values) to the local [dbname].syntaxdb"
            }
    JSONDUMP = {"cmd": "jsondump", "args": [], "function": jsonDUMP, "help": "Get all the data and dump it to a JSON file."}
    JSONLOAD = {"cmd": "jsonload", "args": [], "function": jsonLOAD, "help": "Load a data from a JSON file."}
    
    TRANSMISSIONSTART = {"cmd": "transmit", "args": [], "function": transmissionserverstart, "help": "Start a 'transmission' server which can let anyone with the correct password transfer data from your database (note: this server will stop if your Python instance stops, and will not turn back on again unless this command is typed in again)"}
    TRANSMISSIONSTOP = {"cmd": "transmitstop", "args": [], "function": transmissionserverstop, "help": "Stop a 'transmission' server/service which is running."}

    INSTANTIATE = {"cmd": "new", "args": [], "function": instantiate, "help": "Create a new value inside a database."}

    RECEIVE = {"cmd": "receive", "args": [], "function": receive, "help": "Receive data from a custom SyntaxDB hosted server."}
    HELP = {"cmd": "help", "args": [], "function": help, "help": "How. Why. How did you do this. I have many questions."}

class TokenType:
    FUNCTION = 0
    VALUE = 1

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