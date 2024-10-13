from django.urls import path
from ecommerce.ecommerce_api.views import ProductsApiView

app_name = 'ecommerce'

urlpatterns = [
    path('products/', ProductsApiView,name="ecommerce-api-products"),
]