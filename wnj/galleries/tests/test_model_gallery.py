from _datetime import datetime

from django.test import TestCase

from wnj.galleries.models import Gallery
from wnj.accounts.models import User

class GalleryModelTest(TestCase):
    def test_create(self):
        user = User.objects.create(email='nickb@wnj.com', password='nick_pass')
        Gallery.objects.create(
            user=user,
            image='http://wnj.s3.com/media/img-1',
            created_at=datetime.now())
        self.assertTrue(Gallery.objects.exists())

    def test_approved_can_be_blank(self):
        field = Gallery._meta.get_field('approved')
        self.assertTrue(field.blank)