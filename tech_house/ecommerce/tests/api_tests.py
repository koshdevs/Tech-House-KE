import unittest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class TestProductsApiView(APITestCase):
    
    url = '/ecommerce/ecommerce_api/products/'
    def test_get_request(self):
       
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'products': ""})

    def test_post_request(self):
        
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_put_request(self):
        
        response = self.client.put(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_request(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        

import unittest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ecommerce.models import ProductBuild

class ProductsDetailsApiViewTest(APITestCase):
    def setUp(self):
        self.product = ProductBuild.objects.create(
            serial1='serial1',
            category_id=1,
            brand_id=1,
            model_id=1,
            origin_id=1,
            cost=10.99,
            price=12.99,
            status='in-stock',
            overview='Product overview'
        )

    def test_get_product_details_valid_id(self):
        url = reverse('products-details', kwargs={'pk': self.product.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['serial1'], self.product.serial1)

    def test_get_product_details_invalid_id(self):
        url = reverse('products-details', kwargs={'pk': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_product_details_serialized_data(self):
        url = reverse('products-details', kwargs={'pk': self.product.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('serial1', response.data)
        self.assertIn('category', response.data)
        self.assertIn('brand', response.data)
        self.assertIn('model', response.data)
        self.assertIn('origin', response.data)
        self.assertIn('cost', response.data)
        self.assertIn('price', response.data)
        self.assertIn('status', response.data)
        self.assertIn('overview', response.data)