# osu!game functions

import diskcache
import httpapi

caches = diskcache.Cache("osu")
# A dict to store player data

cabbageApi = httpapi.HttpGetAPI("https://www.mothership.top")
cabbageBindInformationApi = cabbageApi.endpoint("/api/v1/user/qq")
cabbageRecentImageApi = cabbageApi.endpoint("/api/")
class OsuContext:
    qq = 0
    group = 0
    cabbage_data = None

    def _refreshCache(self):
        caches.set(self.qq, self, expire=86400)
        # set expire time to 1 day

    def __init__(self, qq, group):
        self.qq = qq
        self.group = group
        self._refreshCache()

    @staticmethod
    def getContext(qq, group):
        return caches[qq] if qq in caches else OsuContext(qq, group)

    @property
    def osuid(self):
        return -1 if self.cabbage_data["code"] == 0 else self.cabbage_data["data"]["userId"]

    async def getCabbageBindInformation(self):
        if not self.cabbage_data:
            self.cabbage_data = await cabbageBindInformationApi.endpoint("/{}".format(self.qq)).call().json()

def recent(cls, phrase, message):
    pass
