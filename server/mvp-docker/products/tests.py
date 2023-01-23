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

# initialize the APIClient app
client = APIClient()
user = User.objects.get(username='samer1alkhatib2_734')
token = token = Token.objects.get(user__username='samer1alkhatib2_734')
headers = {
    "Content-Type": "application/json",
    'Authorization': 'Bearer ' + str(token)
}

user = User.objects.all()[2]
client = APIClient()
client.force_authenticate(user=user)


# class ProductTest(TestCase):
#     """ Test module for product model """

#     def setUp(self):
#         userA = User.objects.create_user('foo', password='bar')
#         userA.is_superuser = True
#         userA.is_staff = True
#         userA.save()

#         userB = User.objects.create_user('gogo', password='bar')
#         userB.is_superuser = True
#         userB.is_staff = True
#         userB.save()

#         UserProfile.objects.create(
#             user=userA, user_type='1', deposite=5, bio='this is the dummy bio here', sorting=0)
#         UserProfile.objects.create(
#             user=userB, user_type='1', deposite=5, bio='this is the dummy bio here', sorting=0)

#         Product.objects.create(
#             title='Casper', amount=3, description='Bull Dog', cost=10, seller=userA)
#         Product.objects.create(
#             title='Muffin', amount=1, description='Gradane', cost=20, seller=userB)
#         Product.objects.create(
#             title='Rambo', amount=2, description='Labrador', cost=30, seller=userB)

#     def test_product_breed(self):
#         product_casper = Product.objects.get(title='Casper')
#         product_muffin = Product.objects.get(title='Muffin')
#         self.assertEqual(
#             product_casper.get_product(), "Casper belongs to Bull Dog.")
#         self.assertEqual(
#             product_muffin.get_product(), "Muffin belongs to Gradane.")


# class GetAllProductsTest(TestCase):
#     """ Test module for GET all Products API """


# def setUp(self):
#     userA = User.objects.create_user('foo', password='bar')
#     userA.is_superuser = True
#     userA.is_staff = True
#     userA.save()

#     userB = User.objects.create_user('gogo', password='bar')
#     userB.is_superuser = True
#     userB.is_staff = True
#     userB.save()

#     UserProfile.objects.create(
#         user=userA, user_type='1', deposite=5, bio='this is the dummy bio here', sorting=0)
#     UserProfile.objects.create(
#         user=userB, user_type='1', deposite=5, bio='this is the dummy bio here', sorting=0)

#     Product.objects.create(
#         title='Casper', amount=3, description='Bull Dog', cost=10, seller=userA,  sorting=0)
#     Product.objects.create(
#         title='Muffin', amount=1, description='Gradane', cost=20, seller=userA,  sorting=0)
#     Product.objects.create(
#         title='Rambo', amount=2, description='Labrador', cost=30, seller=userB,  sorting=0)
#     Product.objects.create(
#         title='Ricky', amount=6, description='Labrador', cost=10, seller=userB,  sorting=0)


# def test_get_all_products(self):
#     # get API response
#     response = client.get(reverse('get_all_products'))
#     # get data from db
#     products = Product.objects.all()
#     serializer = ProductsSerializer(products, many=True)
#     self.assertEqual(response.data, serializer.data)
#     self.assertEqual(response.status_code, status.HTTP_200_OK)


# class GetSingleProductTest(TestCase):
#     """ Test module for GET single product API """

#     def setUp(self):
#         userB = User.objects.create_user('gogo', password='bar')
#         userB.is_superuser = True
#         userB.is_staff = True
#         userB.save()

#         UserProfile.objects.create(
#             user=userB, user_type='1', deposite=5, bio='this is the dummy bio here', sorting=0)

#         self.casper = Product.objects.create(
#             title='Casper', amount=3, description='Bull Dog', cost=10, seller=userB)
#         self.muffin = Product.objects.create(
#             title='Muffin', amount=1, description='Gradane', cost=20, seller=userB)
#         self.rambo = Product.objects.create(
#             title='Rambo', amount=2, description='Labrador', cost=30, seller=userB)
#         self.ricky = Product.objects.create(
#             title='Ricky', amount=6, description='Labrador', cost=10, seller=userB)

#     def test_get_valid_single_product(self):
#         response = client.get(
#             reverse('get_single_product', kwargs={'id': self.casper.pk}))
#         product = Product.objects.get(pk=self.rambo.pk)
#         serializer = ProductsSerializer(product)
#         self.assertEqual(response.data, serializer.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_get_invalid_single_product(self):
#         response = client.get(
#             reverse('get_single_product', kwargs={'id': 30}))
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# class CreateNewProductTest(TestCase):
#     """ Test module for inserting a new product """

#     def setUp(self):
#         userB = User.objects.create_user('gogo', password='bar')
#         userB.is_superuser = True
#         userB.is_staff = True
#         userB.save()

#         UserProfile.objects.create(
#             user=userB, user_type='1', deposite=5, bio='this is the dummy bio here', sorting=0)

#         self.valid_payload = {
#             'title': 'Muffin',
#             'description': 'Pamerion',
#             'amount': 4,
#             'cost': 4,
#             'seller': userB
#         }
#         self.invalid_payload = {
#             'title': '',
#             'description': 'Pamerion',
#             'amount': 4,
#             'cost': 4,
#             'category': '3'
#         }

#     def test_create_valid_product(self):
#         response = client.post(
#             reverse('create_new_product'),
#             data=json.dumps(self.valid_payload),
#             headers=headers,
#             content_type='application/json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_create_invalid_product(self):
#         response = client.post(
#             reverse('create_new_product'),
#             data=json.dumps(self.invalid_payload),
#             headers=headers,
#             content_type='application/json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# class UpdateSingleProductTest(TestCase):
#     """ Test module for updating an existing product record """

#     def setUp(self):
#         userB = User.objects.filter(id=4).first()
#         category = Page.objects.filter(publisher_public_id=3).first()

#         self.casper = Product.objects.create(
#             title='Casper', amount=3, description='Bull Dog', cost=10, seller=userB, category=category, sorting=0)
#         self.muffin = Product.objects.create(
#             title='Muffin', amount=1, description='Gradane', cost=20, seller=userB, category=category, sorting=0)
#         self.valid_payload = {
#             'title': 'Casper',
#             'description': 'Pamerion',
#             'amount': 4,
#             'cost': 4,
#             'category': category,
#             'seller': userB,
#             'sorting': 5
#         }
#         self.invalid_payload = {
#             'title': '',
#             'description': 'Pamerion',
#             'amount': 4,
#             'cost': 4,
#             'category': '3'
#         }

#     def test_valid_update_product(self):
#         response = client.put(
#             reverse('edit_delete_product', kwargs={'id': self.muffin.pk}),
#             data=json.dumps(self.valid_payload),
#             headers=headers,
#             content_type='application/json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

#     def test_invalid_update_product(self):
#         response = client.put(
#             reverse('edit_delete_product', kwargs={'id': self.muffin.pk}),
#             data=json.dumps(self.invalid_payload),
#             headers=headers,
#             content_type='application/json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# class DeleteSingleProductTest(TestCase):
#     """ Test module for deleting an existing product record """

#     def setUp(self):
#         userB = User.objects.filter(id=4).first()
#         category = Page.objects.filter(publisher_public_id=3).first()

#         self.casper = Product.objects.create(
#             title='Casper', amount=3, description='Bull Dog', cost=10, seller=userB, category=category, sorting=0)
#         self.muffin = Product.objects.create(
#             title='Muffin', amount=1, description='Gradane', cost=20, seller=userB, category=category, sorting=0)

#     def test_valid_delete_product(self):
#         response = client.delete(
#             reverse('edit_delete_product', kwargs={'id': self.muffin.pk}), headers=headers,)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

#     def test_invalid_delete_product(self):
#         response = client.delete(
#             reverse('edit_delete_product', kwargs={'id': 30}), headers=headers,)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# class BuyProductTest(TestCase):
#     """ Test module for updating an existing product record """

#     def setUp(self):
#         userB = User.objects.filter(id=4).first()
#         category = Page.objects.filter(publisher_public_id=3).first()

#         self.casper = Product.objects.create(
#             title='Casper', amount=30, description='Bull Dog', cost=10, seller=userB, category=category, sorting=0)
#         self.muffin = Product.objects.create(
#             title='Muffin', amount=100, description='Gradane', cost=20, seller=userB, category=category, sorting=0)
#         self.valid_payload = {
#             'amount': 4,
#             'category': category,
#             'seller': userB,
#         }
#         self.invalid_payload = {
#             'amount': 4,
#             'cost': 4,
#             'category': '3',
#             'seller': userB,
#         }

#     def test_valid_buy_product(self):
#         response = client.put(
#             reverse('buy_product', kwargs={
#                     'id': self.muffin.pk, 'amount': self.muffin.amount}),
#             data=json.dumps(self.valid_payload),
#             headers=headers,
#             content_type='application/json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

#     def test_invalid_buy_product(self):
#         response = client.put(
#             reverse('buy_product', kwargs={
#                     'id': self.muffin.pk, 'amount': 10000}),
#             data=json.dumps(self.invalid_payload),
#             headers=headers,
#             content_type='application/json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
