class Contractor:
    def __init__(self, clasterGroup, contractorTable, instaUser, adwList):
        self.clasterGroup = clasterGroup
        self.contractorTable = contractorTable
        self.instaUser = instaUser
        self.adwList = adwList.split(",") if adwList != "" else []

    def doWork(self):
        self.instaUser.getNewSubscribers(self.adwList)
        self.clasterGroup.addSubs(self.instaUser.new_subscribers)
        self.contractorTable.addLine(self.clasterGroup)

    def __repr__(self):
        items = ("%s = %r" % (k, v) for k, v in self.__dict__.items())
        return "<%s: {%s}>" % (self.__class__.__name__, ', '.join(items))
