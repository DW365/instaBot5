import sqlite3


class Db:
    def __init__(self):
        self.db = sqlite3.connect("db.db")
        self.cursor = self.db.cursor()
        self.initUsers()

    def applyChanges(self):
        self.db.commit()

    def initUsers(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS 'users' (username TEXT PRIMARY KEY, last_subs TEXT, status TEXT)")

    def getLastSubscribers(self, username):
        resp = self.cursor.execute("SELECT * FROM users WHERE username = ?", [username]).fetchall()
        if len(resp) != 0:
            return resp[0][1].split(",")
        return []

    def setLastSubscribers(self, username, subscribers):
        cur5 = self.getLastSubscribers(username)
        last5 = subscribers[:5]
        last5.extend(cur5[:5-len(last5)])
        self.cursor.execute("INSERT OR IGNORE INTO users VALUES (?,?,?)", [username, "", "OK"])
        self.cursor.execute("UPDATE users SET last_subs = ? WHERE username = ?", [",".join(last5), username])
        self.applyChanges()