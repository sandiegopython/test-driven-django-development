Forms
=====

Blogs should be interactive.  Let's allow visitors to comment on each post.

Adding a Comment model
----------------------

First we need to add a ``Comment`` model in ``blog/models.py``.

.. code-block:: python

    class Comment(models.Model):
        post = models.ForeignKey(Post)
        name = models.CharField(max_length=100)
        email = models.EmailField()
        body = models.TextField()
        created_at = models.DateTimeField(auto_now_add=True, editable=False)
        modified_at = models.DateTimeField(auto_now=True, editable=False)


Let's write a ``__unicode___`` method for our ``Comment`` model like we did for our ``Post`` model earlier.

First we should create a test in ``blog/tests.py``.  Our test should look very similar to the ``__unicode__`` test we wrote for posts earlier.  This should suffice:

.. code-block:: python

    class CommentModelTest(TestCase):

        def test_unicode_representation(self):
            comment = Comment(body="My comment body")
            self.assertEqual(unicode(comment), "My comment body")


Now let's run our tests to make sure our new test fails:

.. code-block:: bash

    $ python manage.py test blog
    
::

    Creating test database for alias 'default'...
    F.
    ======================================================================
    FAIL: test_unicode_representation (blog.tests.CommentModelTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
    ...
    AssertionError: u'Comment object' != 'My comment body'

    ----------------------------------------------------------------------
    Ran 9 tests in 0.001s

    FAILED (failures=1)
    Destroying test database for alias 'default'...

Great.  After we implement our ``__unicode__`` method our tests should pass:

.. code-block:: bash

    $ python manage.py test blog
    
::

    Creating test database for alias 'default'...
    ..
    ----------------------------------------------------------------------
    Ran 2 tests in 0.001s

    OK
    Destroying test database for alias 'default'...


Adding a Comment form
---------------------

To allow users to create comments we need to accept a form submission.  We can use Django's form framework for this task.

First let's write some tests.  We'll need to create a ``Post`` and a ``User`` for our tests.  Let's make a setup method for our tests which creates a post and adds it to the database:

.. code-block:: python

    class CommentFormTest(TestCase):

        def setUp(self):
            user = User.objects.create_user('zoidberg')
            self.post = Post.objects.create(author=user, title="My post title")

Let's make sure we've imported ``User`` and ``CommentForm`` in our tests file.  Our imports should look like this:

.. code-block:: python

    from django.test import TestCase
    from django.contrib.auth.models import User
    from .models import Post, Comment
    from .forms import CommentForm

Now let's start testing our form.  Let's link our comments to post by allowing our form accept a ``post`` keyword argument like this:

.. code-block:: pycon

    >>> form = CommentForm(post=post)  # Without form data
    >>> form = CommentForm(request.POST, post=post)  # with form data

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

We need to create our ``CommentForm`` model form.  Let's start with something simple:

.. code-block:: python

    from django import forms
    from .models import Comment


    class CommentForm(forms.ModelForm):
        class Meta:
            model = Comment
            fields = ('name', 'email', 'body')

Now our tests should fail because the ``post`` keyword argument is not accepted nor required:

.. code-block:: bash

    $ python manage.py test blog
    
::

    Creating test database for alias 'default'...
    EF..
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
    Ran 4 tests in 0.005s

    FAILED (failures=1, errors=1)
    Destroying test database for alias 'default'...

Our two form tests fail as expected.  Let's create a couple more tests for our form before we start fixing it.  We should create at least two tests to make sure our form validation works:

1. Assert ``form.is_valid()`` is ``True`` for a form submission with valid data
2. Assert ``form.is_valid()`` is ``False`` for a form submission with invalid data (preferably a separate test for each type of error)

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
            self.post = kwargs.pop('post')
            super(CommentForm, self).__init__(*args, **kwargs)

        def save(self):
            comment = super(CommentForm, self).save(commit=False)
            comment.post = self.post
            comment.save()
            return comment

        class Meta:
            model = Comment
            fields = ('name', 'email', 'body')

Let's run our tests again to see whether they pass:

.. code-block:: bash

    $ python manage.py test blog
    
::

    Creating test database for alias 'default'...
    F.....
    ======================================================================
    FAIL: test_blank_data (blog.tests.CommentFormTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
    ...
    AssertionError: {'body': [u'This field is required.'], 'name': [u'This field is required.'], 'email': [u'This field is required.']} != {'body': ['required'], 'name': ['required'], 'email': ['required']}

    ----------------------------------------------------------------------
    Ran 6 tests in 0.009s

    FAILED (failures=1)
    Destroying test database for alias 'default'...

Our test for blank form data is failing because we aren't checking for the correct error strings.  Let's fix that and make sure our tests pass:

.. code-block:: bash

    $ python manage.py test blog
    
::

    Creating test database for alias 'default'...
    ......
    ----------------------------------------------------------------------
    Ran 6 tests in 0.009s

    OK
    Destroying test database for alias 'default'...


Displaying the comment form
---------------------------

We've made a form to create comments, but we still don't yet have a way for visitors to use the form.  The Django test client cannot test form submissions, but `WebTest`_ can.  We'll use `django-webtest`_ to handle testing the form submission.

First let's install ``django-webtest``:

.. code-block:: bash

    $ pip install webtest django-webtest

Let's create a test to verify that a form is displayed on the page.  Let's add a test:

.. code-block:: python

    # ...
    from django.core.urlresolvers import reverse
    from django_webtest import WebTest
    # ...


    class CommentFormViewTest(WebTest):

        def setUp(self):
            user = get_user_model().objects.create_user('zoidberg')
            self.post = Post.objects.create(author=user, title="My post title")

        def test_view_page(self):
            page = self.app.get(reverse('blog.views.create_comment',
                                        kwargs={'blog_pk': self.post.pk}))
            self.assertEqual(len(page.forms), 1)

Now let's create a view and URL for our comment creation page.  Let's start with a view like this:

.. code-block:: python

from django.views.generic import DetailView, CreateView
from django.shortcuts import get_object_or_404
from .models import Post
from .forms import CommentForm


# ...


class CreateComment(CreateView):
    template_name = 'blog/create_comment.html'
    form_class = CommentForm

create_comment = CreateComment.as_view()

Now if we run our test we'll see a failure because we aren't passing a ``post`` keyword argument to our form:

.. code-block:: python

    $ python manage.py test
    Creating test database for alias 'default'...
    .......E......
    ======================================================================
    ERROR: test_view_page (blog.tests.CommentFormViewTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
    ...
    KeyError: 'post'

    ----------------------------------------------------------------------
    Ran 14 tests in 0.073s

    FAILED (errors=1)

Let's get the ``Post`` from the database and pass it to our form.  Our view should look something like this now:

.. code-block:: python

    class CreateComment(CreateView):
        template_name = 'blog/create_comment.html'
        form_class = CommentForm

        def get_post(self):
            return get_object_or_404(Post, pk=self.kwargs['blog_pk'])

        def get_form_kwargs(self):
            kwargs = super(CreateComment, self).get_form_kwargs()
            kwargs['post'] = self.get_post()
            return kwargs

Now when we run our tests we'll see a ``TemplateDoesNotExist`` error because we haven't created the ``blog/create_comment.html`` template yet.

Let's create a simple template in ``templates/blog/create_comment.html``:

.. code-block:: html

    {% extends "base.html" %}

    {% block content %}
    <form method="post">
        {{ form.as_table }}
        <input type="submit" value="Create Comment">
    </form>
    {% endblock content %}

Now our test should pass.

Let's test that our form actually submits.  We should write two tests: one to test for errors, and one to test a successful form submission.

.. code-block:: python

    def test_form_error(self):
        page = self.app.get(reverse('blog.views.create_comment',
                                    kwargs={'blog_pk': self.post.pk}))
        page = page.form.submit()
        self.assertContains(page, "This field is required.")

    def test_form_success(self):
        page = self.app.get(reverse('blog.views.create_comment',
                                    kwargs={'blog_pk': self.post.pk}))
        page.form['name'] = "Phillip"
        page.form['email'] = "phillip@example.com"
        page.form['body'] = "Test comment body."
        page = page.form.submit()
        self.assertRedirects(page, self.post.get_absolute_url())

Now let's run our tests:

.. code-block:: bash

    $ python manage.py test blog
    Creating test database for alias 'default'...
    .......EE.......
    ======================================================================
    ERROR: test_form_error (blog.tests.CommentFormViewTest)
    ----------------------------------------------------------------------
    ...
    AppError: Bad response: 403 FORBIDDEN (not 200 OK or 3xx redirect for http://localhost/blog/post/1/comment)
    ...

    ======================================================================
    ERROR: test_form_success (blog.tests.CommentFormViewTest)
    ----------------------------------------------------------------------
    ...
    AppError: Bad response: 403 FORBIDDEN (not 200 OK or 3xx redirect for http://localhost/blog/post/1/comment)
    ...

    ----------------------------------------------------------------------
    Ran 16 tests in 0.118s

    FAILED (errors=2)

We got a HTTP 403 error because we forgot to add the cross-site request forgery token to our form.  Every HTTP POST request made to our Django site needs to include a CSRF token.  Let's add that to our template:

.. code-block:: html

    {% extends "base.html" %}

    {% block content %}
    <form method="post">
        {% csrf_token %}
        {{ form.as_table }}
        <input type="submit" value="Create Comment">
    </form>
    {% endblock content %}

Now only one of our tests fails:

.. code-block:: bash

    $ python manage.py test blog
    
::

    Creating test database for alias 'default'...
    ........E.......
    ======================================================================
    ERROR: test_form_success (blog.tests.CommentFormViewTest)
    ----------------------------------------------------------------------
    ...
    ImproperlyConfigured: No URL to redirect to.  Either provide a url or define a get_absolute_url method on the Model.

    ----------------------------------------------------------------------
    Ran 16 tests in 0.056s

    FAILED (errors=1)

Let's fix this by adding a ``get_success_url`` to our view:

.. code-block:: python

    def get_success_url(self):
        return self.get_post().get_absolute_url()

Now our tests should pass.

TODO: Add comments to post page

.. _WebTest: http://webtest.pythonpaste.org/en/latest/
.. _django-webtest: https://bitbucket.org/kmike/django-webtest/
