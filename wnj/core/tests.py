from django.test import TestCase

class HomeTest(TestCase):
    def setUp(self):
        self.resp = self.client.get('/')

    def test_get(self):
        """Must return status code 200"""
        self.assertEqual(self.resp.status_code, 200)

    def test_template(self):
        """Must use index.html"""
        self.assertTemplateUsed(self.resp, 'index.html')

    def test_signup_link(self):
        """Html must contain link to sign up"""
        self.assertContains(self.resp, 'href="/signup/"')

    def test_gallery_link(self):
        """Html must contain link to login"""
        self.assertContains(self.resp, 'href="/login/"')