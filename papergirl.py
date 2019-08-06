
import config
import httpapi
import random
import re

konachanApi = httpapi.HttpGetAPI("https://konachan.net")
konachanPostApi = konachanApi.endpoint("/post.json")

yandereApi = httpapi.HttpGetAPI("https://yande.re")
yanderePostApi = yandereApi.endpoint("/post.json")

danbooruApi = httpapi.HttpGetAPI("https://danbooru.donmai.us")
danbooruPostApi = danbooruApi.endpoint("/posts.json")

saucenaoApi = httpapi.HttpGetAPI("https://saucenao.com/search.php")

searchApis = {
    "konachan": konachanPostApi,
    "k": konachanPostApi,
    "yandere": yanderePostApi,
    "y": yanderePostApi,
    "danbooru": danbooruPostApi,
    "d": danbooruPostApi
}

async def paper(cls, phrase, message):
    query = "rating:safe"

    if phrase.get("~query", None):
        query = "{} {}".format(phrase.get("~query", None), query)

    limit = int(phrase.get("*number", 1))
    limit = 10 if limit > 10 else limit

    pf = phrase.get("~platform", "random")

    api = random.choice(list(searchApis.values())) if pf == "random" else searchApis[pf] if pf in searchApis else searchApis["k"]

    if api != danbooruPostApi:
        query = "order:random {}".format(query)

    rep = (await api.call({
        "limit": limit,
        "tags": query,
        "random": True
    })).json()

    if len(rep) == 0:
        await cls.sendMessage(message['type'], message['group'], message['qq'], "Not found")
        return
    
    for i in rep:
        await cls.sendMessage(message['type'], message['group'], message['qq'], cls.formatImage(i["file_url"]))

img_regex = re.compile(r"\[qq:pic=(\S*)\]")

async def artist(cls, phrase, message):
    img = phrase.get("*img", None)
    
    if not img:
        await cls.sendMessage(message['type'], message['group'], message['qq'], "Input an image")
        return

    uuid = img_regex.findall(img)[0]
    
    imgurl = cls.getImageUrl(uuid)
    sauce = (await saucenaoApi.call({
        "output_type": 2,
        "api_key": config.sacuenao_api_key,
        "testmode": 1,
        "db": 999,
        "numres": 15,
        "url": imgurl
    })).json()

    flag = False
    response = ""
    
    if not sauce["results"] or len(sauce["results"]) == 0:
        flag = True
    else:
        for i in sauce["results"]:
            sim = float(i["header"]["similarity"])
            if sim >= 80.0:
                # if the similarity greater than 80%, 
                # then it is usually the source
                data = i["data"]
                if "pixivid" in data.keys():
                    # from pixiv
                    response = "Author: {}\nhttps://www.pixiv.net/member.php?id={}".format(data["member_name"], data["member_id"])
                elif "author_name" in data.keys() and "author_url" in data.keys():
                    response = "Author: {}\n{}".format(data["author_name"], data["author_url"])
                if "ext_urls" in data.keys():
                    response = "Source: {}\n\n{}".format(", ".join(data["ext_urls"]), response)
                if "source" in data.keys():
                    response = "Source: {}\n\n{}".format(data["source"], response)
                if "title" in data.keys():
                    response = "{}\n{}".format(data["title"], response)

                response = "Match: {}\n\n{}".format(sim, response)
                    
                break
        else:
            flag = True
    if flag:
        response = "Not Found"
        # TODO: search from ascii2d

    await cls.sendMessage(message['type'], message['group'], message['qq'], response)
    