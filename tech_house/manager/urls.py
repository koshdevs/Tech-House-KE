from django.urls import path
from . import views
from .views import store_counter,add_to_counter,remove_from_counter,gen_store_invoices,\
    customer_invoice_details,list_invoices,filter_orders,filter_products,\
        store_complete_order,store_process_delivery,store_generate_d_notes,gen_instant_receipt,\
            complete_instant_sales,store_generate_reports,remove_order_from_invoice,\
                list_invoice_items,gen_invoice_for_selected_items,gen_receipt_for_selected_items,\
                    rem_selected_items_from_orders,store_list_customer_details,list_on_sales_items,\
                        filter_on_sales_items,sales_as_delivered,sales_as_returned,sales_as_invoiced,file_transfer


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
    path('complete-instant-sales/', complete_instant_sales, name="manager-complete-instant-sales"),
    path('store-generate-reports/', store_generate_reports, name="manager-store-generate-reports"),
    path('remove-order-from-invoice/<str:order_id>/', remove_order_from_invoice, name="manager-remove-order-from-invoice"),
    path('list-invoice-items/<str:order_id>/', list_invoice_items, name="manager-list-invoice-items"),
    path('list-on-sales-items/',list_on_sales_items, name="manager-list-on-sales-items"),
    path('filter-on-sales-items',filter_on_sales_items, name="manager-filter-on-sales-items"),
    path('gen-invoice-for-selected-items/', gen_invoice_for_selected_items, name="manager-gen-invoice-for-selected-items"),
    path('gen-receipt-for-selected-items/', gen_receipt_for_selected_items, name="manager-gen-receipt-for-selected-items"),
    path('rem-selected-items-from-orders/', rem_selected_items_from_orders, name="manager-rem-selected-items-from-orders"),
    path('store-list-customer-details/<str:order_id>/', store_list_customer_details, name="manager-store-list-customer-details"),
    
    path('sales-as-delivered/', sales_as_delivered, name="manager-sales-as-delivered"),
    path('sales-as-return/', sales_as_returned, name="manager-sales-as-return"),
    path('sales-as-invoiced/', sales_as_invoiced, name="manager-sales-as-invoiced"),
    
    path('file-transfer/', file_transfer, name="manager-file-transfer"),
    
]
