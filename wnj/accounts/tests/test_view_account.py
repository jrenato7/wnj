from django.test import TestCase

from wnj.accounts.forms import RegisterForm
from wnj.accounts.models import User


class AccountsSignUpGet(TestCase):

    def setUp(self):
        self.resp = self.client.get('/signup/')

    def test_status_code(self):
        """Get /signup/ must return status code 200"""
        self.assertEqual(self.resp.status_code, 200)

    def test_template_used(self):
        """Must use the template accounts/account_sign_up.html"""
        self.assertTemplateUsed(self.resp, 'accounts/account_sign_up.html')

    def test_html(self):
        """Html must contain input tags"""
        tags = (
            ('<form', 1),
            ('<input', 5),
            ('type="email"', 1),
            ('type="password"', 2),
            ('type="submit"', 1)
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)

    def test_csrf(self):
        """Html must contains csrf"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have register form"""
        form = self.resp.context['form']
        self.assertIsInstance(form, RegisterForm)


class AccountSignUpPostValid(TestCase):

    def setUp(self):
        data = dict(
            email='nickb@wnj.com',
            password='NicL12pWs9',
            password2='NicL12pWs9')
        self.resp = self.client.post('/signup/', data=data)

    def test_post(self):
        """The status code must be 302"""
        self.assertEqual(302, self.resp.status_code)

    def test_user_added(self):
        """Must create a new user"""
        self.assertTrue(User.objects.exists())


class AccountSignUpSuccessMessage(TestCase):

    def test_message(self):
        """The template must have a success message"""
        data = dict(
            email='juliette@wnj.com',
            password='JicL12pWs9',
            password2='JicL12pWs9')
        resp = self.client.post('/signup/', data=data, follow=True)
        self.assertContains(resp, 'Success')


class AccountSignUpPostInvalid(TestCase):
    def setUp(self):
        data = {}
        self.resp = self.client.post('/signup/', data)

    def test_post(self):
        """Invalid POST should not redirect"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp,
                                'accounts/account_sign_up.html')

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, RegisterForm)

    def test_form_has_errors(self):
        """The form in context must contain errors """
        form = self.resp.context['form']
        self.assertTrue(form.errors)

    def test_user_dont_added(self):
        """Must not create a new user"""
        self.assertFalse(User.objects.exists())
