from django.test import TestCase
from wnj.accounts.models import User


class UserMotelTest(TestCase):
    def test_create(self):
        obj = User(email='nickb@wnj.com')
        obj.set_password('nick_pass')
        obj.save()
        self.assertTrue(User.objects.exists())