Custom template tags
====================

Let's make our blog list recent entries in the sidebar.

How are we going to do this?  We could loop through blog entries in our
``base.html`` template, but that means we would need to include a list of our
recent blog entries in the template context for all of our views.  That could
result in duplicate code and we don't like duplicate code.

.. TIP::

    If you didn't fully understand the last paragraph, that's okay. `DRY`_ or
    "Don't Repeat Yourself" is a rule of thumb for good programming practice.
    You might want to read through the Django `template documentation`_ again
    later.

To avoid duplicate code, let's create a `custom template tag`_ to help us
display recent blog entries in the sidebar on every page.

.. NOTE::
  A custom template tag that itself fires a SQL query enables our HTML
  templates to add more SQL queries to our view. That hides some behavior. It's
  too early at this point, but that query should be cached if we expect to use
  this often.


Where
-----

Let's create a template library called ``blog_tags``.  Why ``blog_tags``?
Because naming our tag library after our app will make our template imports
more understandable. We can use this template library in our templates by
writing ``{% load blog_tags %}`` near the top of our template file.

Create a ``templatetags`` directory in our ``blog`` app and create two empty
Python files within this directory: ``blog_tags.py`` (which will hold our
template library code) and ``__init__.py`` (to make this directory into a Python
package).

We should now have something like this::

    blog
    ├── admin.py
    ├── forms.py
    ├── __init__.py
    ├── migrations
    │   ├── 0001_initial.py
    │   ├── 0002_auto_20141019_0232.py
    │   └── __init__.py
    ├── models.py
    ├── templatetags
    │   ├── blog_tags.py
    │   └── __init__.py
    ├── tests.py
    ├── urls.py
    └── views.py


Creating an inclusion tag
-------------------------

Let's create an `inclusion tag`_ to query for recent blog entries and render a list
of them.  We'll name our template tag ``entry_history``.

Let's start by rendering an empty template with an empty template context
dictionary. First let's create a ``templates/blog/_entry_history.html``
file with some dummy text:

.. code-block:: html

    <p>Dummy text.</p>

Now we'll create our ``blog/templatetags/blog_tags.py`` module with our ``entry_history`` template tag:

.. code-block:: python

    from django import template

    register = template.Library()


    @register.inclusion_tag('blog/_entry_history.html')
    def entry_history():
        return {}

Let's use our tag in our base template file. In our ``base.html`` file, import our new template library by adding the line
``{% load blog_tags %}`` near the top of the file.

Then modify our second column to use our ``entry_history`` template tag:

.. code-block:: html

    <div class="large-4 columns">
        <h3>About Me</h3>
        <p>I am a Python developer and I like Django.</p>
        <h3>Recent Entries</h3>
        {% entry_history %}
    </div>

Restart the server and make sure our dummy text appears.


Make it work
------------

We just wrote code without writing any tests.  Let's write some tests now.

At the top of ``blog/tests.py`` we need to add
``from django.template import Template, Context``. We need those
imports because we will be manually rendering template strings to test
our template tag.

Now let's add a basic test to our ``blog/tests.py`` file:

.. code-block:: python

    class EntryHistoryTagTest(TestCase):

        TEMPLATE = Template("{% load blog_tags %} {% entry_history %}")

        def setUp(self):
            self.user = get_user_model().objects.create(username='zoidberg')

        def test_entry_shows_up(self):
            entry = Entry.objects.create(author=user, title="My entry title")
            rendered = self.TEMPLATE.render(Context({}))
            self.assertIn(entry.title, rendered)


The tricky bits here are ``TEMPLATE``, ``Context({})`` and that ``render()`` call. These should all look somewhat familiar
from the `django tutorial part 3`_. ``Context({})`` in this case just passes no data to a ``Template`` that we're
rendering directly in memory. That last assert just checks that the title of the entry is in the text.

As expected, our test fails because we are not actually displaying any entries with our ``entry_history`` template tag:

.. code-block:: bash

    $ python manage.py test blog
    Creating test database for alias 'default'...
    .....F...............
    ======================================================================
    FAIL: test_entry_shows_up (blog.tests.EntryHistoryTagTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      ...
    AssertionError: 'My entry title' not found in ' <p>Dummy text.</p>'

    ----------------------------------------------------------------------
    Ran 21 tests in 0.132s

    FAILED (failures=1)
    Destroying test database for alias 'default'...

Let's make our template tag actually display entry history. First we
will import our ``Entry`` model at the top of our template tag library
module:

.. code-block:: python

    from ..models import Entry

.. NOTE::

    For more information on the ``..`` syntax for imports see the Python documentation on `relative imports`_.

Now let's send the last 5 entries in our sidebar:

.. code-block:: python

    def entry_history():
        entries = Entry.objects.all()[:5]
        return {'entries': entries}

Now we need to update our ``_entry_history.html`` file to display the
titles of these blog entries:

.. code-block:: html

    <ul>
        {% for entry in entries %}
            <li>{{ entry.title }}</li>
        {% endfor %}
    </ul>

Let's run our tests again and make sure they all pass.

Making it a bit more robust
---------------------------

What happens if we don't have any blog entries yet? The sidebar might
look a little strange without some text indicating that there aren't
any blog entries yet.

Let's add a test for when there are no blog posts:

.. code-block:: python

    def test_no_posts(self):
        rendered = self.TEMPLATE.render(Context({}))
        self.assertIn("No recent entries", rendered)

The above test is for an edge case. Let's add a test for another edge
case: when there are more than 5 recent blog entries.  When there are 6
posts, only the last 5 should be displayed.  Let's add a test for this
case also:

.. code-block:: python

    def test_many_posts(self):
        for n in range(6):
            Entry.objects.create(author=self.user, title="Post #{0}".format(n))
        rendered = self.TEMPLATE.render(Context({}))
        self.assertIn("Post #5", rendered)
        self.assertNotIn("Post #6", rendered)

The ``{% for %}`` template tag allows us to define an ``{% empty %}``
tag which we will be displayed when there are no blog entries (see
`for loops`_ documentation).

Update the ``_entry_history.html`` template to utilize the
``{% empty %}`` tag and make sure the tests pass.

.. code-block:: html

    <ul>
        {% for entry in entries %}
            <li>{{ entry.title }}</li>
        {% empty %}
            <li>No recent entries</li>
        {% endfor %}
    </ul>

It looks like we still have some problems because our tests still fail:

.. code-block:: bash

    $ python manage.py test blog
    Creating test database for alias 'default'...
    .....EE................
    ======================================================================
    ERROR: test_entry_shows_up (blog.tests.EntryHistoryTagTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      ...
    AttributeError: 'EntryHistoryTagTest' object has no attribute 'entry'

    ======================================================================
    ERROR: test_many_posts (blog.tests.EntryHistoryTagTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      ...
    AttributeError: 'EntryHistoryTagTest' object has no attribute 'user'

    ----------------------------------------------------------------------
    Ran 23 tests in 0.164s

    FAILED (errors=2)
    Destroying test database for alias 'default'...

Try to fix the bugs on your own but don't be afraid to ask for help.

.. HINT::

    There are multiple bugs in our test code. Let's give you a couple of hints on how you can approach debugging and resolving them.

    First of all, for the ``test_no_posts``, think about what is initially being set up in the function ``setUp``. How many entries have been created? What could we do to have no entries created when ``test_no_posts`` is called and executed?

    Secondly, for ``test_many_posts``, read about `slicing`_ and the `range`_ function to resolve the errors that appear during testing.

    .. _range: https://docs.python.org/2/library/functions.html?highlight=slice#range
    .. _slicing: https://docs.python.org/2/library/functions.html?highlight=slice#slice


.. _custom template tag: https://docs.djangoproject.com/en/dev/howto/custom-template-tags/#writing-custom-template-tags
.. _dry: http://programmer.97things.oreilly.com/wiki/index.php/Don%27t_Repeat_Yourself
.. _for loops: https://docs.djangoproject.com/en/dev/ref/templates/builtins/#for-empty
.. _template documentation: https://docs.djangoproject.com/en/1.6/ref/templates/api/
.. _inclusion tag: https://docs.djangoproject.com/en/1.6/howto/custom-template-tags/#howto-custom-template-tags-inclusion-tags
.. _django tutorial part 3: https://docs.djangoproject.com/en/1.6/intro/tutorial03/#write-views-that-actually-do-something
.. _relative imports: http://docs.python.org/2/tutorial/modules.html#intra-package-references
