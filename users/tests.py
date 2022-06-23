from django.contrib.auth import get_user, get_user_model
from django.test import TestCase

User = get_user_model()


class AuthBackendTests(TestCase):
    """
    Test Authentication Backend
    """

    def setUp(self):
        user = User.objects.create(username="username", email="user@test.com")
        user.set_password("testpassword")
        user.save()

    def test_username_login(self):
        self.assertFalse(get_user(self.client).is_authenticated)
        self.client.login(username="username", password="testpassword")
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_email_login(self):
        self.assertFalse(get_user(self.client).is_authenticated)
        self.client.login(username="user@test.com", password="testpassword")
        self.assertTrue(get_user(self.client).is_authenticated)
