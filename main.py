# -*- coding: utf-8 -*-
from clasterGroup import ClasterGroup
from db import Db
from settings import Settings

SETTINGS = Settings('data')
DB = Db()
USERS = {}

class mainTable:
    pass


class ContractorTable:
    pass


def main():
    c = ClasterGroup("0-200;201-500;501-700;701-1000;1000+", "20;18;15;12,5;8")
    from instaUser import InstaUser
    u = InstaUser('lonyowl')
    c.addSubs(u.new_subscribers)
    print(c)

if __name__ == '__main__':
    main()
