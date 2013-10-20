Creating your Django project
============================

TODO: Actually explain what's going on and why.  Example: https://docs.djangoproject.com/en/1.5/intro/tutorial01/

Creating the project
--------------------

.. code-block:: bash

    $ django-admin.py startproject myblog
    $ cd myblog

Creating the database
---------------------

First we need to update the ``DATABASES`` variable in our settings file (``myblog/settings.py``).  For now we'll just use sqlite for our database:

.. code-block:: python

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'myblog.sqlite3',
    }

Now let's create the database and a super user account for accessing the admin interface:

.. code-block:: bash

    $ python manage.py syncdb

Enabling the admin site
-----------------------

We're going to want to use Django's built-in admin site later, so let's enable it now.

We need to add ``'django.contrib.admin'`` to ``INSTALLED_APPS`` in our settings file (``myblog/settings.py``).  Afterward it should look something like this:

.. code-block:: python

    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.admin',
    )


After adding the admin to our installed apps we need to have Django create the tables for admin:

.. code-block:: bash

    $ python manage.py syncdb

We also need to enable admin URLs and make enable auto-discovery of ``admin.py`` files in our apps.  To do this we need to uncomment some lines in our project's urls file (``myblog/urls.py``).  Afterward our urls file should look something like this:

.. code-block:: python

    from django.conf.urls import patterns, include, url

    from django.contrib import admin
    admin.autodiscover()

    urlpatterns = patterns('',
        url(r'^admin/', include(admin.site.urls)),
    )

Testing the site
----------------

Let's test our progress by running the Django test server and visiting the admin site.

In your terminal run the Django server:

.. code-block:: bash

    $ python manage.py runserver

Now visit the admin site in your browser (http://localhost:8000/admin/).
