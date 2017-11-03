import time

from main import SETTINGS
from tools import Tools


class Subscriber:
    def __init__(self, username):
        self.username = username
        data = Tools.getUser(username)
        self.id = data['id']
        self.subscriptions_count = int(data['follows']['count'])
        self.posts = int(data['media']['count'])
        self.advSubs = self.checkAdvSub(SETTINGS.adv_list)
        time.sleep(1)

    def checkAdvSub(self, adv_list):
        resp = SETTINGS.IAPI.getUserFollowings(self.id)
        subscriptions = [u.getUsername() for u in resp.getFollowings()]
        counter = 0
        for s in subscriptions:
            if s in adv_list:
                counter += 1
        while resp.getNextMaxId() is not None:
            resp = SETTINGS.IAPI.getUserFollowings(self.id, resp.getNextMaxId())
            subscriptions.extend([u.getUsername() for u in resp.getFollowings()])
            for s in subscriptions:
                if s in adv_list:
                    counter += 1
            time.sleep(0.5)
        return counter

    def __repr__(self):
        items = ("%s = %r" % (k, v) for k, v in self.__dict__.items())
        return "\n<%s: {%s}>" % (self.__class__.__name__, ', '.join(items))