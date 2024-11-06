from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.db.models import Q
from ecommerce.models import ProductBuild 
from .models import StoreSales,CustomerDetails,StoreOrders,OrgDetails
from.sales_ops import get_sales_data
import datetime

# Create your views here.


def store_counter(request):
    
    

    """
    The store counter view is the main view for the store counter,
    it shows all the products in the store and their quantities.
    The view also shows the total of all the products in the store
    and the total of all the products in the cart.
    """
    

    items = ProductBuild.objects.filter()
    
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

    orders = StoreOrders.objects.filter(order_id=order_id)
    
    if len(orders) > 0:
        
        customer_details = StoreOrders.objects.filter(order_id=order_id)[0].customer_details
        date = orders[0].date
        
    subtotal = round(sum([i.sales.price for i in orders]))
    tax = round((subtotal*orders[0].sales.tax)/100 if len(orders) > 0 else 0.00,2)
    total = tax  + subtotal
    total = round(total,2)
    totals  = {'tax':tax,'subtotal':subtotal,'total':total}
    
    if OrgDetails.objects.count() > 0:
        org = OrgDetails.objects.all()[0]
    
    
    
    contxt = {"orders":orders, "customer_details":customer_details,"totals":totals ,"order_id":order_id,"date":date,"org":org}
    
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
    
    if request.method == 'POST':
        
        status = request.POST.get('status')
        dpn = request.POST.get('dpn')
        dppn  = request.POST.get('dppn')
        dpidf = request.POST.get('dpidf')
        dpidb = request.POST.get('dpidb')
        dd = request.POST.get('dd')
        
        
        
        

    orders = StoreOrders.objects.filter(order_id=order_id)
    
    for order in orders: 
        
        order.sales.status = "sold" 
        order.save()  
        
    orders= StoreOrders.objects.raw("select * from manager_StoreOrders group by order_id")
        
    if len(orders)>10:
            
        orders = StoreOrders.objects.raw("select * from manager_StoreOrders group by order_id limit 10")
            
        
    
    contxt = {"orders":orders}
    
    return render(request, 'manager/shop-invoice-list.html',contxt)
    
    
    
    
    
    
        
       
    
    
            
        
        
        
        
        


    
    

