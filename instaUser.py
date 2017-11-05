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
            self.new_subscribers = []
            self.count = len(self.new_subscribers)
            USERS[username] = self

    def copy(self):
        return copy.deepcopy(self)

    def getNewSubscribers(self, adv_list):
        last = DB.getLastSubscribers(self.username)
        first = False
        if len(last) == 0:
            first = True
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
        if first:
            needMore = False
            DB.setLastSubscribers(self.username, new_subs)
            return []
        subscribers.extend(new_subs)

        while resp.getNextMaxId() is not None and needMore:
            resp = SETTINGS.IAPI.getUserFollowers(self.id, resp.getNextMaxId())
            subscribers_raw = ([u.getUsername() for u in resp.getFollowings()])

            new_subs, needMore = parse_raw(subscribers_raw)
            subscribers.extend(new_subs)
            time.sleep(float(SETTINGS.delay))
        DB.setLastSubscribers(self.username, subscribers)
        self.new_subscribers = [Subscriber(self.id, s, adv_list) for s in subscribers]
        self.count = len(self.new_subscribers)

    def __repr__(self):
        items = ("%s = %r" % (k, v) for k, v in self.__dict__.items())
        return "<%s: {%s}>" % (self.__class__.__name__, ', '.join(items))