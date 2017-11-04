import datetime

import gspread
from oauth2client.service_account import ServiceAccountCredentials


class ContractorTable:
    def __init__(self, account, adw_account, clasters, link=None):
        scope = ['https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('test-92ef740f572c.json', scope)
        self.gc = gspread.authorize(credentials)

        self.account = account
        self.adw_account = adw_account
        self.clasters = clasters

        if link is not None:
            self.link = link
            self.sheet = self.gc.open_by_url(link)
            self.worksheet = self.sheet.worksheets()[-1]
        else:
            self.sheet = self.gc.create(account)
            self.sheet.share(None, perm_type='anyone', role='reader')
            self.link = "https://docs.google.com/spreadsheets/d/"+self.sheet.id
            self.worksheet = self.sheet.worksheets()[-1]
            self.createHeader()

    def delete(self):
        self.gc.del_spreadsheet(self.sheet.id)

    def createHeader(self):
        # self.worksheet.resize(2, 7 + 4 * len(self.clasters.split(";")))
        # self.worksheet.update_cell(1, 1, ' 📆📆📆📆📆')
        # self.worksheet.update_cell(2, 1, ' 📆    Дата   📆')
        #
        # self.worksheet.update_cell(1, 2, '👥👥👥👥👥')
        # self.worksheet.update_cell(2, 2, '👥 Аккаунт  👥')
        #
        # self.worksheet.update_cell(1, 3, '👥👥👥👥👥')
        # self.worksheet.update_cell(2, 3, '👥 Запаска  👥')
        #
        # self.worksheet.update_cell(1, 4, '📈📈📈📈📈📈')
        # self.worksheet.update_cell(2, 4, ' Подписчиков')
        #
        # self.worksheet.update_cell(1, 5, '💰💰💰💰💰💰')
        # self.worksheet.update_cell(2, 5, '💰  Cумма:  💰')
        #
        # self.worksheet.update_cell(1, 6, '📰📰📰📰📰')
        # self.worksheet.update_cell(2, 6, 'Постов в сред.')
        #
        # self.worksheet.update_cell(1, 7, '✅✅✅✅✅')
        # self.worksheet.update_cell(2, 7, 'Подпис. в сред.')
        #
        # x = 8
        # cls = self.clasters.split(";")
        # for i in cls:
        #     if i != cls[len(cls) // 2]:
        #         self.worksheet.update_cell(1, x, '📈📈📈📈📈📈')
        #     else:
        #         self.worksheet.update_cell(1, x, ' 📈Подписок📈')
        #     self.worksheet.update_cell(2, x, "🔻 " + i + " 🔺")
        #     x += 1
        #
        # for i in cls:
        #     if i != cls[len(cls) // 2]:
        #         self.worksheet.update_cell(1, x, '💰💰💰💰💰💰')
        #     else:
        #         self.worksheet.update_cell(1, x, 'Цены за подписчиков')
        #     self.worksheet.update_cell(2, x, "💲 " + i + " 💲")
        #     x += 1
        #
        # for i in cls:
        #     if i != cls[len(cls) // 2]:
        #         self.worksheet.update_cell(1, x, '📄📄📄📄📄📄')
        #     else:
        #         self.worksheet.update_cell(1, x, 'Постов у подписчиков')
        #     self.worksheet.update_cell(2, x, "📌 " + i + " 📌")
        #     x += 1
        #
        # for i in cls:
        #     if i != cls[len(cls) // 2]:
        #         self.worksheet.update_cell(1, x, '🔗🔗🔗🔗🔗')
        #     else:
        #         self.worksheet.update_cell(1, x, 'В среднем подписывается на рекламодателей')
        #     self.worksheet.update_cell(2, x, "🔗 " + i + " 🔗")
        #     x += 1
        self.worksheet.resize(2, 7 + 4 * len(self.clasters.split(";")))
        self.worksheet.update_cell(1, 1, '')
        self.worksheet.update_cell(2, 1, 'Дата')

        self.worksheet.update_cell(1, 2, '')
        self.worksheet.update_cell(2, 2, 'Аккаунт')

        self.worksheet.update_cell(1, 3, '')
        self.worksheet.update_cell(2, 3, 'Запаска')

        self.worksheet.update_cell(1, 4, '')
        self.worksheet.update_cell(2, 4, 'Подписчиков')

        self.worksheet.update_cell(1, 5, '')
        self.worksheet.update_cell(2, 5, 'Cумма')

        self.worksheet.update_cell(1, 6, '')
        self.worksheet.update_cell(2, 6, 'Постов в среднем')

        self.worksheet.update_cell(1, 7, '')
        self.worksheet.update_cell(2, 7, 'Подписчиков в среднем')

        x = 8
        cls = self.clasters.split(";")
        for i in cls:
            self.worksheet.update_cell(1, x, 'Подписок')
            self.worksheet.update_cell(2, x, i)
            x += 1

        for i in cls:
            self.worksheet.update_cell(1, x, 'Цены за подписчиков')
            self.worksheet.update_cell(2, x, i)
            x += 1

        for i in cls:
            self.worksheet.update_cell(1, x, 'Постов у подписчиков')
            self.worksheet.update_cell(2, x, i)
            x += 1

        for i in cls:
            self.worksheet.update_cell(1, x, 'В среднем подписывается на рекламодателей')
            self.worksheet.update_cell(2, x, i)
            x += 1

    def addWorksheet(self):
        self.worksheet = self.sheet.add_worksheet(title="Sheet" + str(len(self.sheet.worksheets()) + 1), rows="1",
                                                  cols="1")
        self.createHeader()

    def addLine(self, clasterGroup):
        values = []
        values.append(datetime.datetime.now().strftime("%d.%m.%Y"))
        values.append(self.account)
        values.append(self.adw_account)
        values.append(clasterGroup.count)
        values.append(clasterGroup.sum)
        values.append(round(clasterGroup.average_posts))
        values.append(round(clasterGroup.average_subs))
        for claster in clasterGroup.clasters:
            values.append(claster.count)
        for claster in clasterGroup.clasters:
            values.append(claster.price)
        for claster in clasterGroup.clasters:
            values.append(round(claster.average_posts))
        for claster in clasterGroup.clasters:
            values.append(round(claster.average_subs))
        self.worksheet.append_row(values)