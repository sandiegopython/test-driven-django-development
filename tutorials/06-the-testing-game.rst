The Testing Game
================


Test Coverage
-------------

It's important to test all your code. Code coverage is frequently used as a measuring stick for quality tests. Code coverage allows you to make sure that every line of code is executed. The basic idea behind code coverage is that if your tests are comprehensive, all of your code should be executed. 

Using Coverage
--------------

Let's demonstrate this idea by using `Coverage`_, a tool that measures code coverage of Python programs. 

First let's install coverage:

.. code-block:: bash

    $ pip install coverage

Now let's run our tests. As we run our tests, coverage records and creates a coverage report:

.. code-block:: bash

    $ coverage run --include='./*' manage.py test blog
    Creating test database for alias 'default'...
    .................
    ----------------------------------------------------------------------
    Ran 17 tests in 0.234s

    OK
    Destroying test database for alias 'default'...

Let's take a look at our code coverage report:

.. code-block:: bash

    $ coverage report
    Name              Stmts   Miss  Cover
    -------------------------------------
    blog/__init__         0      0   100%
    blog/admin            4      0   100%
    blog/forms           14      0   100%
    blog/models          21      0   100%
    blog/tests           87      0   100%
    blog/urls             2      0   100%
    blog/views           22      0   100%
    manage                6      0   100%
    myblog/__init__       0      0   100%
    myblog/settings      29      0   100%
    myblog/urls           5      0   100%
    myblog/views          6      0   100%
    -------------------------------------
    TOTAL               196      0   100%


TODO: explain what this means.


HTML Coverage Report
--------------------

You can prettify the coverage report above into html format by running the following command:

.. code-block:: bash

    $ coverage html

This command will create a directory/file called ``htmlcov/index.html`` and save it in your current directory. You can then view this file in your web browser as below. Or if you prefer, take a `look at our report`_ on Github.

.. image:: _static/06-01_coverage_report.png

Branch Coverage
---------------

So far we've been testing "line coverage" to ensure we execute every line of code during our tests.  We can do better by ensuring every code branch is taken.

For example let's say we have a file called ``example.py``::

    a = 0
    if not a:
        a = 1

Let's execute this file with code coverage including branch coverage and then view the coverage report:

.. code-block:: bash

    $ coverage run --branch example.py
    $ coverage report
    Name    Stmts   Miss Branch BrMiss  Cover
    -----------------------------------------
    test        3      0      2      1    80%

The two new columns in our coverage report count the total number of branches and the number of missed branches.  In this case our code always executes the "if" branch and never skips it so we miss the negative branch in our if condition.

From now on we will add the ``--branch`` argument when we record code coverage.  Let's try it on our tests:

.. code-block:: bash

    $ coverage run --include='./*' manage.py test blog
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

Coverage Configuration
----------------------

TODO: Add a ``.coveragerc`` file with our defaults::

    [run]
    include = ./*
    branch = 1

HTML Coverage Report
--------------------

TODO: show how an HTML coverage report can be generated

Full coverage isn't enough
--------------------------

TODO: coverage can only indicate that you've forgotten tests; it doesn't tell you whether your tests are good

Adding Gravatars
----------------

TODO: Move this section to another file?

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

.. _coverage: http://nedbatchelder.com/code/coverage/
.. _look at our report: https://raw.github.com/pythonsd/test-driven-django-development/master/myblog/htmlcov/index.html
.. _gravatar: http://gravatar.com/
.. _gravatar documentation: http://en.gravatar.com/site/implement/images/
.. _hashlib: http://docs.python.org/2/library/hashlib.html
