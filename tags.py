#!/usr/bin/env python

# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <filip@j03.de> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return Poul-Henning Kamp
# ----------------------------------------------------------------------------

from django.conf import settings
from django.template import Library

register = Library()

@register.simple_tag
def hashed_media_url(realname):
    from django_hashedmedia import hashfile

    if not getattr(settings, "HASHEDMEDIA_ENABLED", False):
        return settings.MEDIA_URL + realname
    return settings.MEDIA_URL + hashfile(settings.MEDIA_ROOT + realname)
