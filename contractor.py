from main import DB, logger

class Contractor:
    def __init__(self, clasterGroup, contractorTable, instaUser, adwList):
        self.clasterGroup = clasterGroup
        self.contractorTable = contractorTable
        self.instaUser = instaUser
        self.adwList = adwList.split(",") if adwList != "" else []

    def doWork(self):
        logger.info("Получаю подписки "+self.instaUser.username)
        self.instaUser.getNewSubscribers(self.adwList)
        logger.info("Подписки получены")
        logger.info("Разбиваю на кластеры, произвожу расчеты")
        self.clasterGroup.addSubs(DB.getDbSubs(self.instaUser.id))
        logger.info("Добавляю в таблицу")
        self.contractorTable.add(self.clasterGroup)
        logger.info("Успешно")

    def __repr__(self):
        items = ("%s = %r" % (k, v) for k, v in self.__dict__.items())
        return "<%s: {%s}>" % (self.__class__.__name__, ', '.join(items))
