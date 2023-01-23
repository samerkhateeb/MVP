from requests.auth import HTTPBasicAuth
import json
from rest_framework import status
from django.test import TestCase, Client
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from auth_user.models import UserProfile
from django.contrib.auth.models import User
from .api.views import vUserProfile_deposite
from rest_framework import permissions
from unittest.mock import patch
from rest_framework.authtoken.models import Token
import requests


# initialize the APIClient app
client = APIClient()
user = User.objects.get(username='samer1alkhatib2_734')
token = token = Token.objects.get(user__username='samer1alkhatib2_734')
headers = {
    'Authorization': 'Bearer ' + str(user.auth_token)
}


class DepositeTest(APITestCase):
    """ Test module for updating an existing product record """

    def setUp(self):

        userA = User.objects.create_user('foo', password='bar')
        userA.is_superuser = True
        userA.is_staff = True
        userA.save()

        userB = User.objects.create_user('gogo', password='bar')
        userB.is_superuser = True
        userB.is_staff = True
        userB.save()

        self.casper = UserProfile.objects.create(
            user=userA, user_type='1', deposite=5, bio='this is the dummy bio here', sorting=0)

        self.muffin = UserProfile.objects.create(
            user=userB, user_type='1', deposite=5, bio='Gradane Gradane Gradane', sorting=0)

        self.valid_payload = {
            'deposite': '5',
        }
        self.invalid_payload = {
            'deposite': '',
        }

    def test_valid_user_deposite(self):
        response = client.put(
            reverse('update_deposite'),
            data=json.dumps(self.valid_payload),
            headers=headers,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_user_deposite(self):
        response = client.put(
            reverse('update_deposite'),
            data=json.dumps(self.invalid_payload),
            headers=headers,
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
