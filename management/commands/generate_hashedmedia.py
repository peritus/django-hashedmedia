#!/usr/bin/env python

# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <filip@j03.de> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return Poul-Henning Kamp
# ----------------------------------------------------------------------------

from django.conf import settings
from django.core.management.base import BaseCommand
from django_hashedmedia import hashfile
from os import listdir, mkdir
from os.path import join as joinpath, exists, isdir, abspath
from shutil import copy2

putwhere = getattr(settings, 'HASHEDMEDIA_ROOT', settings.MEDIA_ROOT)

aliascommand = 'cp -v "%s" "%s"'
if getattr(settings, 'HASHEDMEDIA_USE_SYMLINKS', False):
    aliascommand = 'ln -s "%s" "%s"'

def _find(root):
    for item in [ joinpath(root, x) for x in listdir(root) ]:
        if isdir(item):
            for subitem in _find(item):
                yield subitem
        else:
            yield item

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print '''
# To actually execute this, run
#   ./manage.py generate_hashedmedia | sh

'''

        if not exists(putwhere):
            print "mkdir -v ", putwhere
       
        for asset in _find(settings.MEDIA_ROOT):
            to = joinpath(putwhere, hashfile(asset))
            print "cp -v %s %s" % (abspath(asset), abspath(to))
