Forms
=====

Blogs should be interactive.  Let's allow visitors to comment on each post.

Adding a Comment model
----------------------

First we need to add a ``Comment`` model.

.. code-block:: python

    class Comment(models.Model):
        post = models.ForeignKey(Post)
        name = models.CharField(max_length=100)
        email = models.EmailField()
        body = models.TextField()
        created_at = models.DateTimeField(auto_now_add=True, editable=False)
        modified_at = models.DateTimeField(auto_now=True, editable=False)


Let's write a ``__unicode___`` method for our ``Comment`` model like we did for our ``Post`` model earlier.

First we should create a test.  Our test should look very similar to the ``__unicode__`` test we wrote for posts earlier.  This should suffice:

.. code-block:: python

    class CommentModelTest(TestCase):

        def test_unicode_representation(self):
            comment = Comment(body="My comment body")
            self.assertEqual(unicode(comment), "My comment body")


Now let's run our tests to make sure our new test fails:

.. code-block:: bash

    $ python manage.py test blog
    Creating test database for alias 'default'...
    F.
    ======================================================================
    FAIL: test_unicode_representation (blog.tests.CommentModelTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
    File "/home/zoidberg/learning-django-by-testing/myblog/blog/tests.py", line 16, in test_unicode_representation
    self.assertEqual(unicode(comment), "My comment body")
    AssertionError: u'Comment object' != 'My comment body'

    ----------------------------------------------------------------------
    Ran 2 tests in 0.001s

    FAILED (failures=1)
    Destroying test database for alias 'default'...

Great.  After we implement our ``__unicode__`` method our tests should pass:

.. code-block:: bash

    $ python manage.py test blog
    Creating test database for alias 'default'...
    ..
    ----------------------------------------------------------------------
    Ran 2 tests in 0.001s

    OK
    Destroying test database for alias 'default'...
