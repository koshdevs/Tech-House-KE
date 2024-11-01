from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from ecommerce.models import ProductBuild 
from .models import StoreSales,CustomerDetails,StoreOrders,OrgDetails
from.sales_ops import get_sales_data

# Create your views here.


def store_counter(request):
    
    
    items = ProductBuild.objects.filter()
    
    sales,totals = get_sales_data('cart')
    
    
    contxt = {"items":items,"sales":sales,"totals":totals}
    
    return render(request, 'manager/store_sales.html',contxt)


def add_to_counter(request,pk): 
    
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
    
    sales = StoreSales.objects.get(pk=pk)
    
    sales.delete()
    
    sales,totals = get_sales_data('cart')
    
    contxt = {"sales":sales,"totals":totals}
    
    return render(request, 'manager/shop-counter-change.html',contxt)


def gen_store_invoices(request,order_id):
    
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
    
    contxt = {"orders":orders}
    
    return render(request, 'manager/shop-invoice-list.html',contxt)
    
    
            
        
        
        
        
        


    
    

