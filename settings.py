import json

from InstagramAPI import Instagram


class Settings:
    def __init__(self, filename):
        self.insta_password = None
        self.insta_login = None
        with open(filename) as data_file:
            filedata = json.load(data_file)
            self.__dict__.update(filedata)
        self.IAPI = Instagram(self.insta_login, self.insta_password)
        self.IAPI.login()