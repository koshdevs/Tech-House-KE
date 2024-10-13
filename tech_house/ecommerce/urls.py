from django.urls import path
from . import views
from .views import shop_view

urlpatterns = [
    
             path('',views.shop_view,name='eco-shop'),
]
