from django.test import TestCase, Client
from django.http import HttpResponse
from django.urls import reverse
from ecommerce.views import shop_view

class TestShopView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_returns_httpresponse(self):
        response = self.client.get(reverse('eco-shop'))
        self.assertIsInstance(response, HttpResponse)

    def test_renders_correct_template(self):
        response = self.client.get(reverse('eco-shop'))
        self.assertTemplateUsed(response, 'ecommerce/shop.html')

    def test_handles_get_request(self):
        response = self.client.get(reverse('eco-shop'))
        self.assertEqual(response.status_code, 200)

    def test_handles_post_request(self):
        response = self.client.post(reverse('eco-shop'))
        self.assertEqual(response.status_code, 200)