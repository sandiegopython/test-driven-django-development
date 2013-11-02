Getting started
===============

Verifying setup
---------------

Before we get started, let's just make sure that Python and Django are
installed correctly and are the appropriate versions.

Running the following command in the MacOS or Linux terminal or in the
Windows command prompt should show the version of Python. For this workshop
you should have a 2.6.x or 2.7.x version of Python.

.. code-block:: bash

    $ python -V

You should also have `pip`_ installed on your machine, along with the `requirements.txt`_ file.

.. code-block:: bash

    # In the same directory where you downloaded requirements.txt
    $ pip install -r requirements.txt

.. HINT::
   Things you should type into your terminal or command prompt will always
   start with ``$`` in this workshop.

Running the next command will show the version of Django you have installed.
For this workshop, a 1.5.x version is required. If instead you see a
"No module named django" message, please follow the Django
`installation instructions`_.

.. _installation instructions: https://docs.djangoproject.com/en/1.5/topics/install/

.. code-block:: bash

    $ python -c "import django; print(django.get_version())"


Creating the project
--------------------

The first step when creating a new Django website is to create the project
boilerplate files.

.. code-block:: bash

    $ django-admin.py startproject myblog
    $ cd myblog

Running this command created a new directory called ``myblog/`` with a few
files and folders in it. Notably, there is a ``manage.py`` file which is a
file used to manage a number of aspects of your Django application such as
creating the database and running the development web server. Two other key
files we just created are ``myblog/settings.py`` which contains
configuration information for the application such as how to connect to the
database and ``myblog/urls.py`` which maps URLs called by a web broser
to the appropriate Python code.


Directory variables
-------------------

Add the following to the top of your ``myblog/settings.py`` file:

.. code-block:: python

    import os
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))


Setting up the database
-----------------------

One building block of virtually all websites that contain user-generated
content is a database. Databases facilitate a good separation between
code (Python and Django in this case), markup and scripts (HTML, CSS and
JavaScript) and actual content (database). Django and other frameworks help
guide developers to separate these concerns.

First we need to update the ``DATABASES`` variable in our settings file
(``myblog/settings.py``).

.. code-block:: python

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'myblog.sqlite3'),
        }
    }

Now let's create the database and a super user account for accessing the
admin interface which we'll get to shortly:

.. code-block:: bash

    $ python manage.py syncdb

After running this command, there will be a database file ``myblog.sqlite3``
in the same directory as ``manage.py``. Right now, this database only has
a few tables specific to Django. The command looks at ``INSTALLED_APPS`` in
``myblog/settings.py`` and creates database tables for models defined in
those apps' ``models.py`` files.

Later in this workshop, we will create models specific to the blog we are
writing. These models will hold data like blog posts and comments on blog
posts.

.. HINT::
    SQLite is a self-contained database engine. It is inappropriate for a
    multi-user website but it works great for development. In production,
    you would probably use PostgreSQL or MySQL. For more info on SQLite,
    see the `SQLite documentation`_.

    .. _SQLite documentation: http://sqlite.org/


Enabling the admin site
-----------------------

One of the killer features Django provides is an admin interface. An admin
interface is a way for an administrator of a website to interact with the
database through a web interface which regular website visitors are not
allowed to use. On a blog, this would be where the author writes new blog
posts.

We need to add ``'django.contrib.admin'`` to ``INSTALLED_APPS`` in our
settings file (``myblog/settings.py``).  Afterward it should look something
like this:

.. code-block:: python

    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.admin',        # we just added this
    )

After adding the admin to our installed apps we need to have Django create
the database tables for admin:

.. code-block:: bash

    $ python manage.py syncdb

We also need to enable admin URLs and enable auto-discovery of
``admin.py`` files in our apps. We will create one of these ``admin.py`` files
later to expose our blog post model and comment model to the admin interface.
To enable auto-discovery, we need to uncomment some lines in our project's
urls file (``myblog/urls.py``). Afterward our urls file should look something
like this:

.. code-block:: python

    from django.conf.urls import patterns, include, url

    from django.contrib import admin
    admin.autodiscover()

    urlpatterns = patterns('',
        url(r'^admin/', include(admin.site.urls)),
    )


Checking our progress
---------------------

Let's check our progress by running the Django test server and visiting the
admin site.

In your terminal, run the Django development server:

.. code-block:: bash

    $ python manage.py runserver

Now visit the admin site in your browser (http://localhost:8000/admin/).

.. HINT::
    The Django development server is a quick and simple web server used for
    rapid development and not for long-term production use. The development
    server reloads any time the code changes but some actions like adding
    files do not trigger a reload and the server will need to be manually
    restarted.

    Read more about the development server in the `official documentation`_.

    Quit the server by holding the control key and pressing C.

    .. _official documentation: https://docs.djangoproject.com/en/1.5/intro/tutorial01/#the-development-server

.. _pip: http://www.pip-installer.org/en/latest/installing.html
.. _requirements.txt: _static/requirements.txt
