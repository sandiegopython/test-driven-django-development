Database Migrations with Django South
=====================================

As explained in this `blog post about Django South`_, if you have a database, you should be using `Django south`_ to manage changes in your database schema.

Let's setup Django south to future-proof our website against database changes.


Installing South
----------------

First let's install South:

.. code-block:: bash

    $ pip install south
    Downloading/unpacking south
    Downloading South-0.8.4.tar.gz (97kB): 97kB downloaded
    Running setup.py egg_info for package south
    ...
    Cleaning up...

Now let's use ``pip freeze`` to check the version of South we have installed:

.. code-block:: bash

    $ pip freeze
    Django==1.6.2
    South==0.8.4
    WebOb==1.3.1
    WebTest==2.0.14
    argparse==1.2.1
    beautifulsoup4==4.3.2
    coverage==3.7.1
    django-webtest==1.7.6
    six==1.5.2
    waitress==0.8.8
    wsgiref==0.1.2

Our requirements.txt file should now look like this::

    coverage==3.7.1
    Django==1.5.5
    django-webtest==1.7.5
    WebTest==2.0.9
    South==0.8.4

Now we need to add South to our ``INSTALLED_APPS`` tuple in our settings file (``myblog/settings.py``):

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'blog',
        'south',
    )

Now we need to run ``python manage.py syncdb`` to create South's database tables:

.. code-block:: bash

    $ python manage.py syncdb
    Syncing...
    Creating tables ...
    Creating table south_migrationhistory
    Installing custom SQL ...
    Installing indexes ...
    Installed 0 object(s) from 0 fixture(s)

    Synced:
    > django.contrib.admin
    > django.contrib.auth
    > django.contrib.contenttypes
    > django.contrib.sessions
    > django.contrib.messages
    > django.contrib.staticfiles
    > blog
    > south

    Not synced (use migrations):
    -
    (use ./manage.py migrate to migrate these)


Converting Our App to South
---------------------------

We didn't start our project using South, so we need to convert all of our apps to South which will create an initial migration detailing our current database schema.

Right now we only have one app called ``blog``.  We can convert it to South like this:

.. code-block:: bash

    $ python manage.py convert_to_south blog

Now let's look at the migrations we have so far in South

.. code-block:: bash

    $ python manage.py migrate --list

     blog
      (*) 0001_initial

We have a single migration file (stored under ``blog/migrations/0001_initial.py``) which contains instructions for creating our initial database tables for our ``blog`` app.

Using South
-----------

Whenever we make a change to our models that would require a change in our database (e.g. adding a model, adding a field, removing a field, etc.) we need to create a South schema migration file for our change.

To do this we will use the ``schemamigration`` command.  Let's try it out right now:

.. code-block:: bash

    $ python manage.py schemamigration --auto blog
    Nothing seems to have changed.

No migration was created because we have not made any changes to our models.

.. TIP::

    For more information about South check out check out the `South tutorial`_ in the documentation.

.. _blog post about Django south: http://www.djangopro.com/2011/01/django-database-migration-tool-south-explained/
.. _django south: http://south.aeracode.org/
.. _south tutorial: http://south.readthedocs.org/en/latest/tutorial/index.html
