Readable URLS
-------------

Our current URL structure doesn't tell us much about the blog posts, so let's add date and title information to help users and also search engines better identify the post.

For this purpose, we're going to use the URL scheme:
``/year/month/day/slug/``

Slug is a term coined by the newspaper industry for a unique identifier for a newspaper article. In our case, we'll be using the Django ``django.template.defaultfilters.slugify()`` method to convert our text title into a slugified version. For example, "This Is A Test Title" would be converted to lowercase, and spaces replaced by dashes into "this-is-a-test-title."

Write the Test
==============

The first step, as usual, is to define our test for the title. For this purpose, we'll:
# Create a new blog post
# Find the slug for the blog post
# Perform an HTTP GET request for the new descriptive URL ``/year/month/day/slug/`` for the blog post
# Check that the request succeeded with a code 200

So, here's the code:



