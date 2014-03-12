Custom template context processors
==================================

Let's make our blog list recent entries in the sidebar.

How are we going to do this?  We can loop through blog entries in our
``base.html`` template, but that means we would need to include a list of our
recent blog entries in the template context for all of our views.  If
we were to update the context in each view, that would result in
duplicate code, and we don't like duplicate code.

.. TIP::

    If you didn't fully understand the last paragraph, that's okay.  You might
    want to read through the Django `template documentation`_ again later.

To avoid duplicate code, let's create a `context processor`_ to help us
add recent blog posts to the context of each view.

.. NOTE::
  Context processors add context to *every* view. Usually they are not
  the right answer, but we are building a blog and will usually need
  these posts available. The extra context may also introduce extra
  database queries on each page.


Where
-----

Template context processors can live anywhere in your code. They are
simple functions that accept a request object as their only parameter,
and return dictionary-like objects that are added to the context. We
will put ours in a shiny new ``context_processors`` module.

Create a ``context_processors.py`` python file in our ``blog`` app.

We should now have something like this::

    ├── blog
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── context_processors.py
    │   ├── forms.py
    │   ├── models.py
    │   ├── tests.py
    │   ├── urls.py
    │   └── views.py


Creating a context processor
----------------------------

Now we'll write our ``blog/templatetags/context_processors.py`` module
with our ``prev_posts`` context processor:

.. code-block:: python

    from . import models


    def prev_posts(request):
        return {'prev_posts': models.Post.objects.all()[:20]}


.. NOTE::
  It is always good to have sane limits, especially when dealing with
  querysets. You will see later it is easy enough to limit the number
  of posts in the template, but adding ``[:20]`` gives us the insurance
  that this feature at maximum will only slow us down enough to grab 20
  previous blog posts.


Updating the site settings
--------------------------

Just writing the context processor isn't enough, we need to add it to
the list of context processors our site uses to populate the context of
each template render.

By default Django is already using a defined tuple of context
preprocessors defined as ``TEMPLATE_CONTEXT_PROCESSORS`` in the site
settings. All we need to do is add our context preprocessor to that
list. Add the following lines to your ``myblog/settings.py settings``
file.

.. code-block:: python

    from django.conf import global_settings


    TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
        "blog.context_processors.prev_posts",
    )

Let's use our new context variable in our base template file. In our
``base.html`` file, add the following template markup to add a list of
post titles in the sidebar.

.. code-block:: html

    <div class="large-4 columns">
        <h3>About Me</h3>
        <p>I am a Python developer and I like Django.</p>
        <h3>Previous Posts</h3>
        <ul>
        {% for entry in prev_posts|slice:":5" %}
            <li>{{ entry.title }}</li>
        {% endfor %}
        </ul>
    </div>

Reload the homepage and make sure our dummy text appears.

.. NOTE::
  ``slice`` is a builtin `template filter`_ included with Django that
  allows us to slice iterable variables in the template markup.

Make it work
------------

We just wrote code without writing any tests.  Let's write some tests now.

At the top of ``blog/test.py`` we need to add ``from django.template import Template, Context``.  We need those imports because we will be manually rendering template strings to test our template tag.

Now let's add a basic test to our ``blog/tests.py`` file:

.. code-block:: python

    class PreviousEntryTagTest(TestCase):
        TEMPLATE = Template("{% load blog_tags %} {% entry_history %}")

        def setUp(self):
            user = get_user_model().objects.create(username='zoidberg')
            Entry.objects.create(self.author=user, title="My entry title")

        def test_entry_shows_up(self):
            rendered = self.TEMPLATE.render(Context({}))
            self.assertContains(rendered, self.entry.title)


The tricky bits here are ``TEMPLATE``, ``Context({})`` and that ``render()`` call. These should all look somewhat familiar
from the `django tutorial part 3`_. ``Context({})`` in this case just passes no data to a ``Template`` that we're
rendering directly in memory. That last assert just checks that the title of the entry is in the text.

Run the tests and we get

::

    Creating test database for alias 'default'...
    ................F.
    ======================================================================
    FAIL: test_entry_shows_up (blog.tests.PreviousEntryTagTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      ...
    AssertionError

    ----------------------------------------------------------------------
    Ran 18 tests in 0.109s

    FAILED (failures=1)
    Destroying test database for alias 'default'...

As expected, our test fails because we are not actually displaying any entries with our ``entry_history`` template tag.

Let's make our template tag actually display entry history.  First we will import our ``Entry`` model at the top of our template tag library module:

.. code-block:: python

    from ..models import Entry

TODO: Add aside explaining ``..`` syntax

Now let's send the last 5 entries in our sidebar:

.. code-block:: python

    def entry_history():
        entries = Entry.objects.all()[:5]
        return {'entries': entries}

Now we need to update our ``_entry_history.html`` file to display the titles of these blog entries:

.. code-block:: html

    <ul>
    {% for entry in entries %}
      <li>{{ entry.title }}</li>
    {% endfor %}
    </ul>

Let's run our tests again and make sure they all pass.

Making it a bit more robust
---------------------------

What happens if we don't have any blog entries yet?  The sidebar might look a little strange without some text indicating that there aren't any blog entries yet.

Let's add a test for when there are no blog posts:

.. code-block:: python

    def test_no_posts(self):
        rendered = self.TEMPLATE.render(Context({}))
        self.assertContains(rendered, "No recent entries")

The above test is for an edge case.  Let's add a test for another edge case: when there are more than 5 recent blog entries.  When there are 6 posts, only the last 5 should be displayed.  Let's add a test for this case also:

.. code-block:: python

    def test_many_posts(self):
        for n in range(6):
            Entry.objects.create(author=self.user, title="Post #{0}".format(n))
        rendered = self.TEMPLATE.render(Context({}))
        self.assertContains(rendered, "Post #5")
        self.assertNotContains(rendered, "Post #6")

TODO: Run tests and show that 1 fails

The ``{% for %}`` template tag allows us to define an ``{% empty %}`` tag which we will be displayed when there are no blog entries (see `for loops`_ documentation).

Update the ``_entry_history.html`` template to utilize the ``{% empty %}`` tag and make sure the tests pass.

.. code-block:: python


    def setUp(self):
        self.user = get_user_model().objects.create(username='zoidberg')
        self.entry = Entry.objects.create(author=self.user, title="My entry title")

It looks like we still have a problem because our tests still fail now.  Try to fix the bug on your own and don't be afraid to ask for help.


.. _context processor: https://docs.djangoproject.com/en/1.6/ref/templates/api/#writing-your-own-context-processors
.. _template filter: https://docs.djangoproject.com/en/1.6/ref/templates/builtins/#built-in-filter-reference
.. _for loops: https://docs.djangoproject.com/en/dev/ref/templates/builtins/#for-empty
.. _template documentation: https://docs.djangoproject.com/en/1.6/ref/templates/api/
.. _inclusion tag: https://docs.djangoproject.com/en/1.6/howto/custom-template-tags/#howto-custom-template-tags-inclusion-tags
.. _django tutorial part 3: https://docs.djangoproject.com/en/1.6/intro/tutorial03/#write-views-that-actually-do-something
