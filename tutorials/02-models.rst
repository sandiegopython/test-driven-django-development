Models
======

(TODO Explain what models are and why we're using them)

Creating an app
---------------

It is generally a good practice to separate your Django projects into multiple specialized (and sometimes reusable) apps.  Additionally every Django model must live in an app so you'll need at least one app for your project.

Let's create an app for blog posts and related models.  We'll call the app ``blog``:

.. code-block:: bash

    $ python manage.py startapp blog

This command should have created a ``blog`` directory with the following files::

    __init__.py
    models.py
    tests.py
    views.py

We'll be focusing on the ``models.py`` file below.

Before we can use our app we need to add it to our ``INSTALLED_APPS`` in our settings file (``myblog/settings.py``).  This will allow Django to discover the models in our ``models.py`` file so they can be added to the database when running syncdb.


Creating a model
----------------

First let's create a blog post model.  This will correspond to a database table which will hold our blog posts.  A blog post will be represented by an instance of our ``Post`` model class and each ``Post`` model instance will identify a row in our database table.

.. code-block:: python

    from django.db import models


    class Post(models.Model):
        title = models.CharField(max_length=500)
        author = models.ForeignKey('auth.User')
        body = models.TextField()
        created_at = models.DateTimeField(auto_now_add=True, editable=False)
        modified_at = models.DateTimeField(auto_now=True, editable=False)

To create the database table for our ``Post`` model we need to run syncdb again:

.. code-block:: bash

    $ python manage.py syncdb


Creating posts from the admin site
----------------------------------

We don't want to manually add posts to the database every time we want to update our blog.  It would be nice if we could use a login-secured webpage to create blog posts.  Fortunately Django's admin interface can do just that.

In order to create blog posts from the admin interface we need to register our Post model with the admin site.  We can do this by creating an ``admin.py`` file in our ``blog`` app with the following code:


.. code-block:: python

    from django.contrib import admin
    from .models import Post


    admin.site.register(Post)

Now we can navigate to the admin site (http://localhost:8000/admin/) and create a blog post.

First click the "Add" link next to *Posts* in the admin site.

(TODO Insert screenshot of admin homepage)

Next fill in the details for our first blog post and click the *Save* button.

(TODO Insert screenshot of Post creation form)

Our post was created

(TODO Insert screenshot of Post change list)

Our first test: __unicode__ method
----------------------------------

In the admin change list our posts all have the unhelpful name *Post object*.  We can customize the way models are referenced by creating a ``__unicode__`` method on our model class.

Let's first create a test demonstrating the behavior we'd like to see.

All the tests for our app will live in the ``tests.py`` file.  Currently this file looks like this:

.. code-block:: python

    """
    This file demonstrates writing tests using the unittest module. These will pass
    when you run "manage.py test".

    Replace this with more appropriate tests for your application.
    """

    from django.test import TestCase


    class SimpleTest(TestCase):
        def test_basic_addition(self):
            """
            Tests that 1 + 1 always equals 2.
            """
            self.assertEqual(1 + 1, 2)

Delete everything in that file and start over with a failing test:

.. code-block:: python

    from django.test import TestCase


    class PostModelTest(TestCase):

        def test_unicode_representation(self):
            self.fail("TODO Test incomplete")

Now run the test command to ensure our app's single test fails as expected:

.. code-block:: bash

    $ python manage.py test blog
    Creating test database for alias 'default'...
    F
    ======================================================================
    FAIL: test_unicode_representation (blog.tests.PostModelTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
    File "/home/zoidberg/learning-django-by-testing/myblog/blog/tests.py", line 7, in test_unicode_representation
        self.fail("TODO Test incomplete")
    AssertionError: TODO Test incomplete

    ----------------------------------------------------------------------
    Ran 1 test in 0.001s

    FAILED (failures=1)
    Destroying test database for alias 'default'...

Great!  Now we're ready to create a real test.

Let's write our test to ensure that a blog post's unicode representation is equal to its title.  We need to modify our tests file like so:

.. code-block::

    from django.test import TestCase
    from .models import Post


    class PostModelTest(TestCase):

        def test_unicode_representation(self):
            post = Post(title="My post title")
            self.assertEqual(unicode(post), "My post title")


Now let's run our tests again:

.. code-block:: bash

    $ python manage.py test blog
    Creating test database for alias 'default'...
    F
    ======================================================================
    FAIL: test_unicode_representation (blog.tests.PostModelTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
    File "/home/trey/repos/meetups/learning-django-by-testing/myblog/blog/tests.py", line 9, in test_unicode_representation
        self.assertEqual(unicode(post), "My post title")
    AssertionError: u'Post object' != 'My post title'

    ----------------------------------------------------------------------
    Ran 1 test in 0.001s

    FAILED (failures=1)
    Destroying test database for alias 'default'...

Our test fails again, but this time it fails because we haven't customized our ``__unicode__`` method yet so the unicode representation for our model is still the default *Post object*.

Let's add a ``__unicode__`` method to our model that returns the post title.  Our ``models.py`` file should look something like this:

.. code-block:: python

    from django.db import models


    class Post(models.Model):
        title = models.CharField(max_length=500)
        author = models.ForeignKey('auth.User')
        body = models.TextField()
        created_at = models.DateTimeField(auto_now_add=True, editable=False)
        modified_at = models.DateTimeField(auto_now=True, editable=False)

        def __unicode__(self):
            return self.title

Now if we run our test again we should see that our single test passes:

.. code-block:: bash

    $ python manage.py test blog
    Creating test database for alias 'default'...
    .
    ----------------------------------------------------------------------
    Ran 1 test in 0.001s

    OK
    Destroying test database for alias 'default'...

We've just written our first test and fixed our code to make our test pass.

(TODO Explain why we wrote the test first)
