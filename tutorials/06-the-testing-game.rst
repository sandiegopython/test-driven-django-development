The Testing Game
================


Test Coverage
-------------

It's important to test all your code. Code coverage is frequently used as a measuring stick for quality tests. Code coverage allows you to make sure that every line of code is executed. The basic idea behind code coverage is that if your tests are comprehensive, all of your code should be executed.

To measure our code coverage we will use `Coverage`_, a tool that measures code coverage for Python code.

Intalling Coverage
------------------

First let's install coverage:

.. code-block:: bash

    $ pip install coverage

Before we continue, we need to remember to add this new dependency to our ``requirements.txt`` file.  Let's use ``pip freeze`` to discover the version of ``coverage`` we installed:

.. code-block:: bash

    $ pip freeze
    Django==1.6.2
    WebOb==1.3.1
    WebTest==2.0.14
    argparse==1.2.1
    beautifulsoup4==4.3.2
    coverage==3.7.1
    django-webtest==1.7.6
    six==1.5.2
    waitress==0.8.8
    wsgiref==0.1.2

Now let's add ``coverage`` to our ``requirements.txt`` file::

    coverage==3.7.1
    Django==1.5.5
    django-webtest==1.7.5
    WebTest==2.0.9

Using Coverage
--------------

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

.. IMPORTANT::

    Note that code coverage can only indicate that you've forgotten tests; it will not tell you whether your tests are good.  Don't use good code coverage as an excuse to write less tests.


HTML Coverage Report
--------------------

Our current command-line coverage reports are useful, but they aren't very detailed.  Fortunately coverage includes a feature for generating HTML coverage reports that visually demonstrate coverage by coloring our code based on the results.

Let's can prettify the coverage report above into HTML format by running the following command:

.. code-block:: bash

    $ coverage html

This command will create a ``htmlcov`` directory containing our test coverage.  The ``index.html`` is the overview file which links to the other files.  Let's open up our ``htmlcov/index.html`` in our web browser.

Our HTML coverage report should look something like this:

.. image:: _static/06-01_coverage_report.png


Branch Coverage
---------------

So far we've been testing statement coverage to ensure we execute every line of code during our tests.  We can do better by ensuring every code branch is taken.  The coverage documentation contains a good description of `branch coverage`_.

From now on we will add the ``--branch`` argument when we record code coverage.  Let's try it on our tests:

.. code-block:: bash

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

Notice the new ``Branch`` and ``BrMiss`` columns and note that we are missing a branch in our ``manage.py`` file.  We'll take a look at that later.


Coverage Configuration
----------------------

Coverage allows us to specify a configuration file (``.coveragerc`` files) to specify default coverage attributes.  The documentation explains how `.coveragerc`_ work.

Let's add a ``.coveragerc`` file to our project that looks like this::

    [run]
    include = ./*
    branch = 1

Now we can run coverage without any extra arguments:

.. code-block::

    $ coverage run manage.py test blog


Inspecting Missing Coverage
---------------------------

Now let's figure out why our branch coverage is not 100%.  First we need to regenerate the HTML coverage report and have a look at it:

.. code-block::

    $ coverage html

.. image:: _static/06-02_branch_coverage_report.png

Let's click on ``manage`` to see why our manage.py file has 88% coverage:

.. image:: _static/06-03_missing_manage_coverage.png

We're missing the ``False`` case for that ``if`` statement in our ``manage.py`` file.  We always run ``manage.py`` from the command line so that code is always executed.

We don't intend to ever test that missing branch, so let's ignore the issue.

.. TIP::

    For extra credit, figure out how we can exclude that ``if __name__ == "__main__":`` line from our coverage count.  Check out the `.coveragerc`_ documentation for help.


.. _coverage: http://nedbatchelder.com/code/coverage/
.. _branch coverage: http://nedbatchelder.com/code/coverage/branch.html
.. _.coveragerc: http://nedbatchelder.com/code/coverage/config.html

