from django.urls import path
from . import views
from .views import store_counter,add_to_counter,remove_from_counter,gen_store_invoices,\
    customer_invoice_details,list_invoices,filter_orders,filter_products,\
        store_complete_order,store_process_delivery,store_generate_d_notes,gen_instant_receipt


urlpatterns = [
    
    path('store-counter/', store_counter,name="manager-store-counter"),
    path('add-to-counter/<int:pk>/', add_to_counter,name="manager-add-to-counter"),
    path('remove-from-counter/<int:pk>/', remove_from_counter,name="manager-remove-from-counter"),
    path('generate-store-invoices/<str:order_id>/', gen_store_invoices, name="manager-generate-store-invoices"),
    path('customer-invoice-details/', customer_invoice_details, name="manager-customer-invoice-details"),
    path('list-invoice/', list_invoices, name="manager-list-invoices"),
    path('filter-orders/', filter_orders, name="manager-filter-orders"),
    path('filter-products/', filter_products, name="manager-filter-products"),
    path('store-complete-order/<str:order_id>/', store_complete_order, name="manager-store-complete-order"),
    path('store-processing-delivery/',store_process_delivery, name="manager-store-process-delivery"),
    path('store-generate-d-notes/<str:order_id>/', store_generate_d_notes, name="manager-store-generate-d-notes"),
    path('gen-instant-receipt/', gen_instant_receipt, name="manager-gen-instant-receipt"),
    
]
