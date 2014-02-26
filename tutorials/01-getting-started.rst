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

You should also have `pip`_ installed on your machine.  First let's install Django 1.6:

.. code-block:: bash

    $ pip install django==1.6.2
    Downloading/unpacking Django==1.6.2
      Downloading Django-1.6.2.tar.gz (6.6MB): 6.6MB downloaded
      Running setup.py egg_info for package Django

        warning: no previously-included files matching '__pycache__' found under directory '*'
        warning: no previously-included files matching '*.py[co]' found under directory '*'
    Installing collected packages: Django
      Running setup.py install for Django
        changing mode of build/scripts-2.7/django-admin.py from 644 to 755

        warning: no previously-included files matching '__pycache__' found under directory '*'
        warning: no previously-included files matching '*.py[co]' found under directory '*'
        changing mode of /home/trey/.virtualenvs/tdd_workshop/bin/django-admin.py to 755
    Successfully installed Django
    Cleaning up...

.. HINT::
   Things you should type into your terminal or command prompt will always
   start with ``$`` in this workshop. Don't type the leading ``$`` though.

Running the next command will show the version of Django you have installed.
For this workshop, a 1.6.x version is required. If instead you see a
"No module named django" message, please follow the Django
`installation instructions`_.

.. _installation instructions: https://docs.djangoproject.com/en/1.6/topics/install/

.. code-block:: bash

    $ python -c "import django; print(django.get_version())"
    1.6.2


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


Setting up the database
-----------------------

One building block of virtually all websites that contain user-generated
content is a database. Databases facilitate a good separation between
code (Python and Django in this case), markup and scripts (HTML, CSS and
JavaScript) and actual content (database). Django and other frameworks help
guide developers to separate these concerns.

First, let's create the database and a super user account for accessing the
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


The admin site
--------------

One of the killer features Django provides is an admin interface. An admin
interface is a way for an administrator of a website to interact with the
database through a web interface which regular website visitors are not
allowed to use. On a blog, this would be where the author writes new blog
posts.

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

    .. _official documentation: https://docs.djangoproject.com/en/1.6/intro/tutorial01/#the-development-server


Python Package Requirements File
--------------------------------

We want to use a few more Python packages besides Django.  We'll plan to use `WebTest`_ and `django-webtest`_ for our functional tests.  Let's install those also:

.. code-block:: bash

    $ pip install webtest django-webtest
    Downloading/unpacking Django==1.6.2
      Downloading Django-1.6.2.tar.gz (6.6MB): 6.6MB downloaded
      Running setup.py egg_info for package Django

        warning: no previously-included files matching '__pycache__' found under directory '*'
        warning: no previously-included files matching '*.py[co]' found under directory '*'
    Installing collected packages: Django
      Running setup.py install for Django
        changing mode of build/scripts-2.7/django-admin.py from 644 to 755

        warning: no previously-included files matching '__pycache__' found under directory '*'
        warning: no previously-included files matching '*.py[co]' found under directory '*'
        changing mode of /home/trey/.virtualenvs/tdd_workshop/bin/django-admin.py to 755
    Successfully installed Django
    Cleaning up...

We don't want to manually install our dependencies every time.  Let's create a `requirements file`_ listing our dependiences so we don't have to type them all out every time we setup our website on a new computer or anytime a package version updates.

First let's use `pip freeze`_ to list our dependencies and their versions:

.. code-block:: bash

    $ pip freeze
    Django==1.6.2
    WebOb==1.3.1
    WebTest==2.0.14
    argparse==1.2.1
    beautifulsoup4==4.3.2
    django-webtest==1.7.6
    six==1.5.2
    waitress==0.8.8
    wsgiref==0.1.2

We care about the ``Django``, ``WebTest``, and ``django-webtest`` lines here.  The other packages are sub-dependencies that were automatically installed and don't need to worry about them.  Let's create our ``requirements.txt`` file with instructions for installing these packages with the versions we have installed now::

    Django==1.6.2
    WebTest==2.0.14
    django-webtest==1.7.6


This file will allow us to install all Python dependencies at once with just one command.  Whenever our dependency files are upgraded or if we setup a new development environment for our Django website we'll need to run:

.. code-block::

    $ pip install -r requirements.txt

.. NOTE::
    Note that we do not need to type this command right now since we have already installed all dependencies.


.. _WebTest: http://webtest.readthedocs.org/en/latest/
.. _django-webtest: https://pypi.python.org/pypi/django-webtest/
.. _pip: http://www.pip-installer.org/en/latest/installing.html
