# -*- coding: utf-8 -*-

from libthumbor import CryptoURL
from django_thumbor import conf
from django.conf import settings


crypto = CryptoURL(key=conf.THUMBOR_SECURITY_KEY)


def _remove_prefix(url, prefix_list):
    """
    Removes from the start of the URL any prefix in the list.
    :param url: The URL to remove the schema from
    :param prefix_list:
    :return: The schemaless URL
    """
    for prefix in prefix_list:
        if url.startswith(prefix):
            return url[len(prefix):]

    return url


def _remove_schema(url):
    """
    Our image host supports https:// and http:// and does not care
    which we use. Our images however are all normally https:// and
    thus we want support to strip both from the image URL.
    :param url: The URL to remove the schema from
    :return: The schemaless URL
    """
    return _remove_prefix(url, ['http://', 'https://'])


def _prepend_media_url(url):
    if url.startswith(settings.MEDIA_URL):
        url = _remove_prefix(url, settings.MEDIA_URL)
        url.lstrip('/')
        return '%s/%s' % (conf.THUMBOR_MEDIA_URL, url)
    return url


def generate_url(image_url, **kwargs):
    image_url = _prepend_media_url(image_url)
    image_url = _remove_schema(image_url)

    kwargs = dict(conf.THUMBOR_ARGUMENTS, **kwargs)
    thumbor_server = kwargs.pop(
        'thumbor_server', conf.THUMBOR_SERVER).rstrip('/')

    encrypted_url = crypto.generate(image_url=image_url, **kwargs).strip('/')

    return '%s/%s' % (thumbor_server, encrypted_url)
