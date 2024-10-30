import unittest
from django.test import Client
from django.urls import reverse
from tech_house.manager.views import store_counter
from ecommerce.models import ProductBuild

class TestStoreCounterView(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('store_counter')

    def test_view_returns_http_response(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.templates[0].name, 'manager/store_sales.html')

    def test_view_passes_correct_context(self):
        response = self.client.get(self.url)
        self.assertIn('items', response.context)
        self.assertIsInstance(response.context['items'], ProductBuild.objects.none().__class__)

    def test_view_handles_empty_queryset(self):
        ProductBuild.objects.all().delete()
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['items']), 0)
        
        
class TestAddToCounterView(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = ProductBuild.objects.create(
            serial1='test_serial',
            price=10.99,
            status='in-stock'
        )

    def test_product_exists(self):
        response = self.client.get(reverse('add_to_counter', args=[self.product.pk]))
        self.assertEqual(response.status_code, 200)

    def test_product_added_to_sales(self):
        self.client.get(reverse('add_to_counter', args=[self.product.pk]))
        sales = StoreSales.objects.all()
        self.assertEqual(len(sales), 1)
        self.assertEqual(sales[0].product, self.product)

    def test_product_status_updated(self):
        self.client.get(reverse('add_to_counter', args=[self.product.pk]))
        product_by_serial = ProductBuild.objects.get(serial1=self.product.serial1)
        self.assertEqual(product_by_serial.status, 'sold')

    def test_sales_retrieved(self):
        self.client.get(reverse('add_to_counter', args=[self.product.pk]))
        sales = StoreSales.objects.all()
        self.assertEqual(len(sales), 1)

    def test_context_rendered(self):
        response = self.client.get(reverse('add_to_counter', args=[self.product.pk]))
        self.assertEqual(response.templates[0].name, 'manager/add_to_counter.html')
        self.assertEqual(response.context['product'], self.product)
        self.assertEqual(response.context['sales'], StoreSales.objects.all())