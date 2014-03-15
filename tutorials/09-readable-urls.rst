Readable URLs
=============

Our current URL structure doesn't tell us much about the blog entries, so let's add date and title information to help users and also search engines better identify the entry.

For this purpose, we're going to use the URL scheme:
``/year/month/day/slug/``

Slug is a term coined by the newspaper industry for a unique identifier for a newspaper article. In our case, we'll be using the Django ``django.template.defaultfilters.slugify()`` method to convert our text title into a slugified version. For example, "This Is A Test Title" would be converted to lowercase, and spaces replaced by dashes into "this-is-a-test-title."


First, let's update our Model to handle the new slug field.


Model
-----

In our ``Entry`` model, we need to automatically create or update the slug of the entry after saving the entry. First, let's add the slug field to our ``Entry`` model. Add this after the ``modified_at`` field declaration:

.. code-block:: python

    slug = models.SlugField()


Next, we update the save function. We import the slugify method at the top of the file:

.. code-block:: python

    from django.template.defaultfilters import slugify

Now create a save method in our ``Entry`` model that slugifies the title upon saving:

.. code-block:: python

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Entry, self).save(*args, **kwargs)


After this, we will update our ``get_absolute_url()`` method to do a reverse of the new URL using our new year, month, day,
and slug parameters:

.. code-block:: python

    def get_absolute_url(self):
        kwargs = {'year': self.created_at.year,
                  'month': self.created_at.month,
                  'day': self.created_at.day,
                  'slug': self.slug}
        return reverse('blog.views.entry_detail', kwargs=kwargs)


We now have to run South to migrate the database, since we have changed the model. Run the
command to migrate your database. First, we create the new migration (assuming you have finished the previous
tutorial where you created your initial migration):

.. code-block:: bash

    $ ./manage.py schemamigration blog --auto

Next, we run the new migration that we just created:

.. code-block:: bash

    $ ./manage.py migrate blog


Write the Test
--------------

The first step is to define our test for the title. For this purpose, we'll:

#) Create a new blog entry
#) Find the slug for the blog entry
#) Perform an HTTP GET request for the new descriptive URL ``/year/month/day/slug/`` for the blog entry
#) Check that the request succeeded with a code 200

First we need to import the Python ``datetime`` package and the ``slugify`` function into our tests file:

.. code-block:: python

    from django.template.defaultfilters import slugify
    import datetime

Now let's write our test:

.. code-block:: python

    def test_url(self):
        title = "This is my test title"
        today = datetime.date.today()
        Entry.objects.create(title=title, body='body', author=self.user)
        slug = slugify(title)
        url = "/{year}/{month}/{day}/{slug}/".format(
            year=today.year,
            month=today.month,
            day=today.day,
            slug=slug,
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


Try running the tests again, and you should see one failure for the test we just added:

.. code-block:: bash

    $ python manage.py test blog


URL Pattern
-----------

Next we are going to change our ``myblog/blog/urls.py`` file. Replace your code with this:

.. code-block:: python

    from django.conf.urls import patterns, url


    urlpatterns = patterns('blog.views',
        url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$', 'entry_detail'),
    )

Let's break this down. For this URL pattern ``(?P<year>\d{4})``, the outer parentheses are for "capturing" the input.
The ``?P<year>`` specifies that we should capture this into a parameter named "year." And the ``\d{4}`` means the value
we are capturing should be four digits. The next part is the month, where we capture ``\d{1,2}``, which captures either
one or two digits for the month (January would be 1, December would be 12, so 1 or 2 digits will represent the month).
And for the day, we also capture one or two digits.

The next part is capturing the slug in ``(?P<slug>[-\w]+)``. For this part, we name the captured variable "slug" and
look for alphanumeric characters or a dash/hyphen (-).

As you can see from the last part of the pattern, we are opening the method ``entry_detail``, which we will also have to
update.

Save the file, and open up your ``myblog/blog/views.py`` file.



Update View
-----------

In the views file, we have to update our code to be able to handle the new parameters we are capturing in the URL pattern.
We will be using these captured parameters to find the right blog entry. We will be replacing the code for the method ``get_entry``.
Instead of using the Entry ID, we will be using the date (year, month, and day) and slug to identify the entry.

The first step is to create a ``datetime.date`` object from the year, month, and day values captured from the URL.
Then we will create a new entry from the date and the slug, and search for the blog entry. If the blog entry exists, then
we will return the entry. Otherwise, we will return an HTTP 404 error. Here's the code:

.. code-block:: python

    def get_entry(self):
        attrs = self.kwargs
        entry_date = datetime.date(
            int(attrs['year']),
            int(attrs['month']),
            int(attrs['day'])
        )
        return get_object_or_404(Entry, created_at__contains=entry_date,
                                 slug=attrs['slug'])



Now save the file and try running the tests again. You should see all of the tests passing.


An Overlooked Bug
-----------------

What would happen if we gave an invalid date?  For example 30 days in February or a month of "30".

Let's write a test for this case to make sure an exception isn't raised when we construct a ``datetime``.  We want to receive a ``404`` for an invalid date and not a ``500``.  Our test should look like this:

.. code-block:: python

    def test_invalid_url(self):
        response = self.client.get("/0000/00/00/invalid/")
        self.assertEqual(response.status_code, 404)

Let's run our test and see what happens:

.. code-block:: bash

    $ python manage.py test blog
    Creating test database for alias 'default'...
    ...E...............
    ======================================================================
    ERROR: test_invalid_url (blog.tests.CommentFormTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
        ...
    ValueError: year is out of range

    ----------------------------------------------------------------------
    Ran 19 tests in 0.142s

    FAILED (errors=1)
    Destroying test database for alias 'default'...

It looks like we need to handle a ``ValueError`` exception in our view.  Let's handle this exception by raising an ``Http404`` exception when a ``ValueError`` is raised:

.. code-block:: python

    def get_entry(self):
        attrs = self.kwargs
        try:
            entry_date = datetime.date(
                int(attrs['year']),
                int(attrs['month']),
                int(attrs['day'])
            )
        except ValueError:
            raise Http404
        return get_object_or_404(Entry, created_at__contains=entry_date,
                                 slug=attrs['slug'])


Don't forget to import ``Http404``:

.. code-block:: python

    from django.http import Http404

Now let's run our tests and make sure they pass.
