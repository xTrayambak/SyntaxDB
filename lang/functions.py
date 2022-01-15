def create(args, db):
    name = args[0]
    db.data.update(
        {
            name: {}
        }
    )

    return db.data[name]

def dump(args, db):
    try:
        db.save()
    except:
        return 'An error occured whilst saving.'

    return 'Saved Successfully.'

def all(args, db):
    if len(args) > 1:
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
    """

def jsonDUMP(args, db):
    return db.toJSON(args[0])

def jsonLOAD(args, db):
    return db.jsonport(args[0])