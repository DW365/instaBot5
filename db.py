import sqlite3
import datetime


class Db:
    def __init__(self):
        self.db = sqlite3.connect("db.db")
        self.cursor = self.db.cursor()
        self.initUsers()
        self.initContractors()
        self.initSubs()
        self.applyChanges()

    def applyChanges(self):
        self.db.commit()

    def initUsers(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS 'users' (username TEXT PRIMARY KEY, last_subs TEXT, status TEXT)")

    def initSubs(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS 'subscribers' (owner TEXT, username TEXT, advSubs INTEGER, posts INTEGER, subscriptions_count INTEGER, date TEXT, userowner TEXT PRIMARY KEY)")

    def initContractors(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS 'contractors' (account TEXT PRIMARY KEY, adw_account TEXT, clasters TEXT, prices TEXT)")

    def getLastSubscribers(self, username):
        resp = self.cursor.execute("SELECT * FROM users WHERE username = ?", [username]).fetchall()
        if len(resp) != 0 and resp[0][1] != "":
            return resp[0][1].split(",")
        return []

    def setLastSubscribers(self, username, subscribers):
        cur5 = self.getLastSubscribers(username)
        last5 = subscribers[:10]
        last5.extend(cur5[:10 - len(last5)])
        self.cursor.execute("INSERT OR IGNORE INTO users VALUES (?,?,?)", [username, "", "OK"])
        self.cursor.execute("UPDATE users SET last_subs = ? WHERE username = ?", [",".join(last5), username])
        self.applyChanges()

    def checkAccount(self, account):
        return len(self.cursor.execute("SELECT * FROM contractors WHERE account = ?", [account]).fetchall()) != 0

    def addAccount(self, account, adw_account, clasters, prices):
        self.cursor.execute("INSERT OR IGNORE INTO contractors VALUES (?,?,?,?)",
                            [account, adw_account, clasters, prices])
        self.applyChanges()

    def needNewPage(self, account, adw_account, clasters, prices):
        line = self.cursor.execute("SELECT * FROM contractors WHERE account = ?", [account]).fetchall()[0]
        if adw_account != line[1] or clasters != line[2] or prices != line[3]:
            return True
        return False

    def updateAccount(self, account, adw_account, clasters, prices):
        self.cursor.execute("UPDATE contractors SET adw_account = ?, clasters = ?, prices = ? WHERE account = ?",
                            [adw_account, clasters, prices, account])
        self.applyChanges()

    def addSubscriber(self, owner, username, advSubs, posts, subscriptions_count):
        self.cursor.execute("INSERT OR IGNORE INTO subscribers VALUES (?,?,?,?,?,?,?)",
                            [owner, username, advSubs, posts, subscriptions_count,
                             datetime.datetime.now().strftime("%d.%m.%Y"), username+owner])
        self.applyChanges()

    def getDbSubs(self, owner):
        from subscriber import Subscriber
        subs = []
        for i in self.cursor.execute("SELECT * FROM subscribers WHERE owner = ? and date = ?", [owner, datetime.datetime.now().strftime("%d.%m.%Y")]).fetchall():
            s = Subscriber("", "", "", True)
            s.emptyInit(i[0], i[1], i[2], i[3], i[4])
            subs.append(s)
        return subs
