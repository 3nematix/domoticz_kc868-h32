try:
    import gevent.monkey
    gevent.monkey.patch_all()
    from requests.packages.urllib3.util.ssl_ import create_urllib3_context
    create_urllib3_context()
    import grequests
    import time
except Exception as er:
    print('Error,', er)


class Domoticz_API:

    def __init__(self):
        pass

    def send_requests(self, urls):
        try:
            self.urls = urls
            rs = (grequests.get(u) for u in self.urls)
            grequests.map(rs)
            return None

        except KeyError as er:
            print(er)
            return er

        except Exception as er:
            print('Error')
            return er


Domoticz_req = Domoticz_API()
