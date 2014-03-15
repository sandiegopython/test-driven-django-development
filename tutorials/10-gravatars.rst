Adding Gravatars
================

Wouldn't it be cool if we could show user avatars next to comments?  Let's use the free `Gravatar`_ service for this.  As usual, we'll start with a test.

According to the `Gravatar documentation`_ a Gravatar profile image can be requested like this:

    https://www.gravatar.com/avatar/HASH

Where ``HASH`` is an MD5 hash of the user's email address.  We can use the `hashlib`_ package in the Python standard library to generate an MD5 hash.

.. TIP::

    There are lots of options for displaying gravatars such as setting the display size for the image and having a default image if there is no Gravatar for a specific email.

First, let's write a test for Gravatars. This test will be added to our already existing test ``CommentModelTest`` since the plan is to add a method to the ``Comment`` model to get the Gravatar URL.

.. code-block:: python

    def test_gravatar_url(self):
        comment = Comment(body="My comment body", email="email@example.com")
        expected = "https://www.gravatar.com/avatar/5658ffccee7f0ebfda2b226238b1eb6e"
        self.assertEqual(comment.gravatar_url(), expected)

When running our tests now, we'll see an error since we have not yet written a ``gravatar_url()`` method to the ``Comment`` model:

.. code-block:: bash

    $ python manage.py test
    Creating test database for alias 'default'...
    ....E...................
    ======================================================================
    ERROR: test_gravatar_url (blog.tests.CommentModelTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
    ...
    AttributeError: 'Comment' object has no attribute 'gravatar_url'

    ----------------------------------------------------------------------
    Ran 24 tests in 0.155s

    FAILED (errors=1)
    Destroying test database for alias 'default'...


Adding comment gravatars
------------------------

Let's add ``gravatar_url()`` method to ``Comment`` so that our tests can pass. This involves editing ``models.py``:

.. code-block:: python

    def gravatar_url(self):
        # Get the md5 hash of the email address
        md5 = hashlib.new('md5')
        md5.update(unicode(self.email))
        digest = md5.hexdigest()

        url = 'https://www.gravatar.com/avatar/{}'.format(digest)
        return url

.. TIP::

    If you've never used ``hashlib`` before, this may look a little daunting. Md5_ is a cryptographic hash function that takes a string of any size and creates a 128 bit binary string. When rendered as hexidecimal, it is a 32 character string.

    .. Technically we will get a UnicodeDecodeError if the email contains non-ascii characters but Django's EmailValidator doesn't support that anyway.

    ``self.email`` is always converted to unicode because it is possible that it is ``None`` since it is not required. If you're feeling up to it, write a test for this case and see what happens.

If you run the tests at this point, you should see that our test case passes.


Displaying gravatars on the site
--------------------------------

Now, let's display the Gravatars with the comments.

In our ``content`` block in ``templates/blog/entry_detail.html``, let's add the Gravatar images:

.. code-block:: html

    {% for comment in entry.comment_set.all %}
        <p>
            <em>Posted by {{ comment.name }}</em>
            <img src="{{ comment.gravatar_url }}" align="left">
        </p>
        {{ comment|linebreaks }}
    {% empty %}
        No comments yet.
    {% endfor %}

If you fire up the development web server and look at a specific blog entry, you should see an image for each comment.


.. _gravatar: http://gravatar.com/
.. _gravatar documentation: http://en.gravatar.com/site/implement/images/
.. _hashlib: http://docs.python.org/2/library/hashlib.html
.. _md5: http://en.wikipedia.org/wiki/Md5
