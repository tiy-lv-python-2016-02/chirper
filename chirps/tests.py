import datetime

from chirps.models import Chirp
from chirps.views import ChirpDetail
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory
from django.utils import timezone
from faker import Faker


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

class ChirpListTests(TestCase):

    def setUp(self):
        fake = Faker()

        self.user = User.objects.create_user(username="tester",
                                             email=fake.email(),
                                             password="password")

        for _ in range(20):
            Chirp.objects.create(user=self.user,
                                 subject=fake.text(max_nb_chars=45),
                                 message=fake.text(max_nb_chars=140))

    def test_list_chirp_order(self):

        response = self.client.get(reverse("chirp_list"))
        chirps = response.context["chirp_list"]
        self.assertEqual(response.status_code, 200)
        self.assertTrue(chirps[0].created_at > chirps[1].created_at)
        self.assertTrue(chirps[0].created_at > chirps[2].created_at)

    def test_list_chirp_count(self):

        response = self.client.get(reverse("chirp_list"))
        chirps = response.context["chirp_list"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(chirps.count(), 5)

class ChirpDetailTests(TestCase):

    def setUp(self):
        fake = Faker()

        self.user = User.objects.create_user(username="tester",
                                             email=fake.email(),
                                             password="password")

        for _ in range(10):
            Chirp.objects.create(user=self.user,
                                 subject=fake.text(max_nb_chars=45),
                                 message=fake.text(max_nb_chars=140))

    def test_chirp_detail(self):
        db_chirp = Chirp.objects.last()

        response = self.client.get(reverse("chirp_detail", args=(db_chirp.id,)))
        chirp = response.context["chirp"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(chirp.id, db_chirp.id)
        self.assertTrue("time_run" in response.context)


class ChirpCreateTests(TestCase):
    def setUp(self):
        self.fake = Faker()

        self.user = User.objects.create_user(username="tester",
                                             email=self.fake.email(),
                                             password="password")

    def test_chirp_create(self):

        self.client.force_login(user=self.user)
        response = self.client.post(reverse("chirp_create"),
                                    {"subject":"hello",
                                     "message":"Hello"
                                     })

        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(response.url, reverse('login'))
        chirp = Chirp.objects.last()
        self.assertEqual(chirp.user, self.user)
        self.assertEqual(chirp.subject, "hello")

