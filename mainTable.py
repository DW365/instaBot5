import gspread
from oauth2client.service_account import ServiceAccountCredentials
from clasterGroup import ClasterGroup
from contractorTable import ContractorTable
from main import DB
from contractor import Contractor
from instaUser import InstaUser
from tools import Tools

class mainTable:
    def __init__(self, sid):
        self.sid = sid
        scope = ['https://spreadsheets.google.com/feeds']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('test-92ef740f572c.json', scope)
        gc = gspread.authorize(credentials)
        sheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/" + sid)
        self.worksheet = sheet.sheet1
        self.contractos = []

    def getContractors(self):
        c = self.worksheet.get_all_records()
        for i in range(0, len(c)):
            accban = Tools.checkBan(Tools.getAccFromUrl(c[i]['Аккаунт']))
            adwban = Tools.checkBan(Tools.getAccFromUrl(c[i]['Запаска']))
            if accban or adwban:
                closed = True
            else:
                closed = Tools.checkClosed(Tools.getAccFromUrl(c[i]['Аккаунт'])) or Tools.checkClosed(
                    Tools.getAccFromUrl(c[i]['Запаска']))

            self.worksheet.update_cell(2 + i, 7, "Да" if accban else "Нет")
            self.worksheet.update_cell(2 + i, 8, "Да" if adwban else "Нет")
            self.worksheet.update_cell(2 + i, 9, "Да" if closed else "Нет")
            if not closed:
                if c[i]['Аккаунт'] != "" and \
                   c[i]['Распределение подписок'] != "" and \
                   c[i]['Запаска'] != "" and \
                   c[i]['Цены по распределению'] != "":
                    if not DB.checkAccount(c[i]['Аккаунт']):
                        DB.addAccount(Tools.getAccFromUrl(c[i]['Аккаунт']),
                                      Tools.getAccFromUrl(c[i]['Запаска']),
                                      c[i]['Распределение подписок'],
                                      c[i]['Цены по распределению'])
                    contractor = Contractor(ClasterGroup(c[i]['Распределение подписок'], c[i]['Цены по распределению']),
                                            ContractorTable(c[i]['Аккаунт'],
                                                            c[i]['Запаска'],
                                                            c[i]['Распределение подписок'],
                                                            c[i]['Ссылка на таблицу подрядчика']),
                                            InstaUser(Tools.getAccFromUrl(c[i]['Запаска'])),
                                            c[i]['Список рекламодателей'])
                    if DB.needNewPage(Tools.getAccFromUrl(c[i]['Аккаунт']),
                                      Tools.getAccFromUrl(c[i]['Запаска']),
                                      c[i]['Распределение подписок'],
                                      c[i]['Цены по распределению']):
                        contractor.contractorTable.addWorksheet()
                        DB.updateAccount(Tools.getAccFromUrl(c[i]['Аккаунт']),
                                  Tools.getAccFromUrl(c[i]['Запаска']),
                                  c[i]['Распределение подписок'],
                                  c[i]['Цены по распределению'])

                    self.contractos.append(contractor)

    def doWork(self):
        for contractor in self.contractos:
            contractor.doWork()
