Readable URLs
=============

Our current URL structure doesn't tell us much about the blog entries,
so let's add date and title information to help users and also search
engines better identify the entry.

For this purpose, we're going to use the URL scheme:
``/year/month/day/pk-slug/``

Slug is a term coined by the newspaper industry for a short identifier
for a newspaper article. In our case, we'll be using the Django's
slugify_ method to convert our text title into a slugified version. For
example, "This Is A Test Title" would be converted to lowercase with
spaces replaced by dashes resulting in "this-is-a-test-title" and the
complete URL might be "/2014/03/15/6-this-is-a-test-title/".

.. _slugify: https://docs.djangoproject.com/en/1.7/ref/utils/#django.utils.text.slugify


First, let's update our Model to handle the new slug field.


Model
-----

In our ``Entry`` model, we need to automatically create or update the
slug of the entry after saving the entry. First, let's add the slug
field to our ``Entry`` model. Add this after the ``modified_at`` field
declaration:

.. code-block:: python

    slug = models.SlugField(default='')


Next, we update the save function. We import the slugify method at the
top of the file:

.. code-block:: python

    from django.template.defaultfilters import slugify

Now create a save method in our ``Entry`` model that slugifies the
title upon saving:

.. code-block:: python

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


After this, we will update our ``get_absolute_url()`` method to do a
reverse of the new URL using our new year, month, day, and slug
parameters:

.. code-block:: python

    def get_absolute_url(self):
        kwargs = {'year': self.created_at.year,
                  'month': self.created_at.month,
                  'day': self.created_at.day,
                  'slug': self.slug,
                  'pk': self.pk}
        return reverse('entry_detail', kwargs=kwargs)


We now have to run South to migrate the database, since we have changed
the model. Run the command to migrate your database. First, we create
the new migration (assuming you have finished the previous tutorial
where you created your initial migration):

.. code-block:: bash

    $ python manage.py makemigrations blog

Next, we run the new migration that we just created:

.. code-block:: bash

    $ python manage.py migrate blog


Write the Test
--------------

The first step is to define our test for the title. For this purpose,
we'll:

#) Create a new blog entry
#) Find the slug for the blog entry
#) Perform an HTTP GET request for the new descriptive URL
   ``/year/month/day/pk-slug/`` for the blog entry
#) Check that the request succeeded with a code 200

First we need to import the Python ``datetime`` package and the
``slugify`` function into our tests file:

.. code-block:: python

    from django.template.defaultfilters import slugify
    import datetime

Now let's write our test in the ``EntryViewTest`` class:

.. code-block:: python

    def test_url(self):
        title = "This is my test title"
        today = datetime.date.today()
        entry = Entry.objects.create(title=title, body="body",
                                     author=self.user)
        slug = slugify(title)
        url = "/{year}/{month}/{day}/{pk}-{slug}/".format(
            year=today.year,
            month=today.month,
            day=today.day,
            slug=slug,
            pk=entry.pk,
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                template_name='blog/entry_detail.html')


Try running the tests again, and you should see one failure for the
test we just added:

.. code-block:: bash

    $ python manage.py test blog


URL Pattern
-----------

Next we are going to change our ``blog/urls.py`` file. Replace your
code with this:

.. code-block:: python

    from django.conf.urls import url

    from . import views

    urlpatterns = [
        url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<pk>\d+)-(?P<slug>[-\w]*)/$', views.EntryDetail.as_view(), name='entry_detail'),
    ]

Let's break this down. For this URL pattern ``(?P<year>\d{4})``, the
outer parentheses are for "capturing" the input. The ``?P<year>``
specifies that we should capture this into a parameter named "year."
And the ``\d{4}`` means the value we are capturing should be four
digits. The next part is the month, where we capture ``\d{1,2}``, which
captures either one or two digits for the month (January would be 1,
December would be 12, so 1 or 2 digits will represent the month). And
for the day, we also capture one or two digits.

We capture the pk (i.e. the "primary key" for accessing a Django model)
with ``(?P<pk>\d+)``.

The next part is capturing the slug in ``(?P<slug>[-\w]*)``. For this
part, we name the captured variable "slug" and look for alphanumeric
characters or a dash/hyphen (-).

As you can see from the last part of the pattern, we are using the view
``EntryDetail``.

Now save the file and try running the tests again. You should see all
of the tests passing.

Another Test
------------

What would happen if we changed the slug or an invalid date was given
in the URL?  This shouldn't matter because we only check for the model
``pk``.

Let's write a couple more tests for this case to make sure the correct
page is displayed in this case, and for when the id does not exist. Our
tests should look like this:

.. code-block:: python

    def test_misdated_url(self):
        entry = Entry.objects.create(
            title="title", body="body", author=self.user)
        url = "/0000/00/00/{0}-misdated/".format(entry.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, template_name='blog/entry_detail.html')

    def test_invalid_url(self):
        entry = Entry.objects.create(
            title="title", body="body", author=self.user)
        response = self.client.get("/0000/00/00/0-invalid/")
        self.assertEqual(response.status_code, 404)

Now let's run our tests and make sure they still pass.


.. TIP::

    If you try to add an entry in the admin, you will notice that you
    must write a slug (it isn't optional) but then whatever you write
    is overwritten in the ``Entry.save()`` method. There are a couple
    ways to resolve this but one way is to set the ``SlugField`` in
    our ``Entry`` model to be ``editable=False`` which will hide it in
    the admin or other forms:

    .. code-block:: python

        slug = SlugField(editable=False)

    See the Django docs on editable_ for details.

    .. _editable: https://docs.djangoproject.com/en/1.7/ref/models/fields/#editable
