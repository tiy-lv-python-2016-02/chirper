from chirps.models import Chirp
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class TestListCreateChirp(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="test",
                                             email="test@test.com",
                                             password="password")

        self.chirp = Chirp.objects.create(subject="My test chirp",
                                          message="My test chirp message",
                                          user=self.user)

    def test_create_chirp(self):
        token = Token.objects.get(user_id=self.user.id)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        url = reverse('list_create_chirp')
        data = {"subject": "Test Chirp", "message": "Test Chirp Message"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Chirp.objects.count(), 2) 
        self.assertEqual(data["subject"], "Test Chirp")

