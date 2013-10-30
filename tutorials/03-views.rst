Views and Templates
===================

Now we can create blog posts and see them in the admin interface, but no one else can see our blog posts yet.


The easiest test
----------------

Every site should have a default template. Lets write a failing test for this first. The way the Django test finder works in 1.5 it's easiest to just put this new class in the ``blog/test.py`` file for now.

.. code-block:: python


    class ProjectTests(TestCase):
        def test_homepage(self):
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)


All this does is try to get the homepage ``/``, and then assert that the HTTP response code was 200. 200 means it got a page without an error. If we run these tests right now this should fail.


Base template and static files
------------------------------

Let's start with base templates based on zurb foundation.  First download and extract the `Zurb Foundation files`_ (`direct link`_).

Static files
~~~~~~~~~~~~

Create a ``static`` directory in our top-level directory (the one with the ``manage.py`` file).  Move the ``css`` directory from the foundation archive to this new ``static`` direcotry.

Now let's add this new ``static`` directory to our settings file:

.. code-block:: python

    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'static'),
    )

Template files
~~~~~~~~~~~~~~

Create a ``templates`` directory in our top-level directory. Our directory structure should look like

.. code-block:: bash

        ├── blog
        │   ├── __init__.py
        │   ├── admin.py
        │   ├── models.py
        │   ├── tests.py
        │   └── views.py
        ├── manage.py
        ├── myblog
        │   ├── __init__.py
        │   ├── settings.py
        │   ├── urls.py
        │   ├── views.py
        │   └── wsgi.py
        ├── myblog.sqlite3
        ├── static
        │   └── css
        │       ├── foundation.css
        │       ├── foundation.min.css
        │       └── normalize.css
        └── templates

Create a basic HTML file like this and name it ``templates/index.html``:

.. code-block:: html

    <!DOCTYPE html>
    <html>
    <head>
        <title>Foundation 4</title>
        <link rel="stylesheet" href="css/foundation.css">
    </head>
    <body>
        <section class="row">
            <header class="large-12 columns">
                <h1>Welcome to My Blog</h1>
                <hr>
            </header>
        </section>
    </body>
    </html>

Now let's add this new ``templates`` directory to our settings file:

.. code-block:: python

    TEMPLATE_DIRS = (
        os.path.join(BASE_DIR, 'templates'),
    )


Views
-----

Now let's create a homepage using the ``index.html`` template we added.

Let's start by creating a views file: ``myblog/views.py`` referencing the ``index.html`` template:

.. code-block:: python

    from django.views.generic.base import TemplateView


    class HomeView(TemplateView):

        template_name = 'index.html'

    home = HomeView.as_view()

Django will be able to find this template in the ``templates`` folder because of our ``TEMPLATE_DIRS`` setting.
Now we need to route the homepage URL to the home view.  Our URL file should look something like this:

.. code-block:: python

    from django.conf.urls import patterns, include, url
    from myblog import views

    from django.contrib import admin
    admin.autodiscover()

    urlpatterns = patterns('',
        url(r'^$', views.home),
        url(r'^admin/', include(admin.site.urls)),
    )

Now let's visit http://localhost:8000/ in a web browser to check our work.  You should see a webpage that looks like this:

.. image:: _static/03-01_myblog.png

Using a base template
~~~~~~~~~~~~~~~~~~~~~

Templates in Django are generally built up from smaller pieces. This lets you include things like a consistent header and footer on all your pages. Convention is to call one of your templates ``base.html`` and have everything inherit from that.

base.html:

.. code-block:: html

    <!DOCTYPE html>
    <html>
    <head>
        <title>Foundation 4</title>
        <link rel="stylesheet" href="static/css/foundation.css">
    </head>
    <body>
        {% block content %}{% endblock %}
    </body>
    </html>

index.html:

.. code-block:: html

    {% extends "base.html" %}

    {% block content %}
    <section class="row">
        <header class="large-12 columns">
            <h1>Welcome to My Blog</h1>
            <hr>
        </header>
    </section>
    {% endblock content %}


Adding filler content
~~~~~~~~~~~~~~~~~~~~~

Our ``base.html`` defines some ``{% block %}``'s for us. In our ``index.html`` we only really need to fill in the ``content`` block. For now please just ignore the ``class="large-8 column"`` and related stuff. All that does is handle the grid layout from our Zurb Foundation CSS.


.. code-block:: html

    {% extends "base.html" %}

    {% block content %}
    <section class="row">
        <header class="large-12 columns">
            <h1>Welcome to My Blog</h1>
            <hr>
        </header>
    </section>

    <section class="row">

        <div class="large-8 columns">
            <h2>Post Title</h2>
            <article>
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec a diam lectus.
            </article>
        </div>

        <div class="large-4 columns">
            <h3>About Me</h3>
            <p>My name is Caroline Elizondo and this is my blog.</p>

            <h3>Post History</h3>
            <ul class="disc">
                <li><a href="">My Second Post</a></li>
                <li><a href="">My First Post</a></li>
            </ul>
        </div>

    </section>
    {% endblock content %}

(TODO: Add sections explaining how to add blog posts to homepage and then how to make an individual page for each post)


ListViews
---------

In our filler view, we just put some hard coded posts in there. Ideally this should come from our DB, so let's get that under test first.


A simple test for "does this show up on the page" is just to use the TestClient to get a page and then check the response text. So in our ``blog/test.py`` file let's add

.. code-block:: python

    from django.contrib import auth

    class ListPostsOnHomePage(TestCase):
        def setUp(self):
            self.user = auth.get_user_model().objects.create(username='some_user')

        def test_one_post(self):
            Post.objects.create(title='1-title', body='1-body', author=self.user)
            response = self.client.get('/')
            self.assertContains(response, '1-title')
            self.assertContains(response, '1-body')

        def test_two_posts(self):
            Post.objects.create(title='1-title', body='1-body', author=self.user)
            Post.objects.create(title='2-title', body='2-body', author=self.user)
            response = self.client.get('/')
            self.assertContains(response, '1-title')
            self.assertContains(response, '1-body')
            self.assertContains(response, '2-title')

which should fail like this

.. code-block:: bash

    Creating test database for alias 'default'...
    FF..
    ======================================================================
    FAIL: test_one_post (blog.tests.ListPostsOnHomePage)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/Users/paulcollins/personal/myblog/blog/tests.py", line 25, in test_one_post
        self.assertContains(response, '1-title')
      File "/opt/boxen/data/virturalenvs/sdpug_tdd_django/lib/python2.7/site-packages/django/test/testcases.py", line 664, in assertContains
        msg_prefix + "Couldn't find %s in response" % text_repr)
    AssertionError: Couldn't find '1-title' in response

    ======================================================================
    FAIL: test_two_posts (blog.tests.ListPostsOnHomePage)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/Users/paulcollins/personal/myblog/blog/tests.py", line 32, in test_two_posts
        self.assertContains(response, '1-title')
      File "/opt/boxen/data/virturalenvs/sdpug_tdd_django/lib/python2.7/site-packages/django/test/testcases.py", line 664, in assertContains
        msg_prefix + "Couldn't find %s in response" % text_repr)
    AssertionError: Couldn't find '1-title' in response

    ----------------------------------------------------------------------
    Ran 4 tests in 0.201s

    FAILED (failures=2)
    Destroying test database for alias 'default'...


Updating our views
~~~~~~~~~~~~~~~~~~

One easy way to get all our posts objects to list is to just use a ``ListView``. That changes our ``HomeView`` only slightly.

.. code-block:: python

    from django.views.generic import ListView

    from blog import models


    class HomeView(ListView):
        template_name = 'index.html'
        queryset = models.Post.objects.order_by('-created_at')

    home = HomeView.as_view()

That small change will provide a ``post_list`` object to our template ``index.html`` which we can then loop over. For some quick documentation on all the Class Based Views in django, take a look at `Classy Class Based Views`_

The last change needed then is just to update our ``index.html`` to actually put those blog posts in there.

.. code-block:: html

    <div class="large-8 columns">
        {% for post in post_list %}
        <h2>{{ post.title }}</h2>
        <article>
          {{ post.body }}
        </article>
        {% endfor %}
    </div>


And now, if we add some posts in our admin, they should show up on the homepage.

.. _zurb foundation files: http://foundation.zurb.com/
.. _direct link: http://foundation.zurb.com/files/foundation-4.3.2.zip
.. _Classy Class Based Views: http://ccbv.co.uk
