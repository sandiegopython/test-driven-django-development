TemplateTags
============

Blogs tend to have a list of blog posts on a sidebar as a nice set of quick
links to previous entries. We could make another template and then ``{% include
"my_template.html" %}``, but then we have to worry about including the list of
posts in the context for every page that uses it. Ugh. `Custom template tags`_
allow us to just to just put one tag in the templates we care about, and that's
it.

.. _Custom template tags: https://docs.djangoproject.com/en/dev/howto/custom-template-tags/#writing-custom-template-tags

.. NOTE::
  A custom template tag that itself fires a SQL query means that our HTML
  templates can add more SQL queries to our view. That hides some behavor It's too early at this point,
  but that query should be cached if we expect to use this often.

Where
-----

Create a ``templatetags`` directory in ``blog`` so we have somthing like this.

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

Also `documented`_ in Django's docs, this allow us to just write a simple function that returns a context for the included template.

.. _documented:: https://docs.djangoproject.com/en/dev/howto/custom-template-tags/#inclusion-tags

#TODO: Wait how am I suppose to test this? https://github.com/kmike/django-widget-tweaks/blob/master/widget_tweaks/tests.py#L33 for ideas
