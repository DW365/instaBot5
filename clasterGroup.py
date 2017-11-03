from claster import Claster


class ClasterGroup:
    def __init__(self, groups, prices):
        self.clasters = self.parseString(groups, prices)
        self.sum = 0
        self.average_subs = 0
        self.average_posts = 0

    def parseString(self, groups, prices):
        clasters = []
        data1 = groups.replace("+", "").split(";")
        data2 = prices.split(";")
        for i in range(0, len(data1)):
            inf = data1[i].split("-")
            start = int(inf[0])
            finish = int(inf[1]) if len(inf) == 2 else None
            price = float(data2[i].replace(",", "."))
            clasters.append(Claster(price, start, finish))
        return clasters

    def addSubs(self, subscribers):
        for claster in self.clasters:
            claster.addSubs(subscribers)
        self.setAverage()

    def setAverage(self):
        posts = 0
        subs = 0
        sum = 0
        count = 0
        for claster in self.clasters:
            sum += claster.sum
            for subscriber in claster.subscribers:
                posts += subscriber.posts
                subs += subscriber.advSubs
                count += 1
        self.sum = sum
        if count != 0:
            self.average_posts = posts / count
            self.average_subs = subs / count

    def __repr__(self):
        items = ("%s = %r" % (k, v) for k, v in self.__dict__.items())
        return "<%s: {%s}>" % (self.__class__.__name__, ', '.join(items))
