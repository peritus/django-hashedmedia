==================
django_hashedmedia
==================

:Author: `Filip Noetzel <http://filip.noetzel.co.uk/>`_
:Version: v0.01
:Web: http://j03.de/projects/django_hashedmedia/
:Source: http://j03.de/projects/django_hashedmedia/git/ (also `on github <http://github.com/peritus/django_hashedmedia/>`_)
:Download: http://j03.de/projects/django_hashedmedia/releases/

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

::

  git clone git://github.com/peritus/django-hashedmedia.git

Using tarball:

::

  wget http://github.com/peritus/django-hashedmedia/tarball/master
  tar -xvzf peritus-django-hashedmedia*.tar.gz  
  rm peritus-django-hashedmedia*.tar.gz
  mv peritus-django-hashedmedia* django-hashedmedia

Installation
------------
Put the folder django_hashedmedia somewhere in your ``$PYTHONPATH`` (presumably your project folder, where your manage.py lives).

Preparing your templates
------------------------

Replace your MEDIA_URL references with the tag hashed_media_url:

So,

::

  <img src="{{ MEDIA_URL }}round_corners.png" />

would become

::

  <img src="{% hashed_media_url "round_corners.png" %}" />

(Don't worry about using the ``{% load .. %}`` directive, the tag is added to
every template automatically.)

Config
------

Open your ``settings.py`` and append the following lines (these are the default values, adapt to your needs):

::

  HASHEDMEDIA_ENABLED = not DEBUG

(Enable django_hashedmedia at all, if set to False, hashed_media_url behaves just like MEDIA_URL.)

::

  HASHEDMEDIA_MEDIA_ROOT = MEDIA_ROOT

(Where to put the renamed files.)

For your production setup make sure your asset location points to whatever you specified at HASHED_MEDIA_ROOT.

Configure your webserver:

Lighttpd

::

  $HTTP["host"] == "static.example.com" {

    $HTTP["url"] =~ "^/[0-9a-zA-Z\_\-]{27}\..{1,5}$" {
        expire.url = ( "" => "access 10 years" )
    }

    # .. ..
  }

Apache

::

  TBD


Usage
-----

Django's builtin development server:

  If you want to try if everything is working correctly with django_hashedmedia, set HASHEDMEDIA_ENABLED to True, if you want to develop with the speaking names of your asset files, set it to False.

Production (Apache, Lighttpd, ..):

  Upon each deployment, run

  ::

    ./manage.py generate_hashedmedia | sh


Other
-----

django-hashedmedia is licensed as Beerware, patches and suggestions are welcome.

