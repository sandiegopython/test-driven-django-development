Readable URLS
-------------

Our current URL structure doesn't tell us much about the blog posts, so let's add date and title information to help users and also search engines better identify the post.

For this purpose, we're going to use the URL scheme:
``/year/month/day/slug/``

Slug is a term coined by the newspaper industry for a unique identifier for a newspaper article. In our case, we'll be using the Django ``django.template.defaultfilters.slugify()`` method to convert our text title into a slugified version. For example, "This Is A Test Title" would be converted to lowercase, and spaces replaced by dashes into "this-is-a-test-title."

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

.. code-block::python

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
We will be using these captured parameters to find the right blog post model.


