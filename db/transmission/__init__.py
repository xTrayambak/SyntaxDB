import flask
from flask import request

from logging import getLogger

from threading import Thread

# Disable the Werkzeug Logger because it's going to spam the console.
werkzeug = getLogger("werkzeug")
werkzeug.disabled = True

class TransmissionServer:
    def __init__(self, db, password: str, host: str = "localhost", port: int = 8000):
        self.password = password
        self.port = port
        self.host = host
        self.db = db

        self.flaskApp = flask.Flask(
            __name__
        )

        def run(): self.flaskApp.run(host,port)

        try:
            db.server_pool = Thread(target = run, args = ())
            self.hookup()
            db.server_pool.start()
        except Exception as exc:
            db.logp(f"* An error has occured whilst trying to host the transmission service. [Exception(message={exc})]")
            return -1

        db.logp(f"Transmission server has started on address [{host}:{port}] with password '{password}'")
        return "* Successfully started server!"

    def hookup(self):
        @self.flaskApp.route("/sdbdatatransfer")
        def sdbdatatransfer():
            if len(self.password) < 1:
                self.password = ""

            ip_address = request.remote_addr
            args = request.args

            password_given = args["password"]

            self.db.logp(f"[{ip_address}] is trying to transmit data from the remote transmission server at [{self.host}:{self.port}]; password = {password_given}")

            if password_given == self.password:
                self.db.logp(f"[{ip_address}] was authenticated successfully!")
                self.db.logp(f"Starting transmission for [{ip_address}]")

                data = self.db.toJSONstr()

                return flask.jsonify(
                    data
                )
            else:
                return flask.jsonify(
                    {
                        "result": "invalid-credentials",
                        "db": f"SyntaxDB {self.db.version}"
                    }
                )

    def stop(self):
        self.db.logp(f"Stopping transmission server on address [{self.host}:{self.port}] with password '{self.password}'")