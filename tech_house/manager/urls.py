from django.urls import path
from . import views
from .views import store_counter


urlpatterns = [
    
    path('store-counter/', store_counter,name="manager-store-counter"),
    
]
