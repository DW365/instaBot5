# -*- coding: utf-8 -*-
from db import Db
from settings import Settings
import logging
import traceback
import time

SETTINGS = Settings('data')
DB = Db()
USERS = {}

logger = logging.getLogger('parser')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('parser.log', 'w', 'utf-8')
ch = logging.FileHandler('parser-error.log', 'w', 'utf-8')
logging.getLogger().addHandler(logging.StreamHandler())
ch.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s  - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)

def main():
    from mainTable import mainTable
    while True:
        logger.info("Начинаю цикл")
        for i in range(3):
            try:
                logger.info("Получаю данные с главной таблицы")
                a = mainTable(SETTINGS.main_table)
                a.getContractors()
                logger.info("Список подрядчиков получен")
                a.doWork()
                USERS.clear()
                logger.info("Начинаю цикл")
                break
            except Exception as err:
                print(err)
                logger.error(str(err))
                logger.exception("ERROR")
                time.sleep(10)


if __name__ == '__main__':
    main()
