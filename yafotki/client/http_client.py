#-*- coding:utf-8 -*-

import http

class YaAtomHttpClient(object):
    http_client = None
    auth_token = None

    def __init__(self, http_client = None, auth_token = None):

        self.http_client = http_client or http.HttpClient()
        self.auth_token = auth_token or None

    def set_token(self, token):
        self.auth_token = token

    def request(self, method = None, uri = None, data = None, headers = None ):
        request_headers = {}
        if headers:
            request_headers.update(headers)
        if self.auth_token:
            request_headers['Authorization'] = 'FimpToken realm="fotki.yandex.ru", token="%s"' % self.auth_token

        return self.http_client.request(method, uri, data,request_headers)


    def get(self, uri, headers = None):
        return self.request('GET', uri = uri, headers = headers )

    def post(self, uri, data = None, headers = None):
        return self.request('POST', uri = uri, data = data,headers = headers )

    def put(self, uri, data = None, headers = None):
        return self.request('PUT', uri = uri, data = data,headers = headers )

    def delete(self, uri, data = None, headers = None):
        return self.request('DELETE', uri = uri, data = data,headers = headers )





