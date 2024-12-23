from django.urls import path
from . import views
from .views import shop_view,shop_details_view,shop_add_to_cart_view,\
    shop_minus_to_cart_view,shop_cart_view,shop_rem_cart_view,filter_products_by_brand,\
    filter_by_sub_category,filter_by_price_range,search_products,sort_products

urlpatterns = [
    
             path('',views.shop_view,name='eco-shop'),
             path('shop-details/<int:pk>/',views.shop_details_view,name="eco-shop-details"),
             path('add-to-cart/<int:pk>/', views.shop_add_to_cart_view, name="eco-shop-add-to-cart"),
             path('minus-to-cart/<int:pk>/', views.shop_minus_to_cart_view, name="eco-shop-minus-to-cart"),
             path('cart/', views.shop_cart_view, name="eco-shop-cart"),
             path('remove-from-cart/<int:pk>/', views.shop_rem_cart_view, name="eco-shop-remove-cart"),
             path('filter-products-by-brand/<int:brand_id>/', views.filter_products_by_brand, name="eco-shop-filter-by-brand"),
             path('filter-products-by-sub-category/<int:sub_category_id>/', views.filter_by_sub_category, name="eco-shop-filter-by-sub-category"),
             path('filter-products-by-price-range/', views.filter_by_price_range, name="eco-shop-filter-by-price-range"),
             path('sort-products', views.sort_products, name="eco-shop-sort-products"),
             path('search-products/', views.search_products, name="eco-shop-search-products"),
]

