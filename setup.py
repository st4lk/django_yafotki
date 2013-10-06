#!/usr/bin/env python


import os
from distutils.core import setup

packages, data_files = [], []
root_dir = os.path.dirname(__file__)


for dirpath, dirnames, filenames in os.walk('yafotki'):
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'):
            del dirnames[i]
    if '__init__.py' in filenames:
        pkg = dirpath.replace(os.path.sep, '.')
        if os.path.altsep:
            pkg = pkg.replace(os.path.altsep, '.')
        packages.append(pkg)
    elif filenames:
        prefix = dirpath[10:]
        for f in filenames:
            data_files.append(os.path.join(prefix, f))

setup(
    name='django-yafotki',
    description='Yandex.Fotki files backend for django',
    author='Serge A Makarov',
    author_email='serg.makar@gmail.com',
    license = 'BSD Licence',
    version = '0.5',
    url='https://bitbucket.org/redsnow/django-yafotki',
    package_dir={'yafotki': 'yafotki'},
    packages=packages,
    package_data={'yafotki': data_files},
    install_requires=['feedparser']
)
