import requests
from main import SETTINGS

class Tools:
    @staticmethod
    def getUser(user_name, max_id=None, proxystring=None):
        proxystring = SETTINGS.proxy
        url = "https://www.instagram.com/%s/" % user_name
        proxies = {'http': proxystring,
                   'https': proxystring}
        payload = {'__a': '1'}
        if max_id is not None: payload['max_id'] = max_id

        try:
            if proxystring is not None:
                res = requests.get(url, params=payload, proxies=proxies).json()
            else:
                res = requests.get(url, params=payload).json()
            body = res['user']
            #cursor = res['user']['media']['page_info']['end_cursor']
        except:
            raise

        return body

    @staticmethod
    def getId(username):
        data = Tools.getUser(username)
        return data['id']

    @staticmethod
    def checkBan(username):
        try:
            Tools.getUser(username)
            return False
        except:
            return True

    @staticmethod
    def checkClosed(username):
        data = Tools.getUser(username)
        return data['is_private'] == True

    @staticmethod
    def getAccFromUrl(url):
        return url.split("/")[-1]
