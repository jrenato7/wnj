from django.test import TestCase
from wnj.accounts.forms import AccountSignUpForm

class AccountsSignUpGet(TestCase):

    def setUp(self):
        self.resp = self.client.get('/signup/')

    def test_status_code(self):
        self.assertEqual(self.resp.status_code, 200)

    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'accounts/account_sign_up.html')

    def test_html(self):
        """Html must contain input tags"""
        tags = (
            ('<form', 1),
            ('<input', 5),
            ('type="text"', 1),
            ('type="email"', 1),
            ('type="password"', 1),
            ('type="submit"', 1)
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)

    def test_csrf(self):
        """Html must contains csrf"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have subscription form"""
        form = self.resp.context['form']
        self.assertIsInstance(form, AccountSignUpForm)