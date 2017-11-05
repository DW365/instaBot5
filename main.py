# -*- coding: utf-8 -*-
from db import Db
from settings import Settings

SETTINGS = Settings('data')
DB = Db()
USERS = {}


def main():
    from mainTable import mainTable
    a = mainTable("1u2f9pfw-I1Am9NnhiZRu8Ani3aCk2v1ECLOmfCAi46w")
    a.getContractors()
    a.doWork()

if __name__ == '__main__':
    main()
