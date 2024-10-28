from django.shortcuts import render
from ecommerce.models import ProductBuild 
from .models import StoreSales

# Create your views here.


def store_counter(request):
    
    
    items = ProductBuild.objects.filter()
    
    contxt = {"items":items}
    
    return render(request, 'manager/store_sales.html',contxt)


def add_to_counter(request,pk): 
    
    product = ProductBuild.objects.get(pk=pk)
    
    sales = StoreSales( 
                       
                       product=product,
                       quantity =1,
                       price = product.price,
                       created_by = request.user,
                       status = 'cart'
                       
                       )
    
    sales.save()
    
    product_by_serial = ProductBuild.objects.get(serial1=product.serial1)
    product_by_serial.status = 'sold'
    product_by_serial.save()
    
    sales  = StoreSales.objects.all()
    
    contxt = {"product":product,"sales":sales}
    
    return render(request, 'manager/add_to_counter.html',contxt)
    
    

