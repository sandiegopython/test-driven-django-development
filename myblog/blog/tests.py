from django.template import Template, Context
from django.test import TestCase
from django.contrib.auth import get_user_model
from django_webtest import WebTest
from .models import Post, Comment
from .forms import CommentForm


class PostModelTest(TestCase):

    def test_unicode_representation(self):
        post = Post(title="My post title")
        self.assertEqual(unicode(post), post.title)

    def test_get_absolute_url(self):
        user = get_user_model().objects.create(username='some_user')
        post = Post.objects.create(title="My post title", author=user)
        self.assertIsNotNone(post.get_absolute_url())


class CommentModelTest(TestCase):

    def test_unicode_representation(self):
        comment = Comment(body="My comment body")
        self.assertEqual(unicode(comment), "My comment body")


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

    def test_no_posts(self):
        response = self.client.get('/')
        self.assertContains(response, 'No blog post entries yet.')


class BlogPostViewTest(WebTest):

    def setUp(self):
        self.user = get_user_model().objects.create(username='some_user')
        self.post = Post.objects.create(title='1-title', body='1-body',
                                        author=self.user)

    def test_basic_view(self):
        response = self.client.get(self.post.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_blog_title_in_post(self):
        response = self.client.get(self.post.get_absolute_url())
        self.assertContains(response, self.post.title)

    def test_blog_body_in_post(self):
        response = self.client.get(self.post.get_absolute_url())
        self.assertContains(response, self.post.body)

    def test_view_page(self):
        page = self.app.get(self.post.get_absolute_url())
        self.assertEqual(len(page.forms), 1)

    def test_form_error(self):
        page = self.app.get(self.post.get_absolute_url())
        page = page.form.submit()
        self.assertContains(page, "This field is required.")

    def test_form_success(self):
        page = self.app.get(self.post.get_absolute_url())
        page.form['name'] = "Phillip"
        page.form['email'] = "phillip@example.com"
        page.form['body'] = "Test comment body."
        page = page.form.submit()
        self.assertRedirects(page, self.post.get_absolute_url())


class CommentFormTest(TestCase):

    def setUp(self):
        user = get_user_model().objects.create_user('zoidberg')
        self.post = Post.objects.create(author=user, title="My post title")

    def test_init(self):
        CommentForm(post=self.post)

    def test_init_without_post(self):
        with self.assertRaises(KeyError):
            CommentForm()

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
            'name': ['This field is required.'],
            'email': ['This field is required.'],
            'body': ['This field is required.'],
        })

class PreviousPostTagTest(TestCase):
    TEMPLATE = Template("{% load blog_tags %} {% entry_history %}")

    def setUp(self):
        user = get_user_model().objects.create(username='zoidberg')
        self.post = Post.objects.create(author=user, title="My post title")

    def test_no_posts(self):
        context = Context({})
        rendered = self.TEMPLATE.render(context)
        assert self.post.title in rendered

    def test_post_shows_up(self):
        context = Context({})
        rendered = self.TEMPLATE.render(context)
        assert self.post.title in rendered

