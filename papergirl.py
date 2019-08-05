import httpapi
import random

konachanApi = httpapi.HttpGetAPI("https://konachan.net")
konachanPostApi = konachanApi.endpoint("/post.json")

yandereApi = httpapi.HttpGetAPI("https://yande.re")
yanderePostApi = yandereApi.endpoint("/post.json")

async def paper(cls, phrase, message):
    query = "order:random rating:safe score:>=120"

    if phrase.get("~query", None):
        query = "{} {}".format(phrase.get("~query", None), query)

    limit = int(phrase.get("*number", 1))
    limit = 10 if limit > 10 else limit

    api = konachanPostApi
    rep = (await api.call({
        "limit": limit,
        "tags": query
    })).json()

    if len(rep) == 0:
        await cls.sendMessage(message['type'], message['group'], message['qq'], "Not found")
        return
    
    for i in rep:
        await cls.sendMessage(message['type'], message['group'], message['qq'], cls.formatImage(i["file_url"]))
