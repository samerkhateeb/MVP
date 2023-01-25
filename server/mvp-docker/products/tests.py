from django.test import TestCase
import json
from rest_framework import status
from django.test import TestCase, Client
from rest_framework.test import APIClient

from django.urls import reverse
from .models import ProductsModel as Product
from .api.serializers import ProductsSerializer
from auth_user.models import UserProfile
# Create your tests here.
from django.contrib.auth.models import User
from cms.models import Page, Title
from rest_framework.authtoken.models import Token
from auth_user.api.views import get_tokens_for_user

# initialize the APIClient app
client = APIClient()


class ProductTest(TestCase):
    """ Test module for product model """

    def setUp(self):
        self.userA = User.objects.create_user('foo', password='bar')
        self.userA.is_superuser = True
        self.userA.is_staff = True
        self.userA.save()

        self.userB = User.objects.create_user('gogo', password='bar')
        self.userB.is_superuser = True
        self.userB.is_staff = True
        self.userB.save()

        UserProfile.objects.create(
            user=self.userA, user_type='1', deposite=5, bio='this is the dummy bio here', sorting=0)
        UserProfile.objects.create(
            user=self.userB, user_type='1', deposite=5, bio='this is the dummy bio here', sorting=0)

        Product.objects.create(
            title='Casper', amount=3, description='Bull Dog', cost=10, seller=self.userA)
        Product.objects.create(
            title='Muffin', amount=1, description='Gradane', cost=20, seller=self.userB)
        Product.objects.create(
            title='Rambo', amount=2, description='Labrador', cost=30, seller=self.userB)

    def test_product_breed(self):
        user = self.userA
        client.force_authenticate(user=user)

        product_casper = Product.objects.get(title='Casper')
        product_muffin = Product.objects.get(title='Muffin')
        self.assertEqual(
            product_casper.get_product(), "Casper belongs to Bull Dog")
        self.assertEqual(
            product_muffin.get_product(), "Muffin belongs to Gradane")


class GetAllProductsTest(TestCase):
    """ Test module for GET all Products API """

    def setUp(self):
        self.userA = User.objects.create_user('foo', password='bar')
        self.userA.is_superuser = True
        self.userA.is_staff = True
        self.userA.save()

        self.userB = User.objects.create_user('gogo', password='bar')
        self.userB.is_superuser = True
        self.userB.is_staff = True
        self.userB.save()

        UserProfile.objects.create(
            user=self.userA, user_type='1', deposite=5, bio='this is the dummy bio here', sorting=0)
        UserProfile.objects.create(
            user=self.userB, user_type='1', deposite=5, bio='this is the dummy bio here', sorting=0)

        Product.objects.create(
            title='Casper', amount=3, description='Bull Dog', cost=10, seller=self.userA,  sorting=0)
        Product.objects.create(
            title='Muffin', amount=1, description='Gradane', cost=20, seller=self.userA,  sorting=0)
        Product.objects.create(
            title='Rambo', amount=2, description='Labrador', cost=30, seller=self.userB,  sorting=0)
        Product.objects.create(
            title='Ricky', amount=6, description='Labrador', cost=10, seller=self.userB,  sorting=0)

    def test_get_all_products(self):
        user = self.userA
        client.force_authenticate(user=user)
        # get API response
        response = client.get(reverse('get_all_products'))
        # get data from db
        products = Product.objects.all()
        serializer = ProductsSerializer(products, many=True)
        self.assertEqual(response.data['context'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleProductTest(TestCase):
    """ Test module for GET single product API """

    def setUp(self):
        self.userA = User.objects.create_user('gogo', password='bar')
        self.userA.is_superuser = True
        self.userA.is_staff = True
        self.userA.save()

        UserProfile.objects.create(
            user=self.userA, user_type='1', deposite=5, bio='this is the dummy bio here', sorting=0)

        self.casper = Product.objects.create(
            title='Casper', amount=3, description='Bull Dog', cost=10, seller=self.userA)
        self.muffin = Product.objects.create(
            title='Muffin', amount=1, description='Gradane', cost=20, seller=self.userA)
        self.rambo = Product.objects.create(
            title='Rambo', amount=2, description='Labrador', cost=30, seller=self.userA)
        self.ricky = Product.objects.create(
            title='Ricky', amount=6, description='Labrador', cost=10, seller=self.userA)

    def test_get_valid_single_product(self):
        user = self.userA
        client.force_authenticate(user=user)

        response = client.get(
            reverse('get_single_product', kwargs={'id': self.rambo.pk}))
        product = Product.objects.get(pk=self.rambo.pk)
        serializer = ProductsSerializer(product)
        self.assertEqual(response.data['context'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_product(self):
        user = self.userA
        client.force_authenticate(user=user)
        response = client.get(
            reverse('get_single_product', kwargs={'id': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewProductTest(TestCase):
    """ Test module for inserting a new product """

    def setUp(self):
        self.userA = User.objects.create_user('foofoo', password='foofoo')
        self.userA.is_superuser = True
        self.userA.is_staff = True
        self.userA.save()

        UserProfile.objects.create(
            user=self.userA, user_type='1', deposite=5, bio='this is the dummy bio here', sorting=0)

        self.userB = User.objects.create_user('gogogogo', password='gogo')
        self.userB.is_superuser = True
        self.userB.is_staff = True
        self.userB.save()

        UserProfile.objects.create(
            user=self.userB, user_type='2', deposite=5, bio='this is the dummy bio here', sorting=0)

        self.valid_payload = {
            'title': 'Muffin',
            'description': 'Pamerion',
            'amount': 4,
            'cost': 4,
        }
        self.invalid_payload = {
            'title': 'Car',
            'description': 'Pamerion',
            'amount': 4,
            'cost': 4,
        }

    def test_create_valid_product(self):
        user = self.userB
        client.force_authenticate(user=user)
        response = client.post(
            reverse('create_new_product'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_product(self):
        user = self.userA
        client.force_authenticate(user=user)

        response = client.post(
            reverse('create_new_product'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UpdateSingleProductTest(TestCase):
    """ Test module for updating an existing product record """

    def setUp(self):
        self.userA = User.objects.create_user('foofoo', password='foofoo')
        self.userA.is_superuser = True
        self.userA.is_staff = True
        self.userA.save()
        UserProfile.objects.create(
            user=self.userA, user_type='2', deposite=5, bio='this is the dummy bio here', sorting=0)

        self.userB = User.objects.create_user('gogogogo', password='gogo')
        self.userB.is_superuser = True
        self.userB.is_staff = True
        self.userB.save()
        UserProfile.objects.create(
            user=self.userB, user_type='2', deposite=5, bio='this is the dummy bio here', sorting=0)

        self.casper = Product.objects.create(
            title='Casper', amount=3, description='Bull Dog', cost=10, seller=self.userA, sorting=0)
        self.muffin = Product.objects.create(
            title='Muffin', amount=1, description='Gradane', cost=20, seller=self.userB, sorting=0)
        self.valid_payload = {
            'title': 'Casper111',
            'description': 'Pamerion',
            'amount': 4,
            'cost': 4,
            'sorting': 5
        }
        self.invalid_payload = {
            'title': 'Muffin',
            'description': 'Pamerion',
            'amount': 4,
            'cost': 4,
            'sorting': 5
        }

    def test_valid_update_product(self):
        user = self.userA
        client.force_authenticate(user=user)

        response = client.put(
            reverse('edit_delete_product', kwargs={'id': self.casper.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_invalid_update_product(self):
        user = self.userB
        client.force_authenticate(user=user)

        response = client.put(
            reverse('edit_delete_product', kwargs={'id': 30}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class DeleteSingleProductTest(TestCase):
    """ Test module for deleting an existing product record """

    def setUp(self):
        self.userA = User.objects.create_user('foofoo', password='foofoo')
        self.userA.is_superuser = True
        self.userA.is_staff = True
        self.userA.save()
        UserProfile.objects.create(
            user=self.userA, user_type='2', deposite=5, bio='this is the dummy bio here', sorting=0)

        self.casper = Product.objects.create(
            title='Casper', amount=3, description='Bull Dog', cost=10, seller=self.userA,  sorting=0)

    def test_valid_delete_product(self):
        user = self.userA
        client.force_authenticate(user=user)

        response = client.delete(
            reverse('edit_delete_product', kwargs={'id': self.casper.pk}), )
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_invalid_delete_product(self):
        user = self.userA
        client.force_authenticate(user=user)

        response = client.delete(
            reverse('edit_delete_product', kwargs={'id': 30}), )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class BuyProductTest(TestCase):
    """ Test module for updating an existing product record """

    def setUp(self):
        self.userA = User.objects.create_user('foofoo', password='foofoo')
        self.userA.is_superuser = True
        self.userA.is_staff = True
        self.userA.save()
        UserProfile.objects.create(
            user=self.userA, user_type='2', deposite=350000, bio='this is the dummy bio here', sorting=0)

        self.userB = User.objects.create_user('gogogogo', password='gogo')
        self.userB.is_superuser = True
        self.userB.is_staff = True
        self.userB.save()
        UserProfile.objects.create(
            user=self.userB, user_type='2', deposite=5, bio='this is the dummy bio here', sorting=0)

        self.casper = Product.objects.create(
            title='Casper',  description='Bull Dog', amount=30, cost=10, seller=self.userA,  sorting=0)
        self.muffin = Product.objects.create(
            title='Muffin', description='Gradane', amount=100, cost=20, seller=self.userB,  sorting=0)

    def test_valid_buy_product(self):
        user = self.userA
        client.force_authenticate(user=user)

        response = client.put(
            reverse('buy_product', kwargs={
                    'id': self.casper.pk, 'amount': 10}),
            data={},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_invalid_buy_product(self):
        user = self.userB
        client.force_authenticate(user=user)

        response = client.put(
            reverse('buy_product', kwargs={
                    'id': self.muffin.pk, 'amount': 10000}),
            data={},
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
