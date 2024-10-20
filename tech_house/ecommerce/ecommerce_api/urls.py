from django.urls import path
from ecommerce.ecommerce_api.views import ProductsApiView,ProductsDetailsApiView

app_name = 'ecommerce'

urlpatterns = [
    path('products/', ProductsApiView,name="ecommerce-api-products"),
    path('products/<int:pk>/', ProductsDetailsApiView,name="ecommerce-api-products-details")
]