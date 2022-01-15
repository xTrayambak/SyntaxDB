from lang.functions import *

class ArgumentTag:
    OPTIONAL = 1
    REQUIRED = 0

class FUNCTIONS:
    CREATE = {"cmd": "create", 
            "args": 
            [{"name": "structure", 
            "tags": [ArgumentTag.REQUIRED]}], 
            "function": create
            }

    MAKE = {"cmd": "make", 
            "args": [
                        {"name": "structure", 
                            "tags": [ArgumentTag.REQUIRED], 
                            "help": "The structure to make the variable in."
                        }, 

                        {"name": "parent", 
                            "tags": [ArgumentTag.REQUIRED],
                            "help": "The parent of the variable."
                        },

                        {"name": "name",
                            "tags": [ArgumentTag.REQUIRED],
                            "help": "The name of the variable to put into the structure."
                        },

                        {"name": "value", 
                            "tags": [ArgumentTag.REQUIRED],
                            "help": "The value of the variable."
                        },

                        {"name": "type",
                            "tags": [ArgumentTag.REQUIRED],
                            "help": "The type of the variable. (eg., integer, map, array, string)"
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

    HELP = {"cmd": "help", "args": [], "function": help, "help": "How. Why. How did you do this. I have many questions."}

class TokenType:
    FUNCTION = 0
    VALUE = 1

class Types:
    STRING = "string"
    INTEGER = "integer"
    ARRAY = "array"
    MAP = "map"