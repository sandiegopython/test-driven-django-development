Forms
=====


Adding a Comment form
---------------------

To allow users to create comments we need to accept a form submission. HTML forms are the most common method used to accept user input on web sites and send that data to a server. We can use Django's form framework for this task.

First let's write some tests.  We'll need to create a blog ``Post`` and a ``User`` for our tests.  Let's make a setup method for our tests which creates a post and adds it to the database. The setup method is called before each test in the given test class so that each test will be able to use the ``User`` and ``Post``.

.. code-block:: python

    class CommentFormTest(TestCase):

        def setUp(self):
            user = get_user_model().objects.create_user('zoidberg')
            self.post = Post.objects.create(author=user, title="My post title")

Let's make sure we've imported ``get_user_model`` and ``CommentForm`` in our tests file.  Our imports should look like this:

.. code-block:: python

    from django.test import TestCase
    from django.contrib.auth import get_user_model
    from .models import Post, Comment
    from .forms import CommentForm

Now let's start testing our form.  Let's link our comments to post by allowing our form accept a ``post`` keyword argument like this:

.. code-block:: pycon

    >>> form = CommentForm(post=post)  # Without form data
    >>> form = CommentForm(request.POST, post=post)  # with form data

.. IMPORTANT::
    ``request.POST`` refers to HTTP POST data and not to the blog post. This
    is the data accepted from user input.

Our first test should ensure that our form's ``__init__`` accepts a ``post`` keyword argument:

.. code-block:: python

    def test_init(self):
        CommentForm(post=self.post)

Our next test should ensure that our test raises an exception if a ``post`` keyword argument isn't specified:

.. code-block:: python

    def test_init_without_post(self):
        with self.assertRaises(KeyError):
            CommentForm()

Let's run our tests:

.. code-block:: bash

    $ python manage.py test blog

::

    ImportError: No module named forms

We haven't created our forms file yet so our import is failing.  Let's create an empty ``blog/forms.py`` file.

Now we get:

.. code-block:: bash

    $ python manage.py test blog

::

    ImportError: cannot import name CommentForm

We need to create our ``CommentForm`` model form in ``blog/forms.py``. This form will process the data sent from users trying to comment on a blog post and ensure that it can be saved to our blog database. Let's start with something simple:

.. code-block:: python

    from django import forms
    from .models import Comment


    class CommentForm(forms.ModelForm):
        class Meta:
            model = Comment
            fields = ('name', 'email', 'body')

Here we have created a simple form associated with our Comment model and we
have specified that the form handle only a subset of all of the fields on
the comment.

.. IMPORTANT::
    `Django forms`_ are a powerful way to handle HTML forms. They provide
    a unified way to check submissions against validation rules and
    in the case of ``ModelForm`` subclasses, share any of the associated
    model's validators. In our example, this will ensure that the
    Comment ``email`` is a valid email address.

    .. _Django forms: https://docs.djangoproject.com/en/1.5/topics/forms/

Now our tests should fail because the ``post`` keyword argument is not accepted nor required:

.. code-block:: bash

    $ python manage.py test blog

::

    Creating test database for alias 'default'...
    ...EF.......
    ======================================================================
    ERROR: test_init (blog.tests.CommentFormTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
    ...
    TypeError: __init__() got an unexpected keyword argument 'post'

    ======================================================================
    FAIL: test_init_without_post (blog.tests.CommentFormTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
    ...
    AssertionError: KeyError not raised

    ----------------------------------------------------------------------
    Ran 12 tests in 0.080s

    FAILED (failures=1, errors=1)
    Destroying test database for alias 'default'...

Our two form tests fail as expected.  Let's create a couple more tests for our form before we start fixing it.  We should create at least two tests to make sure our form validation works:

1. Ensure that ``form.is_valid()`` is ``True`` for a form submission with valid data
2. Ensure that ``form.is_valid()`` is ``False`` for a form submission with invalid data (preferably a separate test for each type of error)

This is a good start:

.. code-block:: python

    def test_valid_data(self):
        form = CommentForm({
            'name': "Turanga Leela",
            'email': "leela@example.com",
            'body': "Hi there",
        }, post=self.post)
        self.assertTrue(form.is_valid())
        comment = form.save()
        self.assertEqual(comment.name, "Turanga Leela")
        self.assertEqual(comment.email, "leela@example.com")
        self.assertEqual(comment.body, "Hi there")
        self.assertEqual(comment.post, self.post)

    def test_blank_data(self):
        form = CommentForm({}, post=self.post)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'name': ['required'],
            'email': ['required'],
            'body': ['required'],
        })

It's usually better to test too much than to test too little.

Okay now let's write finally write our form code.

.. code-block:: python

    from django import forms
    from .models import Comment


    class CommentForm(forms.ModelForm):

        def __init__(self, *args, **kwargs):
            self.post = kwargs.pop('post')   # the blog post instance
            super(CommentForm, self).__init__(*args, **kwargs)

        def save(self):
            comment = super(CommentForm, self).save(commit=False)
            comment.post = self.post
            comment.save()
            return comment

        class Meta:
            model = Comment
            fields = ('name', 'email', 'body')

The ``CommentForm`` class is instantiated by passing the blog post that the
comment was written against as well as the HTTP POST data containing the
remaining fields such as comment body and email. The ``save`` method is
overridden here to set the associated blog post before saving the comment.

Let's run our tests again to see whether they pass:

.. code-block:: bash

    $ python manage.py test blog

::

    Creating test database for alias 'default'...
    ...F..........
    ======================================================================
    FAIL: test_blank_data (blog.tests.CommentFormTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
    ...
    AssertionError: {'body': [u'This field is required.'], 'name': [u'This field is required.'], 'email': [u'This field is required.']} != {'body': ['required'], 'name': ['required'], 'email': ['required']}

    ----------------------------------------------------------------------
    Ran 14 tests in 0.086s

    FAILED (failures=1)
    Destroying test database for alias 'default'...

Our test for blank form data is failing because we aren't checking for the correct error strings.  Let's fix that and make sure our tests pass:

.. code-block:: bash

    $ python manage.py test blog

::

    Creating test database for alias 'default'...
    ..............
    ----------------------------------------------------------------------
    Ran 14 tests in 0.085s

 OK
 Destroying test database for alias 'default'...


Displaying the comment form
---------------------------

We've made a form to create comments, but we still don't yet have a way for visitors to use the form.  The Django test client cannot test form submissions, but `WebTest`_ can.  We'll use `django-webtest`_ to handle testing the form submission.

Let's create a test to verify that a form is displayed on our blog post detail page.

First we need to import the ``WebTest`` class (in ``blog/tests.py``):

.. code-block:: python

    from django_webtest import WebTest

Now let's make our ``BlogPostViewTest`` class inherit from ``WebTest``:

.. code-block:: python

    class BlogPostViewTest(WebTest):

        def test_view_page(self):
            page = self.app.get(self.post.get_absolute_url())
            self.assertEqual(len(page.forms), 1)

Now let's update our ``PostDetails`` view (in ``blog/views.py``) to inherit from ``CreateView`` so we can use it to handle submissions to a ``CommentForm``:

.. code-block:: python

    from django.views.generic import CreateView
    from django.shortcuts import get_object_or_404
    from .models import Post
    from .forms import CommentForm


    class PostDetails(CreateView):
        template_name = 'blog/post_detail.html'
        form_class = CommentForm

        def get_post(self):
            return get_object_or_404(Post, pk=self.kwargs['pk'])

        def dispatch(self, *args, **kwargs):
            self.blog_post = self.get_post()
            return super(PostDetails, self).dispatch(*args, **kwargs)

        def get_context_data(self, **kwargs):
            kwargs['post'] = self.blog_post
            return super(PostDetails, self).get_context_data(**kwargs)

    post_details = PostDetails.as_view()


Now if we run our test we'll see 4 failures.  Our blog post detail view is failing to load the page because we aren't passing a ``post`` keyword argument to our form:

.. code-block:: python

    $ python manage.py test
    Creating test database for alias 'default'...
    EEEE...........
    ======================================================================
    ERROR: test_basic_view (blog.tests.BlogPostViewTest)
    ----------------------------------------------------------------------
    ...
    KeyError: 'post'

    ----------------------------------------------------------------------
    Ran 15 tests in 0.079s

    FAILED (errors=4)

Let's get the ``Post`` from the database and pass it to our form.  Our view should look something like this now:

.. code-block:: python

    class PostDetails(CreateView):
        template_name = 'blog/post_detail.html'
        form_class = CommentForm

        def get_post(self):
            return get_object_or_404(Post, pk=self.kwargs['pk'])

        def dispatch(self, *args, **kwargs):
            self.blog_post = self.get_post()
            return super(PostDetails, self).dispatch(*args, **kwargs)

        def get_form_kwargs(self):
            kwargs = super(PostDetails, self).get_form_kwargs()
            kwargs['post'] = self.blog_post
            return kwargs

        def get_context_data(self, **kwargs):
            kwargs['post'] = self.blog_post
            return super(PostDetails, self).get_context_data(**kwargs)

Now when we run our tests we'll see the following assertion error because we have not yet added the comment form to our blog detail page:

.. code-block:: bash

    $ python manage.py test blog

::

    Creating test database for alias 'default'...
    ...F...........
    ======================================================================
    FAIL: test_view_page (blog.tests.BlogPostViewTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/zoidberg/learning-django-by-testing/test/myblog/blog/tests.py", line 81, in test_view_page
        self.assertEqual(len(page.forms), 1)
    AssertionError: 0 != 1

    ----------------------------------------------------------------------
    Ran 15 tests in 0.099s

    FAILED (failures=1)
    Destroying test database for alias 'default'...

Let's add a comment form to the bottom of our ``content`` block in our blog post detail template (``templates/post_detail.html``):

.. code-block:: html

        <h5>Add a comment</h5>
        <form method="post">
            {{ form.as_table }}
            <input type="submit" value="Create Comment">
        </form>

Now our tests pass again:

.. code-block:: bash

    $ python manage.py test blog

::

    Creating test database for alias 'default'...
    ...............
    ----------------------------------------------------------------------
    Ran 15 tests in 0.108s

 OK
 Destroying test database for alias 'default'...

Let's test that our form actually submits.  We should write two tests: one to test for errors, and one to test a successful form submission.

.. code-block:: python

    def test_form_error(self):
        page = self.app.get(self.post.get_absolute_url())
        page = page.form.submit()
        self.assertContains(page, "This field is required.")

    def test_form_success(self):
        page = self.app.get(self.post.get_absolute_url())
        page.form['name'] = "Phillip"
        page.form['email'] = "phillip@example.com"
        page.form['body'] = "Test comment body."
        page = page.form.submit()
        self.assertRedirects(page, self.post.get_absolute_url())

Now let's run our tests:

.. code-block:: bash

    $ python manage.py test blog

::

    Creating test database for alias 'default'...
    ...EE............
    ======================================================================
    ERROR: test_form_error (blog.tests.CommentFormViewTest)
    ----------------------------------------------------------------------
    ...
    AppError: Bad response: 403 FORBIDDEN (not 200 OK or 3xx redirect for http://localhost/post/1)
    ...

    ======================================================================
    ERROR: test_form_success (blog.tests.CommentFormViewTest)
    ----------------------------------------------------------------------
    ...
    AppError: Bad response: 403 FORBIDDEN (not 200 OK or 3xx redirect for http://localhost/post/1)
    ...

    ----------------------------------------------------------------------
    Ran 17 tests in 0.152s

    FAILED (errors=2)

We got a HTTP 403 error because we forgot to add the cross-site request forgery token to our form.  Every HTTP POST request made to our Django site needs to include a CSRF token.  Let's change our form to add a CSRF token field to it:

.. code-block:: html

        <form method="post">
            {% csrf_token %}
            {{ form.as_table }}
            <input type="submit" value="Create Comment">
        </form>

Now only one test fails:

.. code-block:: bash

    $ python manage.py test blog

::

    Creating test database for alias 'default'...
    ....E............
    ======================================================================
    ERROR: test_form_success (blog.tests.CommentFormViewTest)
    ----------------------------------------------------------------------
    ...
    ImproperlyConfigured: No URL to redirect to.  Either provide a url or define a get_absolute_url method on the Model.

    ----------------------------------------------------------------------
    Ran 17 tests in 0.0.166s

    FAILED (errors=1)

Let's fix this by adding a ``get_success_url`` to our view:

.. code-block:: python

    def get_success_url(self):
        return self.get_post().get_absolute_url()

Now our tests pass again and we can submit comments as expected.

.. _WebTest: http://webtest.pythonpaste.org/en/latest/
.. _django-webtest: https://bitbucket.org/kmike/django-webtest/
