from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

from startapp.models import Category, Product, Order


class OrderAPITests(APITestCase):
    def setUp(self):
        self.ali = User.objects.create_user(username='ali', password='Ali12345!')
        self.vali = User.objects.create_user(username='vali', password='Vali12345!')
        self.admin = User.objects.create_user(
            username='boss', password='Boss12345!', is_staff=True
        )
        category = Category.objects.create(name='Telefonlar')
        self.product = Product.objects.create(
            name='Phone', price=1000, category=category
        )
        self.inactive = Product.objects.create(
            name='Old', price=500, is_active=False, category=category
        )
        self.url = '/api/orders/'

    def test_anonymous_cannot_see_orders(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_empty_items_rejected(self):
        self.client.force_authenticate(self.ali)
        response = self.client.post(self.url, {'items': []}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_zero_quantity_rejected(self):
        self.client.force_authenticate(self.ali)
        data = {'items': [{'product': self.product.id, 'quantity': 0}]}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_inactive_product_rejected(self):
        self.client.force_authenticate(self.ali)
        data = {'items': [{'product': self.inactive.id, 'quantity': 1}]}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_calculates_total(self):
        self.client.force_authenticate(self.ali)
        data = {'items': [{'product': self.product.id, 'quantity': 2}]}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['total_price'], 2000)
        self.assertEqual(response.data['user'], self.ali.id)

    def test_user_sees_only_own_orders(self):
        self.client.force_authenticate(self.ali)
        data = {'items': [{'product': self.product.id, 'quantity': 1}]}
        self.client.post(self.url, data, format='json')

        self.client.force_authenticate(self.vali)
        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], 0)

    def test_other_users_order_returns_404(self):
        self.client.force_authenticate(self.ali)
        data = {'items': [{'product': self.product.id, 'quantity': 1}]}
        order_id = self.client.post(self.url, data, format='json').data['id']

        self.client.force_authenticate(self.vali)
        response = self.client.get(f'{self.url}{order_id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_staff_sees_all_orders(self):
        self.client.force_authenticate(self.ali)
        data = {'items': [{'product': self.product.id, 'quantity': 1}]}
        self.client.post(self.url, data, format='json')

        self.client.force_authenticate(self.admin)
        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], 1)