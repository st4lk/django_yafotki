#-*- coding:utf-8 -*-

import httplib
from urlparse import urlparse
import types

def parse_url(url):
    url_parts = urlparse(url)
    url = Url(url_parts)
    return url

    

class Url(object):

    protocol = None
    host = None
    port = None
    path = None

    def __init__(self, url_parts):
        if url_parts[0]:
            self.protocol = url_parts[0]
        else:
            self.protocol = 'http'

        if url_parts[1]:
            host_parts = url_parts[1].split(":")
            if host_parts[0]:
                self.host = host_parts[0]
            try:
                self.port = int(host_parts[1])
            except IndexError:
                self.port = 80
        if url_parts[2]:
            self.path = url_parts[2]


class YandexHttpClientException(Exception):
    pass


DEFAULT_CONTENT_TYPE = 'application/atom+xml'
DEFAULT_CHARSET = 'charset=utf-8'

class HttpClient(object):
    debug = False
    headers = {}

    def __init__(self, headers = None, debug = None):
        self.debug = debug or False
        self.headers = headers or {}


    def request(self, method, url, data = None, headers = None):
        all_headers = self.headers.copy()
        if headers:
            all_headers.update(headers)
        if data and 'Content-Length' not in all_headers:
            if isinstance(data, types.StringTypes):
                all_headers['Content-Length'] = str(len(data))
            else:
                pass

        if 'Content-Type' not in all_headers:
            all_headers['Content-Type'] = DEFAULT_CONTENT_TYPE
        url_object = parse_url(url)
        if 'Host' not in all_headers:
            if url_object.host:
                all_headers['Host'] = url_object.host
        connection = self.init_connection(url)
        connection.request(method, url_object.path, data, all_headers)
        return connection.getresponse()


    def init_connection(self, url):
        url = parse_url(url)
        return httplib.HTTPConnection(url.host, url.port)
   
