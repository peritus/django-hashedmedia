==================
django-hashedmedia
==================

:Author: `Filip Noetzel <http://filip.noetzel.co.uk/>`_
:Version: v0.01
:Web: http://j03.de/projects/django-hashedmedia/
:Git: ``git clone http://j03.de/git/django-hashedmedia.git/``
  ( `browse <http://j03.de/git/?p=django-hashedmedia.git>`_,
  also `on github <http://github.com/peritus/django-hashedmedia/>`_)
:Download: `django-hashedmedia.tar.gz <http://j03.de/git/?p=django-hashedmedia.git;a=snapshot;sf=tgz>`_

A `django <http://djangoproject.com/>`_ application, that makes `Rule #3 ('Add
a far future Expires header to your components')
<http://stevesouders.com/hpws/rule-expires.php>`_ easy and efficient.

Motivation
----------
Say, your django webapp http://example.com/ references a CSS file
http://static.example.com/main.css. A web browser loading the page for the
first time (i.e. with an empty cache) will retrieve the whole file.  The web
browser will check at any subsequent page load, whether your css file has
changed (and most of the time it has not changed).

Using django_hashedmedia, you refer to your assets (e.g. .js, .css, .png, etc.)
by it's content's hash digest (40 byte SHA1): For example, your HTML will refer
to ``blGX5jfkVqtFoZWlwlVia3l5BxI.css`` instead of ``main.css``. You then
configure your web server to serve your assets with an ``Expires:``-header that
is a few years in the far future. That way browsers need to retrieve your
assets only once and after you change them.


Download
--------

Using git:

.. sourcecode:: bash

  git clone http://j03.de/git/django-hashedmedia.git/

Using tarball:

.. sourcecode:: bash

  curl 'http://j03.de/git/?p=django-hashedmedia.git;a=snapshot;sf=tgz' > django-hashedmedia.tar.gz
  tar -xvzf django-hashedmedia.tar.gz
  rm django-hashedmedia.tar.gz

Installation
------------
Put the folder django_hashedmedia somewhere in your ``$PYTHONPATH`` (presumably
your project folder, where your manage.py lives).

Then edit settings.py and add django_hashedmedia to the list of INSTALLED_APPS:

.. sourcecode:: python
  INSTALLED_APPS = (
    # ...
    'django_hashedmedia',
  )


Preparing your templates
------------------------

Replace your ``MEDIA_URL`` references with the tag ``{% hashed_media_url %}``:

So,

.. sourcecode:: html+django

  <img src="{{ MEDIA_URL }}round_corners.png" />

would become

.. sourcecode:: html+django

  <img src="{% hashed_media_url "round_corners.png" %}" />

.. note::

  Don't worry about using the ``{% load .. %}`` directive, the tag is added to
  every template automatically.

Configuration
-------------

Open your ``settings.py`` and append the following lines (these are the default
values, adapt to your needs):

.. sourcecode:: python

  # If set to False, hashed_media_url behaves just like MEDIA_URL
  HASHEDMEDIA_ENABLED = not DEBUG

  # Where to put the renamed files.
  HASHEDMEDIA_ROOT = MEDIA_ROOT

  # URL for serving compressed media. Include a trailing slash.
  HASHEDMEDIA_URL = MEDIA_URL

  # Hashing algorithm to use (callable)
  import hashlib
  HASHEDMEDIA_HASHFUN = hashlib.sha1

  # Length of generated filename. Must be lower than digest length
  HASHEDMEDIA_DIGESTLENGTH = 9999

For your production setup make sure your webserver serves the static media from
``HASHED_MEDIA_ROOT``.

Lighttpd
++++++++

.. sourcecode:: lighttpd

  $HTTP["host"] == "static.example.com" {

    $HTTP["url"] =~ "^/[0-9a-zA-Z\_\-]{27}\..{1,5}$" {
        expire.url = ( "" => "access 10 years" )
    }

    # .. ..
  }

Apache
++++++

.. sourcecode:: apache

  #FIXME: To be documented

Usage
-----

Django's builtin development server
+++++++++++++++++++++++++++++++++++

If you want to try if everything is working correctly with django_hashedmedia,
set ``HASHEDMEDIA_ENABLED = True``, if you want to develop with the speaking names
of your asset files, set it to False.

Production (Apache, Lighttpd, ..)
+++++++++++++++++++++++++++++++++

Upon each deployment, run

.. sourcecode:: bash

  ./manage.py generate_hashedmedia | sh

Misc
----

See `django-hashedfilestorage <http://j03.de/projects/django-hashedfilestorage/>`_ for a way to add far future expires headers also to your user-uploaded data.

License
+++++++
django-hashedmedia is licensed as Beerware, patches and suggestions are welcome.
