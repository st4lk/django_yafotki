#!/usr/bin/env python

import os
from distutils.core import setup

VERSION = '0.7.3a' 

if __name__ == '__main__':
    setup(
        version = VERSION,
        description = 'Yandex.Fotki files backend for django',
        author = 'Mikhail Polykovskij',
        author_email = 'glader@gmail.com',
        url = 'https://github.com/glader/django_yafotki',
        name = 'django_yafotki',
        packages = ['yafotki', 'yafotki/client'],
        install_requires = ['feedparser', 'requests'],

        license = "BSD",
        keywords = "django yafotki",
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Web Environment',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    )                                             
