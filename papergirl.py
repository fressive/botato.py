import httpapi
import re
import config

konachanApi = httpapi.HttpGetAPI("https://konachan.net")
konachanPostApi = konachanApi.endpoint("/post.json")

yandereApi = httpapi.HttpGetAPI("https://yande.re")
yanderePostApi = yandereApi.endpoint("/post.json")

saucenaoApi = httpapi.HttpGetAPI("https://saucenao.com/search.php")

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
    response = "Not Found"
    
    if not sauce["results"] or len(sauce["results"]) == 0:
        flag = True
    else:
        for i in sauce["results"]:
            sim = float(i["header"]["similarity"])
            if sim >= 80.0:
                # if the similarity greater than 80%, 
                # then it is usually the source
                if i["data"]["pixiv_id"]:
                    # from pixiv
                    response = "Author: {}\nhttps://www.pixiv.net/member.php?id={}".format(i["data"]["member_name"], i["data"]["member_id"])
                elif i["data"]["author_name"] and i["data"]["author_url"]:
                    response = "Author: {}\n{}".format(i["data"]["author_name"], i["data"]["author_url"])

                if i["data"]["ext_urls"]:
                    response = "Source: {}\n\n{}".format(", ".join(i["data"]["ext_urls"]), response)
                if i["data"]["title"]:
                    response = "{}\n{}".format(i["data"]["title"], response)

                response = "Match: {}\n\n{}".format(sim, response)
                    
                break
        else:
            flag = True
    if flag:
        pass 
        # TODO: search from ascii2d

    await cls.sendMessage(message['type'], message['group'], message['qq'], response)
    