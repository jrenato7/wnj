from django.test import TestCase

from wnj.galleries.forms import GalleryAddForm


class GalleryAddFormTest(TestCase):
    def setUp(self):
        self.form = GalleryAddForm()

    def test_form_has_fields(self):
        """Form must have an image field"""
        expected = ['image']
        self.assertSequenceEqual(expected, list(self.form.fields))