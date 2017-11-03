# -*- coding: utf-8 -*-
from db import Db
from settings import Settings

SETTINGS = Settings('data')
DB = Db()
USERS = {}

class mainTable:
    pass


class ContractorTable:
    pass


class Claster:
    def __init__(self, price, start, finish=None):
        self.start = start
        self.finish = finish if finish is not None else 1000000
        self.subscribers = []
        self.price = price
        self.count = 0
        self.average_posts = 0
        self.average_subs = 0
        self.sum = 0

    def addSubs(self, subscribers):
        for s in subscribers:
            if self.start <= s.subscriptions_count <= self.finish:
                self.subscribers.append(s)
        self.count = len(self.subscribers)
        self.sum = self.price * self.count
        self.setAverage()

    def setAverage(self):
        if self.count != 0:
            for i in self.subscribers:
                self.average_posts += i.posts
                self.average_subs += i.advSubs
            self.average_posts /= self.count
            self.average_subs /= self.count

    def __repr__(self):
        items = ("%s = %r" % (k, v) for k, v in self.__dict__.items())
        return "\n<%s: {%s}>" % (self.__class__.__name__, ', '.join(items))

class ClasterGroup:
    def __init__(self, groups, prices):
        self.clasters = self.parseString(groups, prices)

    def parseString(self, groups, prices):
        clasters = []
        data1 = groups.replace("+","").split(";")
        data2 = prices.split(";")
        for i in range(0,len(data1)):
            inf = data1[i].split("-")
            start = int(inf[0])
            finish = int(inf[1]) if len(inf) == 2 else None
            price = float(data2[i].replace(",","."))
            clasters.append(Claster(price, start, finish))
        return clasters

    def addSubs(self, subscribers):
        for claster in self.clasters:
            claster.addSubs(subscribers)

    def __repr__(self):
        items = ("%s = %r" % (k, v) for k, v in self.__dict__.items())
        return "<%s: {%s}>" % (self.__class__.__name__, ', '.join(items))



def main():
    c = ClasterGroup("0-200;201-500;501-700;701-1000;1000+", "20;18;15;12,5;8")
    from instaUser import InstaUser
    u = InstaUser('lonyowl')
    c.addSubs(u.new_subscribers)
    print(c)

if __name__ == '__main__':
    main()
