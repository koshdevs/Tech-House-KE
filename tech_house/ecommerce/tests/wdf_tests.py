from django.test import TestCase, Client
from django.http import HttpResponse
from django.urls import reverse
from ecommerce.views import shop_view
from ecommerce.models import ProductBuild

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
        
class ShopDetailsViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.product = ProductBuild.objects.create(
            # create a product instance with required fields
            model='Test Product',
            brand='Test Brand',
            price=100.00,
            # add other required fields here
        )

    def test_function_returns_httpresponse(self):
        response = self.client.get(reverse('eco-shop-details', args=[self.product.pk]))
        self.assertIsInstance(response, HttpResponse)

    def test_function_raises_http404_error(self):
        response = self.client.get(reverse('eco-shop-details', args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_function_renders_correct_template(self):
        response = self.client.get(reverse('eco-shop-details', args=[self.product.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ecommerce/shop-details.html')

    def test_function_passes_correct_context(self):
        response = self.client.get(reverse('eco-shop-details', args=[self.product.pk]))
        self.assertEqual(response.context['product'], self.product)
        
        

class TestShopAddToCartView(TestCase):

    def setUp(self):
        self.client = Client()
        self.product = ProductBuild.objects.create(name='Test Product', price=10.99)

    def test_returns_http_response(self):
        response = self.client.get(reverse('eco-shop-add-to-cart', args=[self.product.pk]))
        self.assertEqual(response.status_code, 200)

    def test_raises_404_error(self):
        response = self.client.get(reverse('eco-shop-add-to-cart', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_adds_product_to_cart(self):
        self.client.get(reverse('eco-shop-add-to-cart', args=[self.product.pk]))
        response = self.client.get(reverse('eco-shop-add-to-cart', args=[self.product.pk]))
        self.assertContains(response, '1')

    def test_displays_correct_number_of_items(self):
        self.client.get(reverse('eco-shop-add-to-cart', args=[self.product.pk]))
        response = self.client.get(reverse('eco-shop-add-to-cart', args=[self.product.pk]))
        self.assertContains(response, '1')

    def test_renders_correct_template(self):
        response = self.client.get(reverse('eco-shop-add-to-cart', args=[self.product.pk]))
        
        
class ShopMinusToCartViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = ProductBuild.objects.create(name='Test Product', price=10.99)

    def test_decrease_quantity(self):
        # Add product to cart
        response = self.client.get(reverse('shop_add_to_cart', args=[self.product.pk]))
        self.assertEqual(response.status_code, 200)

        # Decrease quantity
        response = self.client.get(reverse('shop_minus_to_cart', args=[self.product.pk]))
        self.assertEqual(response.status_code, 200)

        # Check cart quantity
        response = self.client.get(reverse('shop_add_to_cart', args=[self.product.pk]))
        self.assertContains(response, 'Quantity: 0')

    def test_rendered_template(self):
        response = self.client.get(reverse('shop_minus_to_cart', args=[self.product.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ecommerce/shop-add-to-cart.html')

    def test_product_not_found(self):
        response = self.client.get(reverse('shop_minus_to_cart', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_invalid_product_id(self):
        response = self.client.get(reverse('shop_minus_to_cart', args=['abc']))
        self.assertEqual(response.status_code, 404)