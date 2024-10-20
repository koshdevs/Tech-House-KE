from django.urls import path
from . import views
from .views import shop_view,shop_details_view,shop_add_to_cart_view

urlpatterns = [
    
             path('',views.shop_view,name='eco-shop'),
             path('shop-details/<int:pk>/',views.shop_details_view,name="eco-shop-details"),
             path('add-to-cart/<int:pk>/', views.shop_add_to_cart_view, name="eco-shop-add-to-cart")
]
