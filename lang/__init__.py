from lang.commons import FUNCTIONS, ArgumentTag, TypeToConvert, Types
import difflib

def props(cls):   
  return [i for i in cls.__dict__.keys() if i[:1] != '_']

class Parser:
    def __init__(self):
        pass

    def get_tokens(self, string: str):
        return string.split(" ")

    def parse(self, string: str, db):
        if len(string) < 1:
            return
        tokens = self.get_tokens(string)

        func = tokens[0]
        tokens.pop(0)

        args = tokens

        attr = props(FUNCTIONS)

        _lower_attr = []
        for _attr in attr:
            _lower_attr.append(_attr.lower())

        closest_matches = difflib.get_close_matches(
            func, _lower_attr
        )

        for funcName in attr:
            data = getattr(FUNCTIONS, funcName)

            class parseLocals: argsRequested = None
            
            if func.lower() == data['cmd']:
                parseLocals.argsRequested = data['args']

                try:
                    argTag = data['args'][0]["tags"][0]
                except:
                    argTag = ArgumentTag.OPTIONAL

                if len(parseLocals.argsRequested) > len(args) and argTag != ArgumentTag.OPTIONAL:
                    error_string = 'Not enough arguments were provided. The command was not executed, this command expects these arguments:'

                    for args in parseLocals.argsRequested:
                        help = args["help"]
                        name = args["name"]

                        error_string += f"\n* {name} -- {help}"

                    return error_string
                    
                try:
                    return data['function'](args, db)
                except:
                    return 'An error occured whilst executing command.'

        error_string = f"No command called '{func}' found."

        for matches in closest_matches:
            idx = closest_matches.index(matches)
            if idx == 0:
                error_string += f"\nClosest matches are: \n* {matches}"
            else:
                error_string += f"\n* {matches}"

        return error_string