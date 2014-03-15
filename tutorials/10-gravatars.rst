Adding Gravatars
================

Wouldn't it be cool if we could show user avatars next to comments?  Let's use the free `Gravatar`_ service for this.  As usual, we'll start with a test.

According to the `Gravatar documentation`_ a Gravatar profile image can be requested like this:

    http://www.gravatar.com/avatar/HASH

Where ``HASH`` is an MD5 hash of the user's email address.  We can use the `hashlib`_ package in the Python standard library to generate an MD5 hash.

Brainstorming a Solution
------------------------

But where do we want to generate the hashes?

We could add a method on our ``Comment`` model that returns a Gravatar URL based on the commenter's email address.  This could be used in our templates like so:

.. code-block:: html

    <img src="{{ comment.gravatar_url }}">

But why not also allow Gravatars to be shown for blog entries?  After all blog entries have an author who probably has an email address.  Retrieving the Gravatar URL for a blog post could look like this:

.. code-block:: html

    <img src="{{ entry.gravatar_url }}">

Instead of adding a ``gravatar_url`` method to the ``Entry`` and ``Comment`` models, we could add a template filter that will generate a Gravatar URL for any email address.  Here are two examples of how this might be used:

.. code-block:: html

    {% load gravatar_url from gravatar %}

    <img src="{{ comment.email|gravatar_url }}">
    <img src="{{ entry.author.email|gravatar_url }}">

TODO: Add tests for gravatar image URLs for comments


.. _gravatar: http://gravatar.com/
.. _gravatar documentation: http://en.gravatar.com/site/implement/images/
.. _hashlib: http://docs.python.org/2/library/hashlib.html
