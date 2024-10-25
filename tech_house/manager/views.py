from django.shortcuts import render
from ecommerce.models import ProductBuild

# Create your views here.


def store_counter(request):
    
    
    items = ProductBuild.objects.all()
    
    contxt = {"items":items}
    
    return render(request, 'manager/store_sales.html',contxt)