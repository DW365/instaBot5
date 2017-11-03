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