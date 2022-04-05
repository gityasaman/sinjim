from django.test import TestCase
from ..models import MyUser

class MyUserTestCase(TestCase):

    def setUp(self):
        self.user1 = MyUser.objects.create(
            email='yasaman@a.com',
            username='yas',
            firstname='yas',
            lastname='shokri'
            )
    def test_model_str(self):
        self.assertEqual(str(self.user1), 'yas')