class DBConverter:
    def __init__(self):
        pass

    def toNewVersion(self, db, data):
        data.update(
            {
                "version": db.version
            }
        )