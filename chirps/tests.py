import datetime

from chirps.models import Chirp
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

class ChirpTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test',
                                             email='test@test.com',
                                             password='password')

        self.chirp = Chirp.objects.create(message="This is my amazing test chirp",
                                          subject="Test Chirp",
                                          user=self.user)

    def test_is_recent_true(self):
        self.assertTrue(self.chirp.is_recent(), msg="Is Recent not True")

    def test_is_recent_false(self):
        old_time = timezone.now() - datetime.timedelta(days=2)
        self.chirp.created_at = old_time
        self.chirp.save()

        self.assertFalse(self.chirp.is_recent(), "Is Recent incorrectly true")

    def test_tag_count(self):
        self.chirp.tag_set.create(name="test")
        self.chirp.tag_set.create(name="test2")

        self.assertEqual(self.chirp.tag_count, 2, "Tag count doesn't match")

