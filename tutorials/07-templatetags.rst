Custom template tags
====================

Let's make our blog list recent entries in the sidebar.

How are we going to do this?  We could loop through blog entries in our
``base.html`` template, but that means we would need to include a list of our
recent blog posts in the template context for all of our views.  That could
result in duplicate code and we don't like duplicate code.

.. TIP::

    If you didn't fully understand the last paragraph, that's okay.  You might
    want to read through the Django `template documentation`_ again later.

To avoid duplicate code, let's create a `custom template tag`_ to help us
display recent blog posts in the sidebar on every page.

.. NOTE::
  A custom template tag that itself fires a SQL query means that our HTML
  templates can add more SQL queries to our view. That hides some behavor It's too early at this point,
  but that query should be cached if we expect to use this often.


Where
-----

Create a ``templatetags`` directory in ``blog`` so we have something like this.

::

    ├── blog
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── forms.py
    │   ├── models.py
    │   ├── templatetags
    │   │   ├── __init__.py
    │   │   └── blog_tags.py
    │   ├── tests.py
    │   ├── urls.py
    │   └── views.py

#TODO: Need to also create the templates/blog/templatetags/entry_history.html, and probably move this section down

Why ``blog_tags.py``? Because in each template we want to use it we include it
by saying ``{% load blog_tags %}`` Naming the tag library with the name of the
app it comes from as the prefix makes it clearer where things are coming from
in your templates later.


Creating an inclusion tag
-------------------------

Also `documented`_ in Django's docs, this allow us to just write a simple function that returns a context for the
included template. To start let's just have an empty context and a template that puts some dummy text on the page


.. code-block:: python

    # in blog/templatetags/blog_tags.py
    from django import template

    register = template.Library()

    @register.inclusion_tag('blog/templatetags/entry_history.html')
    def entry_history():
        return {}

That entry_history.html file, and directory we'll need to create that too. Our directory tree should look something like
this (note only the templates directory is expanded)

::

    ├── blog
    ├── manage.py
    ├── myblog
    ├── requirements.txt
    ├── static
    └── templates
        ├── _post.html
        ├── base.html
        ├── blog
        │   ├── post_detail.html
        │   └── templatetags
        │       └── entry_history.html
        └── index.html

So our entry_history.html file can have some dummy text in there, because we just want to make sure it works visually
first. Let's edit the base.html file and put our tag in there. After the `{% load staticfiles %}` tag, put another `{%
load blog_tags %}` and then add the following after About Me

.. code-block:: html

    {% load staticfiles %}
    {% load blog_tags %}


            <div class="large-4 columns">
                <h3>About Me</h3>
                <p>I am a Python developer and I like Django.</p>

                <h3>Previous Posts</h3>
                {% entry_history %}
            </div>

        </section>

Reloading the home page should have the dummy text we put in entry_history.html show up.

.. _documented:: https://docs.djangoproject.com/en/dev/howto/custom-template-tags/#inclusion-tags

Make it work
------------

So our inclusion tag skeleton code is there, but we have no test for this. At the top of `blog/test.py` we need to add
`from django.template import Template, Context` and then at the bottom of the file we'll have

.. code-block:: python

    class PreviousPostTagTest(TestCase):
        TEMPLATE = Template("{% load blog_tags %} {% entry_history %}")

        def setUp(self):
            user = get_user_model().objects.create(username='zoidberg')
            self.post = Post.objects.create(author=user, title="My post title")

        def test_post_shows_up(self):
            context = Context({})
            rendered = self.TEMPLATE.render(context)
            assert self.post.title in rendered


The tricky bits here are `TEMPLATE`, `Context({})` and that `render()` call. These should all look somewhat familiar
from the `django tutuorial part 3`_. `Context({})` in this case just passes no data to a `Template` that we're
rendering directly in memory. That last assert just checks that the title of the post is in the text.

Run the tests and we get

::

    Creating test database for alias 'default'...
    ................F.
    ======================================================================
    FAIL: test_post_shows_up (blog.tests.PreviousPostTagTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      ...
    AssertionError

    ----------------------------------------------------------------------
    Ran 18 tests in 0.109s

    FAILED (failures=1)
    Destroying test database for alias 'default'...

The next step then is to send a list of posts to that template tag for rendering.
In `blog_tags.py` we need to `from ..models import Post` with our other imports and then we'll modify `entry_history`

.. code-block:: python

    def entry_history():
        posts = Post.objects.all()[:10]  # Don't flood that sidebar
        return {'posts': posts}

Then it's a matter of updating the `entry_history.html` file to display the post titles of those posts. Something like
this should work

.. code-block:: html

    <ul>
    {% for post in posts %}
      <li>{{post.title}}</li>
    {% endfor %}
    </ul>

Rerun the tests, and they should all pass.
.. _django tutuorial part 3:: https://docs.djangoproject.com/en/1.6/intro/tutorial03/#write-views-that-actually-do-something

Making it a bit more robust
---------------------------

So we can render some blog posts, but there's no real feedback for empty posts, and we're not really testing what
happens when we've got a LOT (or >10) of posts in the DB. A `{% for %}` loop allows us to define a `{% empty %}` tag,
which you can see in the docs on `for loops`_. Let's add that to the `entry_history.html` and write a quick test for it.
Our new tests should look something like.

.. code-block:: python

    def test_no_posts(self):
        context = Context({})
        rendered = self.TEMPLATE.render(context)
        assert "No posts" in rendered


    def test_many_posts(self):
        for idx in range(12):
            last_post = Post.objects.create(author=self.user, title="My post title {}".format(idx))
        context = Context({})
        rendered = self.TEMPLATE.render(context)
        assert last_post.title not in rendered

The tests themselves have a small problem, `self.user` does not exist! A quick change to our `setUp()` method should fix
that

.. code-block:: python


    def setUp(self):
        self.user = get_user_model().objects.create(username='zoidberg')
        self.post = Post.objects.create(author=self.user, title="My post title")

With that we once again have our failing tests. Try to fix them without looking at our solution code first!


.. _custom template tag: https://docs.djangoproject.com/en/dev/howto/custom-template-tags/#writing-custom-template-tags
.. _for loops: https://docs.djangoproject.com/en/dev/ref/templates/builtins/#for-empty
.. _template documentation: https://docs.djangoproject.com/en/1.6/ref/templates/api/
