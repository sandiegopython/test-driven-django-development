from django.test import TestCase
from .models import Post


class PostModelTest(TestCase):
    def test_unicode_representation(self):
        post = Post(title="My post title")
        self.assertEqual(unicode(post), post.title)
