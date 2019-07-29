import requests_async as requests

# 对 HttpAPI 的封装

class HttpAPI:
    def __init__(self, url):
        self.url = url

    def call(self):
        raise NotImplementedError

    def endpoint(self, endpoint):
        return HttpAPI(self.url + endpoint)

class HttpGetAPI(HttpAPI):
    async def call(self, params = None, **kwargs):
        return await requests.get(self.url, params=params, **kwargs)

class HttpPostAPI(HttpAPI):
    async def call(self, data=None, json=None, **kwargs):
        return await requests.post(self.url, data, json, **kwargs)