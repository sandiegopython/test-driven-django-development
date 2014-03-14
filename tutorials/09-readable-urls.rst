Readable URLS
-------------

Our current URL structure doesn't tell us much about the blog posts, so let's add date and title information to help users and also search engines better identify the post.

For this purpose, we're going to use the URL scheme:
``/year/month/day/slug/``

Slug is a term coined by the newspaper industry for a unique identifier for a newspaper article. In our case, we'll be using the Django ``django.template.defaultfilters.slugify()`` method to convert our text title into a slugified version. For example, "This Is A Test Title" would be converted to lowercase, and spaces replaced by dashes into "this-is-a-test-title."


First, let's update our Model to handle the new slug field.

Model
======

In the file ``myblog/blog/models.py``, we will need to automatically create or update the slug of the post after saving the post.
So the first thing is to add the slug field to our Entry model. Add this after the ``modified_at`` declaration:

.. code-block:: python
    slug = models.SlugField()


Next, we update the save function. We import the slugify method at the top of the file:

.. code-block:: python

    from django.template.defaultfilters import slugify

Create a save method in our Entry model that slugifies the title upon saving:

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
``./manage.py schemamigration blog --auto``

Next, we run the new migration that we just created:
``./manage.py migrate blog``

Write the Test
==============

The first step is to define our test for the title. For this purpose, we'll:
# Create a new blog post
# Find the slug for the blog post
# Perform an HTTP GET request for the new descriptive URL ``/year/month/day/slug/`` for the blog post
# Check that the request succeeded with a code 200

.. code-block:: python

    def test_url(self):
        from django.template.defaultfilters import slugify
        import datetime
        title = "This is my test title"
        today = datetime.date.today()
        Entry.objects.create(title=title, body='body', author=self.user)
        slug = slugify(title)
        url = "/{year}/{month}/{day}/{slug}/".format(year=today.year,month=today.month,day=today.day, slug=slug)
        print url
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


Try running the tests again, and you should see one failure for the test we just added: ``python manage.py test blog``

URL Pattern
============

Next we are going to change our ``myblog/blog/urls.py`` file as we had defined previously. Replace your code with this:

.. code-block:: python

    from django.conf.urls import patterns, url
    urlpatterns = patterns('blog.views',
        url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$', 'entry_detail'),
    )

Let's break this down. For this URL pattern``(?P<year>\d{4})``, the outer parentheses are for "capturing" the input.
The ``?P<year>`` specifies that we should capture this into a parameter named "year." And the ``\d{4}`` means the value
we are capturing should be four digits. The next part is the month, where we capture ``\d{1,2}``, which captures either
one or two digits for the month (January would be 1, December would be 12, so 1 or 2 digits will represent the month). 
And for the day, we also capture one or two digits.

The next part is capturing the slug in `, `(?P<slug>[-\w]+)``. For this part, we name the captured variable "slug" and 
look for alphanumeric characters or a dash/hyphen (-).

As you can see from the last part of the pattern, we are opening the method ``entry_detail``, which we will also have to 
update.




Save the file, and open up your ``myblog/blog/views.py``

Update View
===========

In the views.py, we have to update our code to be able to handle the new parameters we are capturing in the URL pattern.
We will be using these captured parameters to find the right blog post model. We will be replacing the code for the method ``get_entry``.
Instead of using the Entry ID, we will be using the date (year, month, and day) and slug to identify the post. 

The first step is to create a ``datetime.date`` object from the year, month, and day values captured from the URL. 
Then we will create a new entry from the date and the slug, and search for the blog post. If the blog post exists, then
we will return the post. Otherwise, we will return an HTTP 404 error. Here's the code:

.. code-block:: python

    def get_entry(self):
        entry_date = datetime.date(int(self.kwargs['year']),int(self.kwargs['month']),int(self.kwargs['day']))
        try:
            current_entry = Entry.objects.filter(
                created_at__contains=entry_date,
                slug=self.kwargs['slug'])
            return current_entry[0]
        except Poll.DoesNotExist:
            raise Http404


Now save the file.



Try running the tests again. You should see all of the tests passing.
