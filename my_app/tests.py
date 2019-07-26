from django.contrib.auth.models import User, Permission
from django.test import TestCase

from my_app.models import MentionableExample, TemporaryMention

UNAPPROVED_MENTIONS_TEXT = 'unapproved mentions'
PASSWORD = 'super-strong-password1'

TEST_URL = 'http://test-url.com'


class ApproveWebmentionPermissionTests(TestCase):
    def setUp(self) -> None:
        MentionableExample.objects.create(
            title='Test example',
            slug='webmention-tester',
            summary='',
            main_content='some text').save()

    def test_anon_user__should_not_see_unapproved_webmentions(self):
        response = self.client.get('/')
        self.assertNotContains(response, UNAPPROVED_MENTIONS_TEXT)

    def test_basic_user__should_not_see_unapproved_webmentions(self):
        self.client.force_login(User.objects.create(
            username='basic',
            password=PASSWORD))

        response = self.client.get('/')
        self.assertNotContains(response, UNAPPROVED_MENTIONS_TEXT)

    def test_user_with_perm__should_see_unapproved_webmentions(self):
        permission = Permission.objects.get(codename='approve_webmention')

        user_with_permission = User.objects.create(
            username='webmention-approver',
            password=PASSWORD)
        user_with_permission.user_permissions.add(permission)
        self.client.force_login(user_with_permission)

        response = self.client.get('/')
        self.assertContains(response, UNAPPROVED_MENTIONS_TEXT)

    def test_superuser__should_see_unapproved_webmentions(self):
        self.client.force_login(User.objects.create_superuser(
            username='superuser',
            email='admin@mydomain.org',
            password=PASSWORD))

        response = self.client.get('/')
        self.assertContains(response, UNAPPROVED_MENTIONS_TEXT)


class SubmitTemporaryMentionTest(TestCase):
    def test_get(self):
        response = self.client.get('/submit')
        self.assertTemplateUsed(response, 'submit_temporary_mention.html')

    def test_post_url__should_redirect_to_homepage(self):
        MentionableExample.objects.create(
            title='Test example',
            slug='webmention-tester',
            summary='',
            main_content='some text').save()

        response = self.client.post('/submit', data={'url': TEST_URL})
        self.assertRedirects(response, '/')

    def test_post_url__should_create_temporary_mention(self):
        self.client.post('/submit', data={'url': TEST_URL})
        self.assertIsNotNone(TemporaryMention.objects.get(url=TEST_URL))
