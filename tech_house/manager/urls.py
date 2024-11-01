from django.urls import path
from . import views
from .views import store_counter,add_to_counter,remove_from_counter,gen_store_invoices,\
    customer_invoice_details,list_invoices


urlpatterns = [
    
    path('store-counter/', store_counter,name="manager-store-counter"),
    path('add-to-counter/<int:pk>/', add_to_counter,name="manager-add-to-counter"),
    path('remove-from-counter/<int:pk>/', remove_from_counter,name="manager-remove-from-counter"),
    path('generate-store-invoices/<str:order_id>/', gen_store_invoices, name="manager-generate-store-invoices"),
    path('customer-invoice-details/', customer_invoice_details, name="manager-customer-invoice-details"),
    path('list-invoice/', list_invoices, name="manager-list-invoices"),
    
]
