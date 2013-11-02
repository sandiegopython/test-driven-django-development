Workshop: Test-Driven Web Development with Django
=================================================

Thank you for attending `San Diego Python <http://pythonsd.org/>`_'s workshop on test-driven
development with the `Django <https://www.djangoproject.com/>`_ web framework. In this one-day
workshop, you will learn to build a well-tested, Django-based website.

This workshop was made possible by a grant from the `Python Software Foundation <http://python.org/psf/>`_
`Outreach and Education Committee <http://python.org/psf/committees/#outreach-education-committee-orec>`_.


Why test-driven development?
----------------------------

When creating a new application, at first you may not need tests.  Tests can
be difficult to write at first and they take time, but they can save an
enormous amount of manual troubleshooting time.

As your application grows, it becomes more difficult to grow and to refactor
your code.  There's always the risk that a change in one part of your
application will break another part. A good collection of automated tests that
go along with an application can verify that changes you make to one part of
the software do not break another.


Prerequisites
-------------

* `Python <http://www.python.org/download/>`_ 2.6 or 2.7 (2.7 is recommended)
* `Install Django <https://docs.djangoproject.com/en/1.5/intro/install/>`_
  1.5
* The `Django tutorials <https://docs.djangoproject.com/en/1.5/intro/tutorial01/>`_

You do not need to be a Django expert to attend this workshop or to find this
document useful. However, the goal of getting a working website with tests in
a single day is a lofty one and so we ask that attendees come with Python
and Django installed. We also encourage people to go through the Django
tutorials beforehand in order to get the most out of the workshop.


The Project: building a blog
----------------------------

The right of passage for most web developers is their own blog system. There
are hundreds of solutions out there.  The features and requirements are
generally well understood. Writing one with TDD becomes a kind of `code kata
<http://codekata.pragprog.com/>`_ that can help you work through all kinds of
aspects of the Django framework.


Contents
--------

.. toctree::
   :maxdepth: 2

   01-getting-started
   02-models
   03-views
   04-more-views
   05-forms
