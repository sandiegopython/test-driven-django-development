Views and Templates
===================

Now we can create blog posts and see them in the admin interface, but no one else can see our blog posts yet.


Base template and static files
------------------------------

Let's start with base templates based on zurb foundation.  First download and extract the `Zurb Foundation files`_.

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

Create a ``templates`` directory in our top-level directory.

Create a basic HTML file like this:

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

(TODO: Add screenshot)

Using a base template
~~~~~~~~~~~~~~~~~~~~~

TODO: Explain this

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

    {% extends "base.html" %}

    {% block content %}
    <section class="row">
        <header class="large-12 columns">
            <h1>Welcome to My Blog</h1>
            <hr>
        </header>
    </section>
    {% endblock content %}

.. code-block:: html

Adding filler content
~~~~~~~~~~~~~~~~~~~~~

TODO: Explain this briefly (also briefly note that we're going glossing over the row and columns syntax of Foundation)

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


.. _zurb foundation files: http://foundation.zurb.com/
