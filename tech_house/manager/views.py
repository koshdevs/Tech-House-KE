from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.db.models import Q
from ecommerce.models import ProductBuild 
from .models import StoreSales,CustomerDetails,StoreOrders,OrgDetails,DeliveryDetails
from.sales_ops import get_sales_data,gen_order_docs,get_sales_by_status
import datetime

# Create your views here.


def store_counter(request):
    
    

    """
    The store counter view is the main view for the store counter,
    it shows all the products in the store and their quantities.
    The view also shows the total of all the products in the store
    and the total of all the products in the cart.
    """
    

    items = ProductBuild.objects.filter(stage="in-stock")
    
    sales,totals = get_sales_data('cart')
    
    
    contxt = {"items":items,"sales":sales,"totals":totals}
    
    return render(request, 'manager/store_sales.html',contxt)

@login_required
def add_to_counter(request,pk): 
    

    """
    Adds a product with id :pk: to the store counter cart.

    :param request: The request object.
    :type request: django.http.HttpRequest
    :param pk: The id of the product to add to the cart.
    :type pk: int
    :return: The rendered shop-counter-change.html template with updated cart items and a message.
    :rtype: django.http.HttpResponse
    """

    product = ProductBuild.objects.get(pk=pk)
    
    sales_check = StoreSales.objects.filter(product__serial1=product.serial1,status='cart')
    
    msg = '' 
    if len(sales_check) == 0:
    
        sales = StoreSales( 
                        
                        product=product,
                        quantity =1,
                        price = product.price,
                        created_by = request.user,
                        status = 'cart',
                        tax= product.tax,
                        
                        )
        
        sales.save()
        
        msg+='<strong style="color:green">Added to cart</strong>'	
    
    else: 
        
        msg+='<strong style="color:red">Item already Exists</strong>'
        
        
    
    product_by_serial = ProductBuild.objects.get(serial1=product.serial1)
    product_by_serial.status = 'sold'
    product_by_serial.save()
    
    sales,totals = get_sales_data('cart')
    
    print(msg)
    
    contxt = {"product":product,"sales":sales,"totals":totals,"msg":msg}	
    
    return render(request, 'manager/shop-counter-change.html',contxt)


def add_to_counter_non_scans(request,pk):
    
    pass

def remove_from_counter(request,pk): 
    
    """
    Removes a product with id :pk: from the store counter cart.

    :param request: The request object.
    :type request: django.http.HttpRequest
    :param pk: The id of the product to remove from the cart.
    :type pk: int
    :return: The rendered shop-counter-change.html template with updated cart items.
    :rtype: django.http.HttpResponse
    """

    sales = StoreSales.objects.get(pk=pk)
    
    sales.delete()
    
    sales,totals = get_sales_data('cart')
    
    contxt = {"sales":sales,"totals":totals}
    
    return render(request, 'manager/shop-counter-change.html',contxt)


def gen_instant_receipt(request): 
    
    contxt = get_sales_by_status('cart')
    
    
    return render(request, 'manager/store-receipt.html',contxt)

def complete_instant_sales(request): 
    

    """
    Completes all sales in the user's cart by updating their status to 'sold' and
    setting the sale date to the current date and time. Returns an HttpResponse
    with a success message if all sales are completed successfully, or an error
    message if an exception occurs.

    :param request: The request object containing the user information.
    :type request: django.http.HttpRequest
    :return: An HttpResponse object with a success or error message.
    :rtype: django.http.HttpResponse
    """

    resp = ""
    try:
    
        sales = StoreSales.objects.filter(status='cart',created_by=request.user)
        
        
        for sale in sales:
            
            sale.status = 'sold'
            sale.product.stage = "sold"
            
            sale.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            sale.save()
            sale.product.save()
        resp+=f"Completed successfully"
        
    except Exception as e: 
        
        resp = str(e)
            
    return JsonResponse(resp,safe=False)

def filter_products(request):
    
    
        

        """
        Filters products based on a scan query parameter. If the scan parameter is provided, it filters products
        whose serial number or model name contains the scan value. If the scan parameter is empty, it retrieves
        all products, but limits the result to 5 products if the total count exceeds 5.

        :param request: The HTTP request object.
        :type request: django.http.HttpRequest
        :return: The rendered shop-products-search-results.html template with filtered products.
        :rtype: django.http.HttpResponse
        """

        scan = request.GET.get('scan')
       
        
       
        
        if scan != "": 
            items = ProductBuild.objects.filter(Q(serial1__contains=scan) | Q(model__name__contains=scan))
            print(scan)
            
        elif scan=='': 
            
            items = ProductBuild.objects.all()
            
            if items.count() > 5: 
            
                items = ProductBuild.objects.all()[:5]
            
       

        
        contxt = {"items":items}
        
        return render(request, 'manager/shop-products-search-results.html',contxt)
            
       

    
   
def gen_store_invoices(request,order_id):
    

    """
    Generates a store invoice for a given order id. The function retrieves
    the relevant store orders and customer details, calculates the subtotal, tax and total,
    and renders the store-invoice.html template with the relevant data.

    :param order_id: The id of the order to generate the invoice for.
    :type order_id: str
    :return: The rendered store-invoice.html template with the invoice details.
    :rtype: django.http.HttpResponse
    """

    contxt = gen_order_docs(order_id)
    
    return render(request, 'manager/store-invoice.html',contxt)

@csrf_exempt
def customer_invoice_details(request):
    

    """
    Handles POST requests containing customer details and updates the relevant
    models, namely CustomerDetails and StoreOrders. The function also updates
    the status of the relevant StoreSales to 'invoiced' and saves the new StoreOrders
    instance. The function renders the shop-counter-change.html template with a
    success message and the updated sales and totals data.

    :param request: The request object.
    :type request: django.http.HttpRequest
    :return: The rendered shop-counter-change.html template with the updated data.
    :rtype: django.http.HttpResponse
    """
    if request.method == 'POST':
        
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        cname = request.POST.get('cname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        caddress = request.POST.get('caddress')
        terms = request.POST.get('terms')
        print(fname)
        orderid = request.POST.get('orderId') 
        
        
        customer_details = CustomerDetails( 
                                           
                                           name = fname+' '+lname,
                                           company_name = cname,
                                           email = email,
                                           phone = phone,
                                           address = caddress,
                                           terms = terms,
                                           order_id = orderid                            
                                           
                                           )
        
        customer_details.save()
        
        sales = StoreSales.objects.filter(status='cart')
        
        for sale in sales:
            
            sale.status = 'invoiced'
            sale.save()
            
            order = StoreOrders( 
                                           
                                           sales = sale,
                                           customer_details = customer_details,
                                           order_id = orderid
                                )
            
            order.save()
            
            
            
    
    resp = '<strong style="color:green">Details Saved successfully</strong>'
    
    sales,totals = get_sales_data('cart')
    
    contxt = {"sales":sales,"totals":totals,"resp":resp}
    
    return render(request, 'manager/shop-counter-change.html',contxt)


def list_invoices(request):
    
    
    """
    Retrieves and displays a list of all store orders.

    :param request: The request object.
    :type request: django.http.HttpRequest
    :return: The rendered shop-invoice-list.html template with all store orders.
    :rtype: django.http.HttpResponse
    """
    
   
    
   

    orders= StoreOrders.objects.raw("select * from manager_StoreOrders group by order_id")
        
    if len(orders)>10:
            
        orders = StoreOrders.objects.raw("select * from manager_StoreOrders group by order_id limit 10")
            
        
    
    contxt = {"orders":orders}
    
    return render(request, 'manager/shop-invoice-list.html',contxt)


def filter_orders(request):
    

    """
    Retrieves and displays a list of store orders based on a given invoice id and
    date range.

    :param request: The request object.
    :type request: django.http.HttpRequest
    :return: The rendered order_search_results.html template with the filtered store orders.
    :rtype: django.http.HttpResponse
    """

    if request.method == 'POST':
        
        invoice_id = request.POST.get('invoice_id')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        
     
        
        if invoice_id == '':	  
            
            orders = StoreOrders.objects.filter(date__range=[from_date, to_date])
        
        else:
            
            orders = StoreOrders.objects.raw(f"select * from manager_StoreOrders  where order_id = %s order by date desc",[invoice_id,])
            
        
        contxt = {"orders":orders}
        
        return render(request, 'manager/shop-orders-search-results.html',contxt) 
    
    
def store_complete_order(request, order_id): 
    
    
    """
    Marks all store orders with a given order id as 'sold' and retrieves and displays a list of all store orders.

    :param request: The request object.
    :type request: django.http.HttpRequest
    :param order_id: The order id to mark as 'sold'.
    :type order_id: str
    :return: The rendered shop-invoice-list.html template with all store orders.
    :rtype: django.http.HttpResponse
    """
    
    

    orders = StoreOrders.objects.filter(order_id=order_id)
    
    for order in orders: 
        
        order.sales.status = "sold" 
        order.save()  
        
    orders= StoreOrders.objects.raw("select * from manager_StoreOrders group by order_id")
        
    if len(orders)>10:
            
        orders = StoreOrders.objects.raw("select * from manager_StoreOrders group by order_id limit 10")
            
        
    
    contxt = {"orders":orders}
    
    return render(request, 'manager/shop-invoice-list.html',contxt)

def store_process_delivery(request):

    """
    Handles POST requests containing delivery details and updates the relevant
    models, namely StoreOrders and DeliveryDetails. The function renders a
    success or failure message to the user based on the status of the update.

    :param request: The request object.
    :type request: django.http.HttpRequest
    :return: An HttpResponse object with a success or failure message.
    :rtype: django.http.HttpResponse
    """

    if request.method == 'POST':
        
        order_id = request.POST.get('order_id')
        status = request.POST.get('status')
        dpn = request.POST.get('dpn')
        dppn  = request.POST.get('dppn')
        person_image = request.POST.get('personImageString')
        d_note_image = request.POST.get('noteImageString')
       
        dd = request.POST.get('dd')
        dc = request.POST.get('dc')
        
        print(status)
        
        resp = ""
        
        if status == 'pnd' or status == 'npd' : 
            
           status = 'paid & delivered' if status == 'pnd' else 'not paid & delivered'
            
           orders = StoreOrders.objects.filter(order_id=order_id)
           
           for order in orders:
               
               if order.delivery_details.paid_status == 'paid & not delivered' or order.delivery_details.paid_status == 'not paid & not delivered':
                   
                   order.delivery_details.paid_status = status
                   order.delivery_details.delivery_note_image = d_note_image
                   order.delivery_details.status = 'delivered'
                   order.delivery_details.last_updates = datetime.datetime.now()
                   order.sales.status = 'sold & delivered'
                   
                   order.save()
                   
                   resp = f'<strong style="color:green">Order marked as {status} successfully</strong>'
                   
                   
               else:
                   
                   resp = '<strong style="color:red">Order is already paid & delivered</strong>'
                   
                   
                   
                   
                
                   
                   
                  
        
        elif status == 'pnotd' or status == 'npnd':
            
            status = 'paid & not delivered' if status == 'pnotd' else 'not paid & not delivered'
            
            orders = StoreOrders.objects.filter(order_id=order_id)
            
            delivery_details = DeliveryDetails(
                
                    delivery_cost = dc,
                    delivery_address = dd,
                    delivery_date = datetime.datetime.now(),
                    delivery_person_name = dpn,
                    delivery_person_phone = dppn,
                    delivery_perdon_id = dppn,
                    delivery_person_id_image = person_image,
                    delivery_note_image = d_note_image,
                    status = 'in-transit',
                    paid_status = status,
                    last_updates = datetime.datetime.now()
                
                )
            delivery_details.save()
                
              
            
            for order in orders:
                
                order.delivery_details = delivery_details
                order.sales.status = 'sold & not delivered'
                
                order.save()
                
                resp = f'<strong style="color:green">Order marked as {status} successfully</strong>'
                
    
    return HttpResponse(resp)


def store_generate_d_notes(request,order_id):
    
    contxt = gen_order_docs(order_id)
    
    return render(request, 'manager/store-dnote.html',contxt)





    
    
    
    
    
    
    
    
    
    
    
    
    
        
       
    
    
            
        
        
        
        
        


    
    

