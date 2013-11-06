from django.db import models
from django.core.urlresolvers import reverse


class Post(models.Model):
    title = models.CharField(max_length=500)
    author = models.ForeignKey('auth.User')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog.views.post_details', kwargs={'pk': self.pk})


class Comment(models.Model):
    post = models.ForeignKey(Post)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)

    def __unicode__(self):
        return self.body
