Forms
=====


Adding a Comment form
---------------------

To allow users to create comments we need to accept a form submission. HTML forms are the most common method used to accept user input on web sites and send that data to a server. We can use `Django's form framework`_ for this task.

.. _Django's form framework: https://docs.djangoproject.com/en/1.6/topics/forms/

First let's write some tests.  We'll need to create a blog ``Entry`` and a ``User`` for our tests.  Let's make a `setup`_ method for our tests which creates an entry and adds it to the database. The `setup`_ method is called before each test in the given test class so that each test will be able to use the ``User`` and ``Entry``.

.. _setup: http://docs.python.org/2.7/library/unittest.html#unittest.TestCase.setUp

.. code-block:: python

    class CommentFormTest(TestCase):

        def setUp(self):
            user = get_user_model().objects.create_user('zoidberg')
            self.entry = Entry.objects.create(author=user, title="My entry title")

Let's make sure we've imported ``CommentForm`` in our tests file.  Our imports should look like this:

.. code-block:: python

    from django.test import TestCase
    from django.contrib.auth import get_user_model

    from .forms import CommentForm
    from .models import Entry, Comment

Before we start testing our form remember that we are writing our tests before actually writing our CommentForm code. In other words, we're pretending that we've already written our code in the way that we want it to work, then we're writing tests for that not-yet-written code. Once we've seen that the tests have failed, we then write the actual code. Lastly, we run the tests again against our implemented code and, if necessary, modify the actual code so the tests run successfully.

Our first test should ensure that our form's ``__init__`` accepts an ``entry`` keyword argument:

.. code-block:: python

    def test_init(self):
        CommentForm(entry=self.entry)

We want to link our comments to entries by allowing our form to accept an ``entry`` keyword argument.  Assuming our ``CommentForm`` has been written this is how we'd like to use it (**you don't need to type this code anywhere**):

.. code-block:: pycon

    >>> form = CommentForm(entry=entry)  # Without form data
    >>> form = CommentForm(request.POST, entry=entry)  # with form data

Our next test should ensure that our form raises an exception if an ``entry`` keyword argument isn't specified:

.. code-block:: python

    def test_init_without_entry(self):
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

We need to create our ``CommentForm`` model form in ``blog/forms.py``. This form will process the data sent from users trying to comment on a blog entry and ensure that it can be saved to our blog database. Let's start with something simple:

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

    .. _Django forms: https://docs.djangoproject.com/en/1.6/topics/forms/

Now our tests should fail because the ``entry`` keyword argument is not accepted nor required:

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
    TypeError: __init__() got an unexpected keyword argument 'entry'

    ======================================================================
    FAIL: test_init_without_entry (blog.tests.CommentFormTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
    ...
    AssertionError: KeyError not raised

    ----------------------------------------------------------------------
    Ran 14 tests in 0.080s

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
        }, entry=self.entry)
        self.assertTrue(form.is_valid())
        comment = form.save()
        self.assertEqual(comment.name, "Turanga Leela")
        self.assertEqual(comment.email, "leela@example.com")
        self.assertEqual(comment.body, "Hi there")
        self.assertEqual(comment.entry, self.entry)

    def test_blank_data(self):
        form = CommentForm({}, entry=self.entry)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'name': ['required'],
            'email': ['required'],
            'body': ['required'],
        })

It's usually better to test too much than to test too little.

Okay now let's finally write our form code.

.. code-block:: python

    from django import forms

    from .models import Comment


    class CommentForm(forms.ModelForm):

        def __init__(self, *args, **kwargs):
            self.entry = kwargs.pop('entry')   # the blog entry instance
            super(CommentForm, self).__init__(*args, **kwargs)

        def save(self):
            comment = super(CommentForm, self).save(commit=False)
            comment.entry = self.entry
            comment.save()
            return comment

        class Meta:
            model = Comment
            fields = ('name', 'email', 'body')

The ``CommentForm`` class is instantiated by passing the blog entry that the
comment was written against as well as the HTTP POST data containing the
remaining fields such as comment body and email. The ``save`` method is
overridden here to set the associated blog entry before saving the comment.

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
    Ran 16 tests in 0.086s

    FAILED (failures=1)
    Destroying test database for alias 'default'...

Our test for blank form data is failing because we aren't checking for the correct error strings.  Let's fix that and make sure our tests pass:

.. code-block:: bash

    $ python manage.py test blog

::

    Creating test database for alias 'default'...
    ..............
    ----------------------------------------------------------------------
    Ran 16 tests in 0.085s

 OK
 Destroying test database for alias 'default'...


Displaying the comment form
---------------------------

We've made a form to create comments, but we still don't yet have a way for visitors to use the form.  The Django test client cannot test form submissions, but `WebTest`_ can.  We'll use `django-webtest`_ to handle testing the form submission.

Let's create a test to verify that a form is displayed on our blog entry detail page.

First we need to import the ``WebTest`` class (in ``blog/tests.py``):

.. code-block:: python

    from django_webtest import WebTest

Now let's make our ``EntryViewTest`` class inherit from ``WebTest``.  Change our ``EntryViewTest`` to inherit from ``WebTest`` instead of from ``TestCase``:

.. code-block:: python

    class EntryViewTest(WebTest):

.. CAUTION::

    **Do not** create a new ``EntryViewTest`` class.  We already have an ``EntryViewTest`` class with tests in it.  If we create a new one, our old class will be overwritten and those tests won't run anymore.  All we want to do is change the parent class for our test from ``TestCase`` to ``WebTest``.

Our tests should continue to pass after this because ``WebTest`` is a subclass of the Django ``TestCase`` class that we were using before.

Now let's add a test to this class:

.. code-block:: python

        def test_view_page(self):
            page = self.app.get(self.entry.get_absolute_url())
            self.assertEqual(len(page.forms), 1)

Now let's update our ``EntryDetail`` view (in ``blog/views.py``) to inherit from ``CreateView`` so we can use it to handle submissions to a ``CommentForm``:

.. code-block:: python

    from django.shortcuts import get_object_or_404
    from django.views.generic import CreateView

    from .forms import CommentForm
    from .models import Entry


    class EntryDetail(CreateView):
        template_name = 'blog/entry_detail.html'
        form_class = CommentForm

        def get_entry(self):
            return get_object_or_404(Entry, pk=self.kwargs['pk'])

        def dispatch(self, *args, **kwargs):
            self.entry = self.get_entry()
            return super(EntryDetail, self).dispatch(*args, **kwargs)

        def get_context_data(self, **kwargs):
            kwargs['entry'] = self.entry
            return super(EntryDetail, self).get_context_data(**kwargs)

    entry_detail = EntryDetail.as_view()


Now if we run our test we'll see 4 failures.  Our blog entry detail view is failing to load the page because we aren't passing an ``entry`` keyword argument to our form:

.. code-block:: python

    $ python manage.py test
    Creating test database for alias 'default'...
    EEEE...........
    ======================================================================
    ERROR: test_basic_view (blog.tests.EntryViewTest)
    ----------------------------------------------------------------------
    ...
    KeyError: 'entry'

    ----------------------------------------------------------------------
    Ran 15 tests in 0.079s

    FAILED (errors=4)

Let's get the ``Entry`` from the database and pass it to our form.  Our view should look something like this now:

.. code-block:: python

    class EntryDetail(CreateView):
        template_name = 'blog/entry_detail.html'
        form_class = CommentForm

        def get_entry(self):
            return get_object_or_404(Entry, pk=self.kwargs['pk'])

        def dispatch(self, *args, **kwargs):
            self.entry = self.get_entry()
            return super(EntryDetail, self).dispatch(*args, **kwargs)

        def get_form_kwargs(self):
            kwargs = super(EntryDetail, self).get_form_kwargs()
            kwargs['entry'] = self.entry
            return kwargs

        def get_context_data(self, **kwargs):
            kwargs['entry'] = self.entry
            return super(EntryDetail, self).get_context_data(**kwargs)

Now when we run our tests we'll see the following assertion error because we have not yet added the comment form to our blog detail page:

.. code-block:: bash

    $ python manage.py test blog

::

    Creating test database for alias 'default'...
    ...F...........
    ======================================================================
    FAIL: test_view_page (blog.tests.EntryViewTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/zoidberg/learning-django-by-testing/test/myblog/blog/tests.py", line 81, in test_view_page
        self.assertEqual(len(page.forms), 1)
    AssertionError: 0 != 1

    ----------------------------------------------------------------------
    Ran 17 tests in 0.099s

    FAILED (failures=1)
    Destroying test database for alias 'default'...

Let's add a comment form to the bottom of our ``content`` block in our blog entry detail template (``templates/entry_detail.html``):

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
        page = self.app.get(self.entry.get_absolute_url())
        page = page.form.submit()
        self.assertContains(page, "This field is required.")

    def test_form_success(self):
        page = self.app.get(self.entry.get_absolute_url())
        page.form['name'] = "Phillip"
        page.form['email'] = "phillip@example.com"
        page.form['body'] = "Test comment body."
        page = page.form.submit()
        self.assertRedirects(page, self.entry.get_absolute_url())

Now let's run our tests:

.. code-block:: bash

    $ python manage.py test blog

::

    Creating test database for alias 'default'...
    ...EE............
    ======================================================================
    ERROR: test_form_error (blog.tests.EntryViewTest)
    ----------------------------------------------------------------------
    ...
    AppError: Bad response: 403 FORBIDDEN (not 200 OK or 3xx redirect for http://localhost/1)
    ...

    ======================================================================
    ERROR: test_form_success (blog.tests.EntryViewTest)
    ----------------------------------------------------------------------
    ...
    AppError: Bad response: 403 FORBIDDEN (not 200 OK or 3xx redirect for http://localhost/1)
    ...

    ----------------------------------------------------------------------
    Ran 19 tests in 0.152s

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
    ERROR: test_form_success (blog.tests.EntryViewTest)
    ----------------------------------------------------------------------
    ...
    ImproperlyConfigured: No URL to redirect to.  Either provide a url or define a get_absolute_url method on the Model.

    ----------------------------------------------------------------------
    Ran 19 tests in 0.0.166s

    FAILED (errors=1)

Let's fix this by adding a ``get_success_url`` to our view:

.. code-block:: python

    def get_success_url(self):
        return self.get_entry().get_absolute_url()

Now our tests pass again and we can submit comments as expected.

.. _WebTest: http://webtest.pythonpaste.org/en/latest/
.. _django-webtest: https://bitbucket.org/kmike/django-webtest/
