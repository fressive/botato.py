import requests_async as requests

# 对 HttpAPI 的封装

class HttpAPI:
    def __init__(self, url):
        self.url = url

    async def call(self):
        raise NotImplementedError

    def endpoint(self, endpoint):
        return HttpAPI(self.url + endpoint)

class HttpGetAPI(HttpAPI):

    def __init__(self, url):
        super().__init__(url)

    async def call(self, params = None, **kwargs):
        return await requests.get(self.url, params=params, **kwargs)

    def endpoint(self, endpoint):
        return HttpGetAPI(self.url + endpoint)

class HttpPostAPI(HttpAPI):
    def __init__(self, url):
        super().__init__(url)

    async def call(self, data=None, json=None, **kwargs):
        return await requests.post(self.url, data, json, **kwargs)

    def endpoint(self, endpoint):
        return HttpPostAPI(self.url + endpoint)