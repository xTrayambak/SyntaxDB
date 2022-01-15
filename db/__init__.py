import os
import logging
import sys
import json

from multiprocessing.pool import ThreadPool
from pickle import dump, load

from lang import Parser
from db.exceptions import *
from db.converter import DBConverter

VERSION = "0.0.1_TESTING"

class Database:
    def __init__(self, name: str):
        self.data = {"version": VERSION}
        self.name = name
        self.location = os.getcwd()
        self.query_threads = []

        self.converter = DBConverter()

        self.parser = Parser()
        
        self.logger_info = logging.Logger("syntaxdb-info", logging.INFO)
        self.logger_warn = logging.Logger("syntaxdb-warn", logging.WARN)

        self.stdout = logging.StreamHandler(sys.stdout)

        self.logger_info.addHandler(self.stdout)
        self.logger_warn.addHandler(self.stdout)

        self.version = VERSION

    def info(self, sender: str = "SyntaxDB/Worker", msg: str = "This is a substitute message!"):
        self.logger_info.log(f"[{sender}/INFO] :: {msg}")

    def warn(self, sender: str = "SyntaxDB/Worker", msg: str = "This is a substitute warning!"):
        self.logger_warn.warn(f"[{sender}/WARN] :: {msg}")

    def query(self, command: str):
        thread = ThreadPool(processes = 1)
        result = thread.apply_async(self._query, (command,))

        self.query_threads.append((thread, result))

        return result.get()

    def _query(self, command: str):
        return self.parser.parse(command, self)

    def save(self):
        dump(self.data, open(f"{self.location}/{self.name}.syntaxdb", "wb"))

    def load(self):
        try:
            self.data = load(
                open(f"{self.location}/{self.name}.syntaxdb", "rb")
            )

            if "version" not in self.data:
                raise InvalidMetadata(f"'version' tag was not found in SyntaxDB file '{self.name}', the file is either corrupted or the tag has been edited and removed.")
            
            version = self.data["version"]

            if version != VERSION:
                self.warn("SyntaxDB/Loader", f"File '{self.name}.syntaxdb' is using SyntaxDB version [{version}] and the installation is running on version [{VERSION}]; creating a backup for the file and attempting to convert to new SyntaxDB version. This may fail, so a backup is about to be created.")
                backup = open(self.location + "/" + self.name + "-BACKUP.syntaxdb", "wb")
                dump(self.data, backup)
                backup.close()
                self.warn("SyntaxDB/Loader", f"File '{self.name}.syntaxdb' has a backup now.")

                self.warn("SyntaxDB/Loader", f"Conversion is now starting, this may fail, so please use [{self.name}-BACKUP.syntaxdb] if it fails.")
                self.converter.toNewVersion(self, self.data)
        except FileNotFoundError:
            self.warn("SyntaxDB/Loader", f"Encountered 'FileNotFoundError' whilst loading file '{self.name}.syntaxdb', the data will be loaded explicitly.")
            self.data = {"version": VERSION}
            open(f"{self.location}/{self.name}.syntaxdb", "w").close()
        except TypeError:
            self.warn("ScaleDB/Loader", f"Encountered 'TypeError' whilst loading file '{self.name}.scaledb', data will be explicitly loaded with a template.")
            self.data = {"version": VERSION}
            open(f"{self.location}/{self.name}.syntaxdb", "w").close()
        except EOFError:
            self.data = {"version": VERSION}

    def jsonport(self, filename: str):
        if os.path.exists(filename) != True:
            raise NoJSONFileFound(f"No file called '{filename}' exists!")

        json_data = json.load(open(filename, "r"))
        self.data = dict(json_data)
        self.data.update(
            {
                "version": VERSION
            }
        )

        return f"Loaded data from {filename} successfully."

    def toJSON(self, filename: str):
        with open(filename, "w") as file:
            json.dump(self.data, file)
            file.close()

            return f"Saved to {filename} successfully."