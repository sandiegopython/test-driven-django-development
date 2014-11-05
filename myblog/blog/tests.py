import datetime

from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
from django.template import Template, Context
from django.test import TestCase
from django_webtest import WebTest

from .forms import CommentForm
from .models import Entry, Comment


class EntryModelTest(TestCase):

    def test_string_representation(self):
        entry = Entry(title="My entry title")
        self.assertEqual(str(entry), entry.title)

    def test_get_absolute_url(self):
        user = get_user_model().objects.create(username='some_user')
        entry = Entry.objects.create(title="My entry title", author=user)
        self.assertIsNotNone(entry.get_absolute_url())

    def test_verbose_name_plural(self):
        self.assertEqual(str(Entry._meta.verbose_name_plural), "entries")


class CommentModelTest(TestCase):

    def test_string_representation(self):
        comment = Comment(body="My comment body")
        self.assertEqual(str(comment), "My comment body")

    def test_gravatar_url(self):
        comment = Comment(body="My comment body", email="email@example.com")
        expected = "http://www.gravatar.com/avatar/5658ffccee7f0ebfda2b226238b1eb6e"
        self.assertEqual(comment.gravatar_url(), expected)


class ProjectTests(TestCase):

    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


class HomePageTests(TestCase):

    """Test whether our blog entries show up on the homepage"""

    def setUp(self):
        self.user = get_user_model().objects.create(username='some_user')

    def test_one_entry(self):
        Entry.objects.create(title='1-title', body='1-body', author=self.user)
        response = self.client.get('/')
        self.assertContains(response, '1-title')
        self.assertContains(response, '1-body')

    def test_two_entries(self):
        Entry.objects.create(title='1-title', body='1-body', author=self.user)
        Entry.objects.create(title='2-title', body='2-body', author=self.user)
        response = self.client.get('/')
        self.assertContains(response, '1-title')
        self.assertContains(response, '1-body')
        self.assertContains(response, '2-title')

    def test_no_entries(self):
        response = self.client.get('/')
        self.assertContains(response, 'No blog entries yet.')


class EntryViewTest(WebTest):

    def setUp(self):
        self.user = get_user_model().objects.create(username='some_user')
        self.entry = Entry.objects.create(title='1-title', body='1-body',
                                          author=self.user)

    def test_basic_view(self):
        response = self.client.get(self.entry.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_title_in_entry(self):
        response = self.client.get(self.entry.get_absolute_url())
        self.assertContains(response, self.entry.title)

    def test_body_in_entry(self):
        response = self.client.get(self.entry.get_absolute_url())
        self.assertContains(response, self.entry.body)

    def test_view_page(self):
        page = self.app.get(self.entry.get_absolute_url())
        self.assertEqual(len(page.forms), 1)

    def test_comment_list(self):
        Comment.objects.create(
            entry=self.entry,
            name="Phillip",
            email="phillip@example.com",
            body="Test comment body.",
        )
        response = self.client.get(self.entry.get_absolute_url())
        self.assertContains(response, "Posted by Phillip")
        self.assertContains(response, "Test comment body.")
        self.assertNotContains(response, "No comments yet.")

    def test_empty_comment_list(self):
        response = self.client.get(self.entry.get_absolute_url())
        self.assertContains(response, "No comments yet.")

    def test_form_error(self):
        page = self.app.get(self.entry.get_absolute_url())
        page = page.form.submit()
        self.assertContains(page, "This field is required.")

    def test_form_success(self):
        page = self.app.get(self.entry.get_absolute_url())
        page.form['name'] = "Phillip"
        page.form['email'] = "phillip@example.com"
        page.form['body'] = "Test comment body."
        page = page.form.submit()
        self.assertRedirects(page, self.entry.get_absolute_url())


class CommentFormTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user('zoidberg')
        self.entry = Entry.objects.create(author=self.user, title="My entry title")

    def test_init(self):
        CommentForm(entry=self.entry)

    def test_init_without_entry(self):
        with self.assertRaises(KeyError):
            CommentForm()

    def test_valid_data(self):
        form = CommentForm({
            'name': "Turanga Leela",
            'email': "leela@example.com",
            'body': "Hi there",
        }, entry=self.entry)
        self.assertTrue(form.is_valid())
        comment = form.save()
        self.assertEqual(comment.name, "Turanga Leela")
        self.assertEqual(comment.email, "leela@example.com")
        self.assertEqual(comment.body, "Hi there")
        self.assertEqual(comment.entry, self.entry)

    def test_blank_data(self):
        form = CommentForm({}, entry=self.entry)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'name': ['This field is required.'],
            'email': ['This field is required.'],
            'body': ['This field is required.'],
        })

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


class EntryHistoryTagTest(TestCase):

    TEMPLATE = Template("{% load blog_tags %} {% entry_history %}")

    def setUp(self):
        self.user = get_user_model().objects.create(username='zoidberg')

    def test_entry_shows_up(self):
        entry = Entry.objects.create(author=self.user, title="My entry title")
        rendered = self.TEMPLATE.render(Context({}))
        self.assertIn(entry.title, rendered)

    def test_no_posts(self):
        rendered = self.TEMPLATE.render(Context({}))
        self.assertIn("No recent entries", rendered)

    def test_many_posts(self):
        for n in range(1, 6):
            Entry.objects.create(author=self.user, title="Post #{0}".format(n))
        rendered = self.TEMPLATE.render(Context({}))
        self.assertIn("Post #5", rendered)
        self.assertNotIn("Post #6", rendered)
