# -*- coding: UTF-8 -*-

import re
from bisect import bisect

from django.db.models.fields.files import  FieldFile,FileField
from yafotki.storage import YFStorage


class YFFieldFile(FieldFile):

    SIZES = {
        50: 'XXXS',
        75: 'XXS',
        100: 'XS',
        150: 'S',
        300: 'M',
        500: 'L',
        800: 'XL'
        }
    size_re = re.compile(r'src_(\w+)$')

    def __init__(self, *args, **kwargs):
        super(YFFieldFile, self).__init__(*args, **kwargs)
        self.storage = YFStorage()

    def __getattr__(self, name):
        match = self.size_re.match(name)
        if match:
            return self.src(size=match.group(1))
        return super(YFFieldFile, self).__getattr__(name)


    def src(self, size = None):
        default_url = self.storage.url(self.name)
        if size is not None:
            if size != 'orig':
                sizes = self.SIZES.keys()
                sizes.sort()
                try:
                    size = self.SIZES[sizes[bisect(sizes, int(size)-1)]]
                except IndexError:
                    size = self.SIZES[sizes[-1]]

            return default_url[:-2]+size
        return default_url


class YFField(FileField):
    attr_class = YFFieldFile

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('upload_to', 'default')
        kwargs.setdefault('max_length', 255)
        super(YFField, self).__init__(*args, **kwargs)


try:
    from south.modelsinspector import add_introspection_rules

    add_introspection_rules([], ["^yafotki\.fields\.YFField"])

except ImportError:
    pass