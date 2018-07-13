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

    def test_add_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, GalleryAddForm)


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


class GalleryAddLikePicture(TestCase):
    def setUp(self):
        user = User(email='nickb@wnj.com', first_name='Nick')
        user.set_password('N%sd00_pTs')
        user.save()
        self.client.login(username='nickb@wnj.com', password='N%sd00_pTs')

        Gallery.objects.create(id=1, user=user, likes=4, created_at='2018-1-1',
            image='http://wnj.s3.com/media/img-1')

        self.resp = self.client.get('/like/1')

    def test_picture_add_like(self):
        """Must increase in 1 the number of likes"""
        gallery = Gallery.objects.get(pk=1)
        self.assertEqual(gallery.likes, 5)

    def test_status_code(self):
        """Must return status code 302"""
        self.assertEqual(302, self.resp.status_code)


class GalleryOrderByPicture(TestCase):
    def setUp(self):
        user = User(email='nickb@wnj.com', first_name='Nick')
        user.set_password('N%sd00_pTs')
        user.save()
        self.client.login(username='nickb@wnj.com', password='N%sd00_pTs')
        g1 = Gallery.objects.create(id=1, user=user, likes=4, approved=True,
                                    image='http://wnj.s3.com/media/img-1')
        g1.created_at = '2018-1-7'
        g1.save()
        g2 = Gallery.objects.create(id=2, user=user, likes=10, approved = True,
                               image='http://wnj.s3.com/media/img-1')
        g2.created_at = '2018-2-15'
        g2.save()
        g3 = Gallery.objects.create(id=3, user=user, likes=0, approved = True,
                               image='http://wnj.s3.com/media/img-1')
        g3.created_at = '2018-3-23'
        g3.save()

    def test_picture_order_by_like(self):
        """Must return the pictures ordered by the number of likes"""
        resp = self.client.get('/gallery/like')
        seq2 = [img.id for img in resp.context['images']]
        seq1 = [2, 1, 3]
        self.assertSequenceEqual(seq1, seq2)

    def test_picture_order_by_created(self):
        """Must return the pictures ordered by creation date"""
        resp = self.client.get('/gallery/date')
        seq2 = [img.id for img in resp.context['images']]
        seq1 = [3, 2, 1]
        self.assertSequenceEqual(seq1, seq2)