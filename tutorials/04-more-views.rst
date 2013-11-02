More Views
==========

Blogs should be interactive.  Let's allow visitors to comment on each post.

Adding a Comment model
----------------------

First we need to add a ``Comment`` model in ``blog/models.py``.

.. code-block:: python

    class Comment(models.Model):
        post = models.ForeignKey(Post)
        name = models.CharField(max_length=100)
        email = models.EmailField()
        body = models.TextField()
        created_at = models.DateTimeField(auto_now_add=True, editable=False)
        modified_at = models.DateTimeField(auto_now=True, editable=False)


Let's write a ``__unicode___`` method for our ``Comment`` model like we did for our ``Post`` model earlier.

First we should create a test in ``blog/tests.py``.  Our test should look very similar to the ``__unicode__`` test we wrote for posts earlier.  This should suffice:

.. code-block:: python

    class CommentModelTest(TestCase):

        def test_unicode_representation(self):
            comment = Comment(body="My comment body")
            self.assertEqual(unicode(comment), "My comment body")

Don't forget to import our ``Comment`` model:

.. code-block:: python

    from .models import Post, Comment


Now let's run our tests to make sure our new test fails:

.. code-block:: bash

    $ python manage.py test blog

::

    Creating test database for alias 'default'...
    F.
    ======================================================================
    FAIL: test_unicode_representation (blog.tests.CommentModelTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
    ...
    AssertionError: u'Comment object' != 'My comment body'

    ----------------------------------------------------------------------
    Ran 10 tests in 0.077s

    FAILED (failures=1)
    Destroying test database for alias 'default'...

Great.  After we implement our ``__unicode__`` method our tests should pass:

.. code-block:: bash

    $ python manage.py test blog

::

    Creating test database for alias 'default'...
    ..........
    ----------------------------------------------------------------------
    Ran 10 tests in 0.072s

    OK
    Destroying test database for alias 'default'...

Since we have added a new model, we also need to make sure that this model
gets synched to our SQLite database.

.. code-block:: bash

    $ python manage.py syncdb


Adding comments on the admin site
----------------------------------

Let's add the Comment model to the admin just like we did with the Post
model. This involves editing ``blog/admin.py`` to look like this:

.. code-block:: python

    from django.contrib import admin
    from .models import Post, Comment


    admin.site.register(Post)
    admin.site.register(Comment)

If you start the development server again, you will see the Comment model
in the admin and you can add comments to the blog posts. However, the point
of a blog is to let other users and not only the admin post comments.


Displaying comments on the website
----------------------------------

Now we can create comments in the admin interface, but we can't see them on the website yet.  Let's display comments on the detail page for each blog post.

At the end of our ``content`` block in ``templates/post_detail.html`` let's add the following:

.. code-block:: html

    <hr>
    <h4>Comments</h4>
    {% for comment in post.comment_set.all %}
        <p><em>Posted by {{ comment.name }}</em></p>
        {{ comment|linebreaks }}
    {% empty %}
        No comments yet.
    {% endfor %}

.. IMPORTANT::

    We forgot to add a test for this!  Why don't you add a test to make sure comments appear on the blog post page.

Now we can see our comments on the website.
