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