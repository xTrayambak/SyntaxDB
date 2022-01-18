import requests

from multiprocessing.pool import ThreadPool

class DataReceiver:
    def __init__(self, url: str, port: int, password: str):
        self.url = url
        self.port = port
        self.password = password

    def _run(self):
        URL = f"{self.url}:{self.port}/sdbdatatransfer?password={self.password}"

        return requests.get(URL).json()

    def run(self):
        pool = ThreadPool(1)
        results = pool.apply_async(self._run).get()

        return results