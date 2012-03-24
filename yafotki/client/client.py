#-*- coding:utf-8 -*-

import os
import urllib
import xml.dom.minidom as minidom
from xml.etree import ElementTree
import feedparser
import yarsa
import http_client

#TODO: Add exceptions for all errors
class YFClientException(Exception):
    pass

class YFCreateObjectException(YFClientException):
    pass


class YFClient(object):

    APP_NAMESPACE = 'http://www.w3.org/2007/app'
    ATOM_NAMESPACE = 'http://www.w3.org/2005/Atom'

    rsa_url = 'http://auth.mobile.yandex.ru/yamrsa/key/'
    rsa_key = {}
    rsa_request_id = None
    token_url = 'http://auth.mobile.yandex.ru/yamrsa/token/'
    service_doc_url = None
    albums_link = None
    photoes_link = None
    atom_processor = None

    def __init__(self, username = None, password = None):
        self.username = username
        self.password = password
        self.http_client = http_client.YaAtomHttpClient()
        if username is not None:
            self.service_doc_url = 'http://api-fotki.yandex.ru/api/users/%s/' % self.username
        self.get_service_doc()
        if self.username and self.password:
            self.login()


    def login(self):
        self.get_rsa()
        self.encrypted_login = yarsa.encrypt("<credentials login='%s' password='%s'/>" % (self.username, self.password,), self.rsa_key)
        login_params = urllib.urlencode({
            'request_id': self.rsa_request_id,
            'credentials': self.encrypted_login
        })
        login_headers = {
            'Host': 'auth.mobile.yandex.ru',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response_data = self.http_client.post(self.token_url, login_params, login_headers).read()
        xml = minidom.parseString(response_data)
        token_node = xml.getElementsByTagName('token')[0]
        self.token = token_node.firstChild.nodeValue
        self.http_client.set_token(self.token)

    def get_service_doc(self):
        service_doc = self.http_client.get(self.service_doc_url).read()
        service_tree = ElementTree.fromstring(service_doc)
        service_collections = service_tree.findall('{%s}workspace/{%s}collection' % (self.APP_NAMESPACE, self.APP_NAMESPACE))
        self.albums_link = service_collections[0].get('href')
        self.photoes_link = service_collections[1].get('href')

    def get_albums(self):
        pass

    def add_album(self, title, summary = None):
        data = '<entry xmlns="http://www.w3.org/2005/Atom" xmlns:f="yandex:fotki"><title>%s</title><summary>%s</summary></entry>' % (title, summary,)
        response = self.http_client.post(self.albums_link, data, {
            'Content-Type': 'application/atom+xml; charset=utf-8; type=entry'
        })
        if response.status == 201:
            print "Album created"
            return feedparser.parse(response.read())
        else:
            raise YFCreateObjectException("Yandex Says: %s - %s" % (response.status, response.reason,)).__class__, YFCreateObjectException

    def add_photo(self, album, filename, content, content_type):
        if self.get_album_by_name(album):
            album_entry = self.get_album_by_name(album)
        else:
            album_entry = self.add_album(album).entries[0]
        headers = dict()
        headers['Content-Type'] = content_type
        headers['Slug'] = os.path.basename(filename)
        new_photo_response = self.http_client.post(album_entry.links[2].href, content, headers).read()
        return feedparser.parse(new_photo_response)

    def get_album_by_name(self, album_title):
        albums_data = self.http_client.get(self.albums_link).read()
        f = feedparser.parse(albums_data)
        for entry in f.entries:
            if entry.title == album_title:
                return entry
        return False

    def get_album_photoes(self, album_name):
        album = self.get_album_by_name(album_name)
        list_link = album.links[2].href
        list_xml = self.http_client.get(list_link).read()
        f = feedparser.parse(list_xml)
        return f.entries

    def is_exist(self, album, name):
        #TODO: Create test for photo is exist
        return False

    def get_rsa(self):
        rsa_data = self.http_client.get(self.rsa_url).read()
        xml = minidom.parseString(rsa_data)
        rsa_key_node = xml.getElementsByTagName('key')[0]
        self.rsa_key = rsa_key_node.firstChild.nodeValue.encode('ascii')
        rsa_id_node = xml.getElementsByTagName('request_id')[0]
        self.rsa_request_id = rsa_id_node.firstChild.nodeValue
