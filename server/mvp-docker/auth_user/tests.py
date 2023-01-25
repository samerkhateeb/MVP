from requests.auth import HTTPBasicAuth
import json
from rest_framework import status
from django.test import TestCase, Client
from rest_framework.test import APIClient, APITestCase, APIRequestFactory, RequestsClient, force_authenticate
from django.urls import reverse
from auth_user.models import UserProfile
from django.contrib.auth.models import User
from .api.views import vUserProfile_deposite
from rest_framework import permissions
from unittest.mock import patch
from rest_framework.authtoken.models import Token
import requests
from django.test.client import encode_multipart, RequestFactory
from .api.views import get_tokens_for_user


client = APIClient()


class DepositeTest(APITestCase):
    """ Test module for updating an existing product record """

    def setUp(self):

        self.userA = User.objects.create_user('foo', password='bar')
        self.userA.is_superuser = True
        self.userA.is_staff = True
        self.userA.save()

        self.userB = User.objects.create_user('gogo', password='bar')
        self.userB.is_superuser = True
        self.userB.is_staff = True
        self.userB.save()

        self.casper = UserProfile.objects.create(
            user=self.userA, user_type='1', deposite=5, bio='this is the dummy bio here', sorting=0)

        self.muffin = UserProfile.objects.create(
            user=self.userB, user_type='1', deposite=5, bio='Gradane Gradane Gradane', sorting=0)

        self.valid_payload = {
            'deposite': '5',
        }
        self.invalid_payload = {
            'deposite': '',
        }

    def test_valid_user_deposite(self):
        user = self.userA
        client.force_authenticate(user=user)

        response = client.put(
            reverse('update_deposite'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_invalid_user_deposite(self):
        user = self.userB
        client.force_authenticate(user=user)

        response = client.put(
            reverse('update_deposite'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code,
                         status.HTTP_404_NOT_FOUND)
