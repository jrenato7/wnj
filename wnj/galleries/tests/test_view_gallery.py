from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from wnj.accounts.models import User
from wnj.galleries.forms import GalleryAddForm
from wnj.galleries.models import Gallery


class GalleryListTest(TestCase):
    def setUp(self):
        user = User(email='nickb@wnj.com')
        user.set_password('N%sd00_pTs')
        user.save()
        Gallery.objects.create(
            user=user,
            image='http://wnj.s3.com/media/img-1',
            created_at="2018-7-11")
        Gallery.objects.create(
            user=user,
            image='http://wnj.s3.com/media/img-2',
            created_at="2018-6-11")
        self.client.login(username='nickb@wnj.com',
                          password='N%sd00_pTs')
        self.resp = self.client.get('/gallery/')

    def test_status_code(self):
        """Must return status code 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """Must use template galleries/gallery.html"""
        self.assertTemplateUsed(self.resp, 'galleries/gallery.html')


class UserGalleryTest(TestCase):
    def setUp(self):
        user = User(email='nickb@wnj.com')
        user.set_password('N%sd00_pTs')
        user.save()
        self.client.login(username='nickb@wnj.com',
                          password='N%sd00_pTs')
        self.resp = self.client.get('/moments/')

    def test_status_code(self):
        """Must return status code 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """Must use template galleries/moments.html"""
        self.assertTemplateUsed(self.resp, 'galleries/moments.html')


class GalleryAddGet(TestCase):
    def setUp(self):
        user = User(email='nickb@wnj.com')
        user.set_password('N%sd00_pTs')
        user.save()
        self.client.login(username='nickb@wnj.com', password='N%sd00_pTs')
        self.resp = self.client.get('/add_picture/')

    def test_status_code(self):
        """Must return status code 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """Must use template galleries/add_picture.html"""
        self.assertTemplateUsed(self.resp, 'galleries/gallery_add.html')

    def test_add_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, GalleryAddForm)


TINY_GIF = b'GIF89a\x01\x00\x01\x00\x00\xff\x00,' \
           b'\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x00;'


class GalleryAddPostValid(TestCase):
    def setUp(self):
        user = User(email='nickb@wnj.com')
        user.set_password('N%sd00_pTs')
        user.save()
        self.client.login(username='nickb@wnj.com', password='N%sd00_pTs')
        data = dict(image=SimpleUploadedFile('tiny.gif', TINY_GIF))
        self.resp = self.client.post('/add_picture/', data=data, follow=True)

    def test_picture_add(self):
        self.assertTrue(Gallery.objects.exists())

    def test_status_code(self):
        """Must return status code 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """Must use template galleries/add_picture.html"""
        self.assertTemplateUsed(self.resp, 'galleries/moments.html')
