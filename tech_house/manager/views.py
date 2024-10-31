from django.shortcuts import render
from ecommerce.models import ProductBuild 
from .models import StoreSales
from.sales_ops import get_sales_data

# Create your views here.


def store_counter(request):
    
    
    items = ProductBuild.objects.filter()
    
    sales,totals = get_sales_data('cart')
    
    
    contxt = {"items":items,"sales":sales,"totals":totals}
    
    return render(request, 'manager/store_sales.html',contxt)


def add_to_counter(request,pk): 
    
    product = ProductBuild.objects.get(pk=pk)
    
    sales_check = StoreSales.objects.filter(product__serial1=product.serial1)
    
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


def gen_store_invoices(request): 
    
    sales,totals = get_sales_data('cart')
    
    contxt = {"sales":sales,"totals":totals}
    
    return render(request, 'manager/store-invoice.html',contxt)


    
    

