Models
======

First let's create a blog post

.. code-block:: python

    from django.db import models


    class Post(models.Model):
        title = models.CharField(max_length=500)
        author = models.Foreignkey('auth.User')
        body = models.TextField()
        created_at = models.DateTimeField(auto_now_add=True, editable=False)
        modified_at = models.DateTimeField(auto_now=True, editable=False)


.. code-block:: python

    from django.contrib import admin
    from .models import Post


    admin.site.register(Post)


TODO Insert screenshot of blog changelist in admin

TODO Add model test for __unicode__ method and then add __unicode__ method
