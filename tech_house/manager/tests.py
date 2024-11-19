from django.test import TestCase, Client
from unittest.mock import patch, MagicMock
from django.test import Client, RequestFactory
from django.urls import reverse
from tech_house.manager.views import store_counter
from ecommerce.models import ProductBuild  
from .models import *
from .views import *

class TestStoreCounterView(TestCase):
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
        
class TestRemoveFromCounterView(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = StoreSales.objects.create()

    def test_product_removed_from_cart(self):
        response = self.client.get(reverse('remove_from_counter', args=[self.product.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(StoreSales.objects.filter(pk=self.product.pk).exists())

    def test_product_not_found_in_cart(self):
        response = self.client.get(reverse('remove_from_counter', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_invalid_product_id(self):
        response = self.client.get(reverse('remove_from_counter', args=['abc']))
        self.assertEqual(response.status_code, 404)

    def test_request_method_is_get(self):
        response = self.client.post(reverse('remove_from_counter', args=[self.product.pk]))
        self.assertEqual(response.status_code, 405)

    def test_template_rendered_correctly(self):
        response = self.client.get(reverse('remove_from_counter', args=[self.product.pk]))
        self.assertEqual(response.template_name, 'manager/shop-counter-change.html')

    def test_context_passed_to_template_correctly(self):
        response = self.client.get(reverse('remove_from_counter', args=[self.product.pk]))
        self.assertIn('sales', response.context)
        self.assertIn('totals', response.context)
        
        
class TestGenInstantReceipt(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

    def test_render_template(self):
        response = self.client.get('/instant_receipt_url/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manager/store-receipt.html')

    @patch('tech_house.manager.views.get_sales_by_status')
    def test_get_sales_by_status_called(self, mock_get_sales_by_status):
        self.client.get('/instant_receipt_url/')
        mock_get_sales_by_status.assert_called_once_with('cart')

    def test_invalid_request(self):
        request = MagicMock()
        del request.method
        with self.assertRaises(AttributeError):
            gen_instant_receipt(request)

    @patch('tech_house.manager.views.get_sales_by_status')
    def test_exception_handling(self, mock_get_sales_by_status):
        mock_get_sales_by_status.side_effect = Exception('Test exception')
        response = self.client.get('/instant_receipt_url/')
        self.assertEqual(response.status_code, 500)