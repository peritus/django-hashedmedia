#!/usr/bin/env python

# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <filip@j03.de> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return Poul-Henning Kamp
# ----------------------------------------------------------------------------

from base64 import urlsafe_b64encode
from django.conf import settings
from django.core.cache import cache
from django.template import add_to_builtins

try:
    # Python 2.5
    from hashlib import sha1
except ImportError:
    # Python 2.4
    from sha import sha as sha1

add_to_builtins('django_hashedmedia.tags')

HASHEDMEDIA_HASHFUN = getattr(settings, "HASHEDMEDIA_HASHFUN", sha1)
HASHEDMEDIA_DIGESTLENGTH = getattr(settings, "HASHEDMEDIA_DIGESTLENGTH", 9999)

def digest(content):
    return urlsafe_b64encode(HASHEDMEDIA_HASHFUN(content).digest()[:HASHEDMEDIA_DIGESTLENGTH]).strip("=")

def hashfile(filename, no_cache=False):
  cache_key = "django_hashedmedia:%s" % filename
  fromcache = cache.get(cache_key)

  if fromcache and not no_cache:
      return fromcache

  # compute hash then
  extension = filename.split(".")[-1]
  hashed_filename = "%s.%s" % (digest(open(filename).read()), extension)

  cache.set(cache_key, hashed_filename)

  return hashed_filename
