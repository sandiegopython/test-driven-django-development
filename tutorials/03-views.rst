Views and Templates
===================

Now we can create blog posts and see them in the admin interface, but no one else can see our blog posts yet.


The homepage test
-----------------

Every site should have a homepage. Let's write a failing test for that.

We can use the Django ``TestClient`` to create a test to make sure that our homepage returns an HTTP 200 status code (this is the standard response for a successful HTTP request).

Let's add the following to our ``blog/tests.py`` file:

.. code-block:: python


    class ProjectTests(TestCase):
        def test_homepage(self):
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)


If we run our tests now this test should fail.


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
        <link rel="stylesheet" href="static/css/foundation.css">
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

We'll start with putting our header and a sidebar in ``base.html``:

.. code-block:: html

    <!DOCTYPE html>
    <html>
    <head>
        <title>Foundation 4</title>
        <link rel="stylesheet" href="static/css/foundation.css">
    </head>
    <body>
        <section class="row">
            <header class="large-12 columns">
                <h1>Welcome to My Blog</h1>
                <hr>
            </header>
        </section>

        <section class="row">

            <div class="large-8 columns">
                {% block content %}{% endblock %}
            </div>

            <div class="large-4 columns">
                <h3>About Me</h3>
                <p>My name is Caroline Elizondo and this is my blog.</p>
            </div>

        </section>

    </body>
    </html>

Let's put some filler content in ``index.html``:

.. code-block:: html

    {% extends "base.html" %}

    {% block content %}
    Page body goes here.
    {% endblock content %}


Adding filler content
~~~~~~~~~~~~~~~~~~~~~

Our ``base.html`` defines some ``{% block %}``'s for us. In our ``index.html`` we only really need to fill in the ``content`` block. For now please just ignore the ``class="large-8 column"`` and related stuff. All that does is handle the grid layout from our Zurb Foundation CSS.


.. code-block:: html

    {% extends "base.html" %}

    {% block content %}
        <h2>Post Title</h2>
        <article>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec a diam lectus.
        </article>
    {% endblock content %}

(TODO: Add sections explaining how to add blog posts to homepage and then how to make an individual page for each post)


ListViews
---------

We put some hard-coded posts in our filler view. These post should come from our models instead. Let's write a test for that.

The Django ``TestClient`` can be used for a simple test of whether text shows up on a page.  Let's add the following to our ``blog/tests.py`` file:

.. code-block:: python

    from django.contrib.auth import get_user_model

    class ListPostsOnHomePage(TestCase):

        """Test whether our blog posts show up on the homepage"""

        def setUp(self):
            self.user = get_user_model().objects.create(username='some_user')

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

    {% for post in post_list %}
    <h2>{{ post.title }}</h2>
    <article>
        {{ post.body }}
    </article>
    {% endfor %}


And now, if we add some posts in our admin, they should show up on the homepage. What about viewing an individual blog post?

Blog Post Details
-----------------

To save a bit of time let's make our urls look like ``http://myblog.com/blog/post/ID/`` where ID is the database ID of the blog post we want to see. Let's write a test for that:

.. code-block:: python

    class BlogPostViewTest(TestCase):
        def setUp(self):
            self.user = get_user_model().objects.create(username='some_user')
            self.post = Post.objects.create(title='1-title', body='1-body', author=self.user)

        def test_basic_view(self):
            response = self.client.get(self.post.get_absolute_url())
            self.assertEqual(response.status_code, 200)

This test fails beacuse we didn't define get_absolute_url (`Django Model Instance Documentation`_). We need to create a URL and a view for blog post pages now. We'll need to create a ``blog/urls.py`` file and reference it in the ``myblog/urls.py`` file.

Our ``blog/urls.py`` file is the very short

.. code-block:: python

    from django.conf.urls import patterns, url


    urlpatterns = patterns('blog.views',
        url(r'^post/(?P<pk>\d+)/$', 'post_details'),
    )

The urlconf in ``myblog/urls.py`` needs to reference ``blog.urls``:

.. code-block:: python

    url(r'^blog/', include('blog.urls')),

Now we need to define a ``post_details`` view in our ``blog/views.py`` file:

.. code-block:: python

    from django.http import HttpResponse


    def post_details(request, pk):
        return HttpResponse('empty')

Which we'll be updating later. The final piece is the ``get_absolute_url()`` function. All we need to add to ``blog/models.py`` is

.. code-block:: python

    from django.core.urlresolvers import reverse

    # And in our Post model class...

    def get_absolute_url(self):
        return reverse('blog.views.post_details', kwargs={'pk': self.pk})

And after all that we should have passing tests! Lets make it actually display a blog post. The tests for that are

.. code-block:: python

    def test_blog_title_in_post(self):
        response = self.client.get(self.post.get_absolute_url())
        self.assertContains(response, self.post.title)

    def test_blog_body_in_post(self):
        response = self.client.get(self.post.get_absolute_url())
        self.assertContains(response, self.post.body)

To stay with our class based views we have the `Detail View`_ which will give us another short piece of code

.. code-block:: python

    # blog/views.py

    from django.views.generic import DetailView
    from . import models

    class PostDetails(DetailView):
        model = models.Post

    post_details = PostDetails.as_view()

Which gives us a LOT of errors now that will look like

.. code-block:: bash

    ======================================================================
    ERROR: test_blog_title_in_post (blog.tests.BlogPostViewTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/Users/paulcollins/personal/myblog/blog/tests.py", line 47, in test_blog_title_in_post
        response = self.client.get(self.post.get_absolute_url())
      File "/opt/boxen/data/virturalenvs/sdpug_tdd_django/lib/python2.7/site-packages/django/test/client.py", line 453, in get
        response = super(Client, self).get(path, data=data, **extra)
      File "/opt/boxen/data/virturalenvs/sdpug_tdd_django/lib/python2.7/site-packages/django/test/client.py", line 279, in get
        return self.request(**r)
      File "/opt/boxen/data/virturalenvs/sdpug_tdd_django/lib/python2.7/site-packages/django/test/client.py", line 424, in request
        six.reraise(*exc_info)
      File "/opt/boxen/data/virturalenvs/sdpug_tdd_django/lib/python2.7/site-packages/django/core/handlers/base.py", line 140, in get_response
        response = response.render()
      File "/opt/boxen/data/virturalenvs/sdpug_tdd_django/lib/python2.7/site-packages/django/template/response.py", line 105, in render
        self.content = self.rendered_content
      File "/opt/boxen/data/virturalenvs/sdpug_tdd_django/lib/python2.7/site-packages/django/template/response.py", line 80, in rendered_content
        template = self.resolve_template(self.template_name)
      File "/opt/boxen/data/virturalenvs/sdpug_tdd_django/lib/python2.7/site-packages/django/template/response.py", line 56, in resolve_template
        return loader.select_template(template)
      File "/opt/boxen/data/virturalenvs/sdpug_tdd_django/lib/python2.7/site-packages/django/template/loader.py", line 194, in select_template
        raise TemplateDoesNotExist(', '.join(not_found))
    TemplateDoesNotExist: blog/post_detail.html

    ----------------------------------------------------------------------

Pesky templates. So we need to create ``templates/blog/post_detail.html``, to get back to make the DetailView happy and then we have a ``post`` context variable that we can use. The template then looks like

.. code-block:: html

    {% extends "base.html" %}

    {% block content %}
    <h2>{{ post.title }}</h2>
    <article>
    {{ post.body }}
    </article>
    {% endblock %}

and we're back to passing tests.

.. _zurb foundation files: http://foundation.zurb.com/
.. _direct link: http://foundation.zurb.com/files/foundation-4.3.2.zip
.. _Classy Class Based Views: http://ccbv.co.uk
.. _Django Model Instance Documentation: https://docs.djangoproject.com/en/dev/ref/models/instances/#get-absolute-url
.. _Detail View: http://ccbv.co.uk/projects/Django/1.5/django.views.generic.detail/DetailView/`
