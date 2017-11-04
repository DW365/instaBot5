class Contractor:
    def __init__(self, clasterGroup, contractorTable, instaUser, adwList):
        self.clasterGroup = clasterGroup
        self.contractorTable = contractorTable
        self.instaUser = instaUser
        self.adwList = adwList.split(",")

    def doWork(self):
        self.instaUser.getNewSubscribers(self.adwList)
        self.clasterGroup.addSubs(self.instaUser.new_subscribers)
        self.contractorTable.addLine(self.clasterGroup)