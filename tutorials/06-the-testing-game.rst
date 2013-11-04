The Testing Game
================

TODO: Code coverage and stuff

.. code-block:: bash

    $ pip install coverage
    $ coverage run --include='./*' --branch manage.py test blog
    $ coverage report
    Name              Stmts   Miss Branch BrMiss  Cover
    ---------------------------------------------------
    blog/__init__         0      0      0      0   100%
    blog/admin            4      0      0      0   100%
    blog/forms           14      0      0      0   100%
    blog/models          21      0      0      0   100%
    blog/tests           87      0      0      0   100%
    blog/urls             2      0      0      0   100%
    blog/views           22      0      0      0   100%
    manage                6      0      2      1    88%
    myblog/__init__       0      0      0      0   100%
    myblog/settings      29      0      0      0   100%
    myblog/urls           5      0      0      0   100%
    myblog/views          6      0      0      0   100%
    ---------------------------------------------------
    TOTAL               196      0      2      1    99%


Adding Gravatars
----------------

Wouldn't it be cool if we could show user avatars next to comments?  Let's use the free `Gravatar`_ for this.  As usual, we'll start with a test.

According to the `Gravatar documentation`_ a Gravatar profile image can be requested like this:

    http://www.gravatar.com/avatar/HASH

Where ``HASH`` is an MD5 hash of the user's email address.  We can use the `hashlib`_ package in the Python standard library to generate the MD5 hash.

How do we want to generate the hashes?  One idea is adding a method of the ``Comment`` model that returns a Gravatar URL for the given email.  This could be used in our templates like so:

.. code-block:: html

    <img src="{{ comment.gravatar_url }}">

But why not also allow Gravatars do be shown for blog entries?  After all blog entries have an author who probably has an email address.  Retrieving the Gravatar URL for a blog post could look like this:

.. code-block:: html

    <img src="{{ entry.gravatar_url }}">

Instead of adding a ``gravatar_url`` method to the ``Entry`` and ``Comment`` models, why not add a template filter that will generate a Gravatar URL for any email address?  Here are two examples of how this might be used:

.. code-block:: html

    {% load gravatar_url from gravatar %}

    <img src="{{ comment.email|gravatar_url }}">
    <img src="{{ entry.author.email|gravatar_url }}">

TODO: Add tests for gravatar image URLs for comments

.. _gravatar: http://gravatar.com/
.. _gravatar documentation: http://en.gravatar.com/site/implement/images/
.. _hashlib: http://docs.python.org/2/library/hashlib.html
