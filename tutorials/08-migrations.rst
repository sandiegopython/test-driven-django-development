Database Migrations
===================

If you have a database, you should be using `migrations`_ to manage
changes in your database schema.

Let's learn about migrations to future-proof our website against
database changes.

Making Migrations
-----------------

We created our project using migrations, so let's look at the
migrations we already have.

Right now we only have one app called ``blog``. We can find the
migrations in that app's ``migrations`` package:

.. code-block:: bash

    migrations
    ├── 0001_initial.py
    ├── 0002_auto_20141019_0232.py
    └── __init__.py

Now let's look at the migrations we have so far

.. code-block:: bash

    $ python manage.py migrate --list
    admin
     [X] 0001_initial
    auth
     [X] 0001_initial
    blog
     [X] 0001_initial
     [X] 0002_auto_20141019_0232
    contenttypes
     [X] 0001_initial
    sessions
     [X] 0001_initial

We actually have quite a few. Since migrations are a feature of Django
itself, each reusable app distributed with Django contains migrations
as well, and will allow you to automatically update your database
schema when their models change.

Each of those migration files stores instructions on how to correctly
alter the database with each change.

Using Migrate
-------------

Whenever we make a change to our models that would require a change in
our database (e.g. adding a model, adding a field, removing a field,
etc.) we need to create a schema migration file for our change.

To do this we will use the ``makemigrations`` command.  Let's try it out right now:

.. code-block:: bash

    $ python manage.py makemigrations blog
    No changes detected in app 'blog'

No migration was created because we have not made any changes to our models.

.. TIP::

    For more information check out `migrations`_ in the Django documentation.

.. _migrations: https://docs.djangoproject.com/en/1.7/topics/migrations/
