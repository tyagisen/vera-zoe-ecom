from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from products.models import Category, Brand, Product, ProductVariant


class ProductAPITestCase(APITestCase):
    def setUp(self):
        pass