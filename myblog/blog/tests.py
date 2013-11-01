from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import Post


class PostModelTest(TestCase):
    def test_unicode_representation(self):
        post = Post(title="My post title")
        self.assertEqual(unicode(post), post.title)

    def test_get_absolute_url(self):
        user = get_user_model().objects.create(username='some_user')
        post = Post.objects.create(title="My post title", author=user)
        self.assertIsNotNone(post.get_absolute_url())


class ProjectTests(TestCase):
    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


class ListPostsOnHomePage(TestCase):

    """Test whether our blog posts show up on the homepage"""

    def setUp(self):
        self.user = get_user_model().objects.create(username='some_user')

    def test_one_post(self):
        Post.objects.create(title='1-title', body='1-body', author=self.user)
        response = self.client.get('/')
        self.assertContains(response, '1-title')
        self.assertContains(response, '1-body')

    def test_two_posts(self):
        Post.objects.create(title='1-title', body='1-body', author=self.user)
        Post.objects.create(title='2-title', body='2-body', author=self.user)
        response = self.client.get('/')
        self.assertContains(response, '1-title')
        self.assertContains(response, '1-body')
        self.assertContains(response, '2-title')

class BlogPostViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='some_user')
        self.post = Post.objects.create(title='1-title', body='1-body', author=self.user)

    def test_basic_view(self):
        response = self.client.get(self.post.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_blog_title_in_post(self):
        response = self.client.get(self.post.get_absolute_url())
        self.assertContains(response, self.post.title)

    def test_blog_body_in_post(self):
        response = self.client.get(self.post.get_absolute_url())
        self.assertContains(response, self.post.body)