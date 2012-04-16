# -*- coding: UTF-8 -*-

import os
import imghdr

from django.conf import settings
from django.core.files.storage import Storage
from yafotki.client.client import YFClient


#TODO: Make queries to YF(e.g Authorization in YF) only in
class YFStorage(Storage):
    options = None
    yf_client = None

    def __init__(self, options = None):
        self.options = options or settings.YAFOTKI_STORAGE_OPTIONS

    @property
    def client(self):
        if not self.yf_client:
            self.yf_client = YFClient(username=self.options['username'], token=self.options['token'])

        return self.yf_client

    def _open(self, name, mode = 'rb'):
        pass

    def _save(self, name, content):
        album_name, image_name = os.path.split(name)
        if not album_name:
            #TODO: Get default album from config
            album_name = 'default'
        content.seek(0)
        content_type = 'image/%s' % (imghdr.what(image_name, content.read(2048)))
        content.seek(0)

        photo_obj = self.client.add_photo(album_name, image_name, content.file, content_type)
        return photo_obj.entries[0].links[3].href

    def delete(self, name):
        pass

    def exists(self, name):
        album_name, file_name = os.path.split(name)
        if not album_name:
            album_name = 'default'

        return self.client.is_exist(album_name, file_name)

    def listdir(self, path):
        pass

    def size(self, name):
        print name

    def url(self, path):
        return path


