import sqlite3
import base64
import pypastebin.settings as settings
import os

class database :
    def __init__(self):
        if not os.path.isfile(settings.database):
            os.system("echo \"CREATE TABLE paste (id text, paste text);\" | sqlite3 \"{}\"".format(settings.database))

        self.db = sqlite3.connect(settings.database)
        self.cur = self.db.cursor()

    def exec(self,cmd):
        ret = self.cur.execute(cmd).fetchall()
        self.db.commit()
        return ret

    def get(self,id):
        paste = self.exec("SELECT * FROM paste WHERE id=\"{}\"".format(
            b64_encode(id),
        ))
        if len(paste) == 0:
            return None
        paste = b64_decode(str(paste[0][1]))
        return paste

    def add(self, id, paste):
        if self.get(id) != None:
            return
        self.exec("INSERT OR REPLACE INTO paste (id,paste) VALUES(\"{}\", \"{}\");".format(
            b64_encode(id),
            b64_encode(paste),
        ))


def b64_encode(data):
    fdata = base64.b64encode(data.encode("utf-8", errors='ignore')).decode("utf-8", errors='ignore')
    return fdata

def b64_decode(data):
    fdata = base64.b64decode(data.encode("utf-8", errors='ignore')).decode("utf-8", errors='ignore')
    return fdata
