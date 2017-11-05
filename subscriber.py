import time

from main import SETTINGS
from tools import Tools
from main import DB

class Subscriber:
    def __init__(self, owner, username, adv_list, empty=False):
        if not empty:
            self.owner = owner
            self.username = username
            data = Tools.getUser(username)
            self.id = data['id']
            self.subscriptions_count = int(data['follows']['count'])
            self.posts = int(data['media']['count'])
            self.advSubs = self.checkAdvSub(adv_list)
            time.sleep(0.2)
            DB.addSubscriber(owner, username, self.advSubs, self.posts, self.subscriptions_count)

    def emptyInit(self, owner, username, advSubs, posts, subscriptions_count):
        self.owner = owner
        self.username = username
        self.advSubs = advSubs
        self.posts = posts
        self.subscriptions_count = subscriptions_count

    def checkAdvSub(self, adv_list):
        resp = SETTINGS.IAPI.getUserFollowings(self.id)
        subscriptions = [u.getUsername() for u in resp.getFollowings()]
        counter = 0
        for s in subscriptions:
            if s in adv_list:
                counter += 1
        c = 0
        while resp.getNextMaxId() is not None and c < 4:
            resp = SETTINGS.IAPI.getUserFollowings(self.id, resp.getNextMaxId())
            subscriptions.extend([u.getUsername() for u in resp.getFollowings()])
            for s in subscriptions:
                if s in adv_list:
                    counter += 1
            time.sleep(0.2)
            c+=1
        return counter

    def __repr__(self):
        items = ("%s = %r" % (k, v) for k, v in self.__dict__.items())
        return "\n<%s: {%s}>" % (self.__class__.__name__, ', '.join(items))