from django.urls import path
from . import views
from .views import store_counter,add_to_counter


urlpatterns = [
    
    path('store-counter/', store_counter,name="manager-store-counter"),
    path('add-to-counter/<int:pk>/', add_to_counter,name="manager-add-to-counter"),	
    
]
