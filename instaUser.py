import time

from main import DB, SETTINGS, USERS
from subscriber import Subscriber
from tools import Tools
import copy


class InstaUser:
    def __init__(self, username):
        if username in USERS:
            self.__dict__ = USERS[username].copy().__dict__
        else:
            self.username = username
            self.id = Tools.getId(self.username)
            self.new_subscribers = self.getNewSubscribers()

            self.count = len(self.new_subscribers)
            self.sum = 0
            self.average_posts = 0
            self.average_subs = 0
            self.setAverage()
            USERS[username] = self

    def copy(self):
        return copy.deepcopy(self)

    def getNewSubscribers(self):
        last = DB.getLastSubscribers(self.username)
        subscribers = []

        resp = SETTINGS.IAPI.getUserFollowers(self.id)
        subscribers_raw = [u.getUsername() for u in resp.getFollowings()]

        def parse_raw(subscribers_raw):
            needMore = True
            subscribers = []
            for subscriber in subscribers_raw:
                if subscriber not in last:
                    subscribers.append(subscriber)
                else:
                    DB.setLastSubscribers(self.username, subscribers)
                    needMore = False
                    break
            return subscribers, needMore

        new_subs, needMore = parse_raw(subscribers_raw)
        subscribers.extend(new_subs)

        while resp.getNextMaxId() is not None and needMore:
            resp = SETTINGS.IAPI.getUserFollowers(self.id, resp.getNextMaxId())
            subscribers_raw = ([u.getUsername() for u in resp.getFollowings()])

            new_subs, needMore = parse_raw(subscribers_raw)
            subscribers.extend(new_subs)
            time.sleep(0.5)
        DB.setLastSubscribers(self.username, subscribers)
        return [Subscriber(s) for s in subscribers]

    def setAverage(self):
        if len(self.new_subscribers) != 0:
            for i in self.new_subscribers:
                self.average_posts += i.posts
                self.average_subs += i.advSubs
            self.average_posts /= len(self.new_subscribers)
            self.average_subs /= len(self.new_subscribers)

    def __repr__(self):
        items = ("%s = %r" % (k, v) for k, v in self.__dict__.items())
        return "<%s: {%s}>" % (self.__class__.__name__, ', '.join(items))