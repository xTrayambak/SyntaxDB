import os
import logging
import sys
import json
import threading
import time

from multiprocessing.pool import ThreadPool
from apscheduler.schedulers.background import BackgroundScheduler
from pickle import dump, load

from syntaxdb.lang import Parser
from syntaxdb.db.exceptions import *

VERSION = "0.0.1_TESTING"

class Database:
    def __init__(self, name: str):
        self.data = {"version": VERSION}
        self.name = name
        self.location = os.getcwd()
        self.query_threads = []

        self.server_pool = None
        self.server = None

        self.scheduler = BackgroundScheduler()

        self.parser = Parser()
        
        self.logger_info = logging.Logger("syntaxdb-info", logging.INFO)
        self.logger_warn = logging.Logger("syntaxdb-warn", logging.WARN)

        self.stdout = logging.StreamHandler(sys.stdout)

        self.logger_info.addHandler(self.stdout)
        self.logger_warn.addHandler(self.stdout)

        self.autosave_time = 30
        self.autosave_status = True

        self.version = VERSION

    def info(self, sender: str = "SyntaxDB/Worker", msg: str = "This is a substitute message!"):
        self.logger_info.log(f"[{sender}/INFO] :: {msg}")

    def warn(self, sender: str = "SyntaxDB/Worker", msg: str = "This is a substitute warning!"):
        self.logger_warn.warn(f"[{sender}/WARN] :: {msg}")

    def logp(self, msg: str):
        self.logger_info.log(msg = f"* {msg}", level = logging.INFO)

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
        except FileNotFoundError:
            self.warn("SyntaxDB/Loader", f"Encountered 'FileNotFoundError' whilst loading file '{self.name}.syntaxdb', the data will be loaded explicitly.")
            self.data = {}
            open(f"{self.location}/{self.name}.syntaxdb", "w").close()
        except TypeError:
            self.warn("SyntaxDB/Loader", f"Encountered 'TypeError' whilst loading file '{self.name}.scaledb', data will be explicitly loaded with a template.")
            self.data = {}
            open(f"{self.location}/{self.name}.syntaxdb", "w").close()
        except EOFError:
            self.data = {}

    def jsonport(self, filename: str):

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

    def toJSONstr(self):
        return self.data

    def autosave(self):
        self.scheduler.add_job(self._autosave, 'autosave', minutes=self.autosave_time)
        self.scheduler.start()

    def _autosave(self):
        if self.autosave_status:
            self.query("DUMP")