Forms
=====

Blogs should be interactive.  Let's allow visitors to comment on each post.

Adding a Comment model
----------------------

First we need to add a ``Comment`` model.

.. code-block:: python

    class Comment(models.Model):
        post = models.ForeignKey(Post)
        name = models.CharField(max_length=100)
        email = models.EmailField()
        body = models.TextField()
        created_at = models.DateTimeField(auto_now_add=True, editable=False)
        modified_at = models.DateTimeField(auto_now=True, editable=False)


Let's write a ``__unicode___`` method for our ``Comment`` model like we did for our ``Post`` model earlier.

First we should create a test.  Our test should look very similar to the ``__unicode__`` test we wrote for posts earlier.  This should suffice:

.. code-block:: python

    class CommentModelTest(TestCase):

        def test_unicode_representation(self):
            comment = Comment(body="My comment body")
            self.assertEqual(unicode(comment), "My comment body")


Now let's run our tests to make sure our new test fails:

.. code-block:: bash

    $ python manage.py test blog
    Creating test database for alias 'default'...
    F.
    ======================================================================
    FAIL: test_unicode_representation (blog.tests.CommentModelTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
    File "/home/zoidberg/learning-django-by-testing/myblog/blog/tests.py", line 16, in test_unicode_representation
    self.assertEqual(unicode(comment), "My comment body")
    AssertionError: u'Comment object' != 'My comment body'

    ----------------------------------------------------------------------
    Ran 2 tests in 0.001s

    FAILED (failures=1)
    Destroying test database for alias 'default'...

Great.  After we implement our ``__unicode__`` method our tests should pass:

.. code-block:: bash

    $ python manage.py test blog
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
    ImportError: No module named forms

We haven't created our forms file yet so our import is failing.  Let's create an empty ``blog/forms.py`` file.

Now we get:

.. code-block:: bash

    $ python manage.py test blog
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
    Creating test database for alias 'default'...
    EF..
    ======================================================================
    ERROR: test_init (blog.tests.CommentFormTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
    File "/home/zoidberg/learning-django-by-testing/myblog/blog/tests.py", line 28, in test_init
        CommentForm(post=self.post)
    TypeError: __init__() got an unexpected keyword argument 'post'

    ======================================================================
    FAIL: test_init_without_post (blog.tests.CommentFormTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
    File "/home/zoidberg/learning-django-by-testing/myblog/blog/tests.py", line 32, in test_init_without_post
        CommentForm()
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
    Creating test database for alias 'default'...
    F.....
    ======================================================================
    FAIL: test_blank_data (blog.tests.CommentFormTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
    File "/home/zoidberg/learning-django-by-testing/myblog/blog/tests.py", line 53, in test_blank_data
    'body': ['required'],
    AssertionError: {'body': [u'This field is required.'], 'name': [u'This field is required.'], 'email': [u'This field is required.']} != {'body': ['required'], 'name': ['required'], 'email': ['required']}

    ----------------------------------------------------------------------
    Ran 6 tests in 0.009s

    FAILED (failures=1)
    Destroying test database for alias 'default'...

Our test for blank form data is failing because we aren't checking for the correct error strings.  Let's fix that and make sure our tests pass:

.. code-block:: bash

    $ python manage.py test blog
    Creating test database for alias 'default'...
    ......
    ----------------------------------------------------------------------
    Ran 6 tests in 0.009s

    OK
    Destroying test database for alias 'default'...
