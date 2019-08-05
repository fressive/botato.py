# osu!game functions

import config
import diskcache
import httpapi

osuctx = diskcache.Cache("osuctx")
osuuser = diskcache.Cache("osuuser")
# store player data

cabbageApi = httpapi.HttpGetAPI("https://www.mothership.top/api/v1")
cabbageBindInformationApi = cabbageApi.endpoint("/user/qq")
cabbageRecentImageApi = cabbageApi.endpoint("/")

osuApi = httpapi.HttpGetAPI("https://osu.ppy.sh/api/")
osuGetUserApi = osuApi.endpoint("get_user")
# APIs

class GameMode:
    def __init__(self, id):
        self.id = id

    def __repl__(self):
        if self == STD:
            return "osu!"
        elif self == TAIKO:
            return "osu!Taiko"
        elif self == CTB:
            return "osu!CatchTheBeat"
        elif self == MANIA:
            return "osu!mania"
        else:
            return "Unknown GameMode(id={})".format(self.id)

    @staticmethod
    def getMode(m):
        m = str(m).lower()
        if m in modemap:
            return modemap[m]

STD = GameMode(0)
TAIKO = GameMode(1)
CTB = GameMode(2)
MANIA = GameMode(3)

modemap = {
    "s": STD, "0": STD, "std": STD, "osu!standard": STD, "osu!": STD,
    "t": TAIKO, "1": TAIKO, "taiko": TAIKO, "osu!taiko": TAIKO,
    "c": CTB, "2": CTB, "ctb": CTB, "catchthebeat": CTB, "osu!ctb": CTB, "osu!catchthebeat": CTB,
    "m": MANIA, "3": MANIA, "mania": MANIA, "osu!mania": MANIA
}


class OsuUser:
    osu_data = {}

    def __refreshCache(self, key):
        osuuser.set(key, self, expire=86400)
        # set expire time to 1 day

    @property
    def osuid(self):
        return -1 if len(self.osu_data) == 0 else int(list(self.osu_data.values())[0]["user_id"])

    def __init__(self, uid = None, username = None, init = True):
        if not uid and not username:
            raise ValueError("Uid or username must be specific.")

        self.uid = uid
        self.username = username

        self.__refreshCache(self.osuid)

    async def updateUserData(self):
        for i in range(0, 4):
            await self.getOsuUserData(self.uid if self.uid else self.username, GameMode.getMode(i), "id" if self.uid else "string")

    async def getOsuUserData(self, user, mode = STD, type = "id"):
        rep = (await osuGetUserApi.call({
                "k": config.osu_api_key,
                "u": user,
                "m": mode.id,
                "type": type
        }))
        rep = rep.json()
        if len(rep) == 0:
            return False, -1
        else:
            self.osu_data[mode.id] = rep[0]
            self.__refreshCache(self.osuid)
            return True, 0
    
    @staticmethod
    def getUser(uid):
        return osuuser[uid] if uid in osuuser else OsuUser(uid)
    
class OsuContext:
    qq = -1
    cabbage_data = None
    osu_user = None

    def __refreshCache(self, key):
        osuctx.set(key, self, expire=86400)
        # set expire time to 1 day

    def __init__(self, qq):
        self.qq = qq

        self.__refreshCache(self.qq)

    def updateUser(self):
        self.osu_user = OsuUser.getUser(self.osuid)

    @staticmethod
    def getContext(qq):
        return osuctx[qq] if qq in osuctx else OsuContext(qq)

    @property
    def osuid(self):
        return -1 if not self.cabbage_data else self.cabbage_data["data"]["userId"]

    @property
    def osuname(self):
        return "" if not self.cabbage_data else self.cabbage_data["data"]["currentUname"]


    async def getCabbageBindInformation(self):
        if not self.cabbage_data:
            rep = (await cabbageBindInformationApi.endpoint("/{}".format(self.qq)).call()).json()
            if rep['code'] != 0:
                return False, rep['code']
            self.cabbage_data = rep
            self.__refreshCache(self.qq)
            return True, 0

def drawrecent(uid):
    pass

async def recent(cls, phrase, message):
    uid = 0
    mode = STD

    if phrase.get("~query", None):
        # get uid from username
        pass
    if phrase.get("~mode", None):
        mode = GameMode.getMode(phrase.get("~mode"))

    ctx = OsuContext.getContext(int(message["qq"]))

    await ctx.getCabbageBindInformation()
    print(osuctx.get(int(message["qq"])).cabbage_data)

async def osudebug(cls, phrase, message):
    ctx = OsuContext.getContext(int(message["qq"]))

    await ctx.getCabbageBindInformation()
    ctx.updateUser()
    await ctx.osu_user.updateUserData()

    result = "Username: {name}\nUID: {id}\nCabbage Data: {cabbage}\n osu![/get_user] Data: {osuu}"
    await cls.sendMessage(message['type'], message['group'], message['qq'], result.format(\
        name = ctx.osuname,\
        id = ctx.osuid,\
        cabbage = ctx.cabbage_data,\
        osuu = ctx.osu_user.osu_data))
    
