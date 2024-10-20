from django.shortcuts import render,get_object_or_404
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import ProductBuild
from .cart import ShopCart,display_cart_items

#Create your views here.
def shop_view(request):
    
    products = cache.get('products')
    
    if products is None:
        
        products = ProductBuild.objects.all()
        cache.set('products', products, timeout=2400)
    
    ''' Pagination '''
  
    paginator = Paginator(products, 6)
    
    page = request.GET.get("page")
    try:
        page_obj = paginator.get_page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
        
        
    cart = ShopCart(request)
    
    items = display_cart_items(cart.get_items())

  
    contxt = {"products":products,"page_obj":page_obj,"items":items}

    return render(request,'ecommerce/shop.html',contxt)


def shop_details_view(request,pk):
    
    product = ProductBuild.objects.get(pk=pk)
    contxt = {"product":product}
    
    return render(request,'ecommerce/shop-details.html',contxt)


def shop_add_to_cart_view(request,pk):
    
    cart = ShopCart(request)
    
    product = get_object_or_404(ProductBuild,pk=pk)

    cart.add(product=product,qty=1)
    
    
    items = display_cart_items(cart.get_items())
   
    print(items)
    
    contxt = {"items":items,"product":product}
    
    return render(request,'ecommerce/shop-add-to-cart.html',contxt)

