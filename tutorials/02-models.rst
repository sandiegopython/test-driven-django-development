Models
======

(TODO Explain what models are and why we're using them)

First let's create a blog post

.. code-block:: python

    from django.db import models


    class Post(models.Model):
        title = models.CharField(max_length=500)
        author = models.Foreignkey('auth.User')
        body = models.TextField()
        created_at = models.DateTimeField(auto_now_add=True, editable=False)
        modified_at = models.DateTimeField(auto_now=True, editable=False)


Creating posts from the admin site
----------------------------------

We don't want to manually add posts to the database every time we want to update our blog.  It would be nice if we could use a login-secured webpage to create blog posts.  Fortunately Django's admin interface can do just that.

In order to create blog posts from the admin interface we need to register our Post model with the admin site.  We can do this by creating an ``admin.py`` file in our ``blog`` app with the following code:


.. code-block:: python

    from django.contrib import admin
    from .models import Post


    admin.site.register(Post)

Now we can navigate to the admin site (http://localhost:8000/admin/) and create a blog post:

(TODO Insert screenshot of blog changelist in admin)


Fixing post names in the admin
------------------------------

TODO Add model test for __unicode__ method and then add __unicode__ method
