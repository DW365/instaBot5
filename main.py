# -*- coding: utf-8 -*-
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from clasterGroup import ClasterGroup
from contractorTable import ContractorTable
from db import Db
from settings import Settings

SETTINGS = Settings('data')
DB = Db()
USERS = {}

class mainTable:
    def __init__(self, sid):
        self.sid = sid
        scope = ['https://spreadsheets.google.com/feeds']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('test-92ef740f572c.json', scope)
        gc = gspread.authorize(credentials)
        sheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/" + sid)
        self.worksheet = sheet.get_worksheet(1)

    def getContractors(self):
        c = self.worksheet.get_all_records()
        #for i in range(0,len(c)):
            #db add line by account
            #add user by zapaska
            #add claster group by pod and prices
            #check ban
            #check closed
            #contractor table = ()
            #if db prices != prices or db.zapaska != zapaska
            # write new state to DB
            #contractor table add list
            #contractor table add info


def main():
    c = ClasterGroup("0-200;201-500;501-700;701-1000;1000+", "20;18;15;12,5;8")
    from instaUser import InstaUser
    u = InstaUser('lonyowl')
    u.getNewSubscribers(['lonyowl','buzova86','vitabudaeva86'])
    c.addSubs(u.new_subscribers)
    # print(c)
    # a = mainTable("1vP6dHaF1gNUZrOyBUWYrpOhuYMWrg4ttLx_onaLEXxU")
    # a.getContractors()
    a = ContractorTable("1asfaa23", "456", "0-200;201-500;501-700;701-1000;1000+",
                        "1othHRfy6yuoDowRIqfEQpG9sDBWeCaD0sQ6ylUJa9u4")
    a.addLine(c)
    print(a.sid)
    # a.addWorksheet()

if __name__ == '__main__':
    main()
