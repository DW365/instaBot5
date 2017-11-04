# -*- coding: utf-8 -*-
from db import Db
from settings import Settings

SETTINGS = Settings('data')
DB = Db()
USERS = {}


def main():
    from mainTable import mainTable
    a = mainTable("1vP6dHaF1gNUZrOyBUWYrpOhuYMWrg4ttLx_onaLEXxU")
    a.getContractors()
    #a.doWork()

if __name__ == '__main__':
    main()
