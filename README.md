Welcome
=======

Welcome to django-yafotki github page. Django-yafotki provides access to Yandex.Fotki picture storage from Django.
This repository cloned from https://bitbucket.org/redsnow/django-yafotki. Author - Serge A Makarov.

Installation
------------

Install using pip

    pip install django_yafotki

or get source code from github

    git clone git://github.com/glader/django_yafotki.git


Add your Yandex account info into settings.py

    YAFOTKI_STORAGE_OPTIONS = {
        'username': 'your_yandex_account_name',
        'token': 'your_token'
    }

You can obtain token by following instructions at page http://api.yandex.ru/oauth/doc/dg/tasks/get-oauth-token.xml

Add Yandex.Fotki field to your model

    ...
    from yafotki.fields import YFField
    ...
    class MyModel(models.Model):
        ...
        yandex_fotki_image = YFField(upload_to='album_name')
        ...

Using in views and templates
----------------------------

Use MyModel.yandex_fotki_image.src attribute for access to image source.

    ...
    <img src="{{ img.yandex_fotki_image.src }}" />
    ...

If you can access to different image sizes use MyModel.yandex_fotki_image.src_100, for access 100px width image, and MyModel.yandex_fotki_image.src for original image size

    ...
    <img src="{{ img.yandex_fotki_image.src_100 }}" width="100" /> <!-- 100px width image -->
    ...
    <img src="{{ img.yandex_fotki_image.src_300 }}" width="300" /> <!-- 300px width image -->
    ...
    <img src="{{ img.yandex_fotki_image.src }}"  /> <!-- Original image widht -->


Using with django-wysiwyg-redactor
----------------------------------

You can set up django_yafotki to upload images from wysiwyg redactor directly to Fotki without any model. Just set a handler

    REDACTOR_UPLOAD_HANDLER = 'yafotki.handlers.FotkiUploader'