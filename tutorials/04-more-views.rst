More Views
==========

Blogs should be interactive.  Let's allow visitors to comment on each entry.

Adding a Comment model
----------------------

First we need to add a ``Comment`` model in ``blog/models.py``.

.. code-block:: python

    class Comment(models.Model):
        entry = models.ForeignKey(Entry)
        name = models.CharField(max_length=100)
        email = models.EmailField()
        body = models.TextField()
        created_at = models.DateTimeField(auto_now_add=True, editable=False)
        modified_at = models.DateTimeField(auto_now=True, editable=False)


Since we have added a new model, we also need to make sure that this model
gets synced to our SQLite database.

.. code-block:: bash

    $ python manage.py makemigrations
    Migrations for 'blog':
      0002_auto_20141019_0232.py:
        - Create model Comment
        - Change Meta options on entry
    $ python manage.py migrate
    Operations to perform:
      Apply all migrations: contenttypes, blog, admin, auth, sessions
    Running migrations:
      Applying blog.0002_auto_20141019_0232... OK


Before we create a ``__str__`` method for our ``Comment`` model
similar to the one we previously added for our ``Entry`` model, let's create a test in ``blog/tests.py``.

Our test should look very similar to the ``__str__`` test we wrote in
``EntryModelTest`` earlier. This should suffice:

.. code-block:: python

    class CommentModelTest(TestCase):

        def test_string_representation(self):
            comment = Comment(body="My comment body")
            self.assertEqual(str(comment), "My comment body")

Don't forget to import our ``Comment`` model:

.. code-block:: python

    from .models import Entry, Comment


Now let's run our tests to make sure our new test fails:

.. code-block:: bash

    $ python manage.py test blog

::

    Creating test database for alias 'default'...
    F..........
    ======================================================================
    FAIL: test_string_representation (blog.tests.CommentModelTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      ...
    AssertionError: 'Comment object' != 'My comment body'
    - Comment object
    + My comment body


    ----------------------------------------------------------------------
    Ran 11 tests in 0.154s

    FAILED (failures=1)
    Destroying test database for alias 'default'...


Great. So it looks like our test fails. Now we should implement the ``__str__`` method for the comment body,
an exercise we leave to the reader. After implementing the method, run the test again to see it pass:

.. code-block:: bash

    $ python manage.py test blog

::

    Creating test database for alias 'default'...
    ...........
    ----------------------------------------------------------------------
    Ran 11 tests in 0.085s

    OK
    Destroying test database for alias 'default'...


Adding comments on the admin site
----------------------------------

Let's add the Comment model to the admin just like we did with the Entry
model. This involves editing ``blog/admin.py`` to look like this:

.. code-block:: python

    from django.contrib import admin

    from .models import Entry, Comment


    admin.site.register(Entry)
    admin.site.register(Comment)

If you start the development server again, you will see the Comment model
in the admin and you can add comments to the blog entries. However, the point
of a blog is to let other users and not only the admin post comments.


Displaying comments on the website
----------------------------------

Now we can create comments in the admin interface, but we can't see them on the website yet.  Let's display comments on the detail page for each blog entry.

After the ``<hr>`` element inside of our content block in ``templates/blog/entry_detail.html`` let's add the following:

.. code-block:: html

    <hr>
    <h4>Comments</h4>
    {% for comment in entry.comment_set.all %}
        <p><em>Posted by {{ comment.name }}</em></p>
        {{ comment|linebreaks }}
    {% empty %}
        No comments yet.
    {% endfor %}

.. IMPORTANT::

    We forgot to add tests for this!  Why don't you add a test to make sure
    comments appear on the blog entry page and a test to make sure the "No
    comments yet" message shows up appropriately.  These tests should probably be
    added to our ``EntryViewTest`` class.

Now we can see our comments on the website.
