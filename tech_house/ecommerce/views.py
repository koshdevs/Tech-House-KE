from django.shortcuts import render,get_object_or_404
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import ProductBuild
from .cart import ShopCart,display_cart_items,cart_render

#Create your views here.
def shop_view(request):

    """
    Displays all products in the shop with pagination. Products are cached for 40 minutes.
    
    :param request: The request object.
    :type request: django.http.HttpRequest
    :return: The rendered shop.html template.
    :rtype: django.http.HttpResponse
    """
    

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
    
    items = cart_render(cart)
    
    
  
  
    contxt = {"products":products,"page_obj":page_obj} | items

    return render(request,'ecommerce/shop.html',contxt)


def shop_details_view(request,pk):
    

    """
    Displays the details of a product with id :pk: in the shop details template.
    
    :param request: The request object.
    :type request: django.http.HttpRequest
    :param pk: The id of the product to be displayed.
    :type pk: int
    :return: The rendered shop-details.html template.
    :rtype: django.http.HttpResponse
    """

    product = ProductBuild.objects.get(pk=pk)
    
    cart = ShopCart(request)
    
    items = cart_render(cart)
    
    
    contxt = {"product":product} | items
    
    return render(request,'ecommerce/shop-details.html',contxt)

def shop_cart_view(request):
    
    cart = ShopCart(request)
    
    items = cart_render(cart)
    
    contxt = items
    
    
    
    return render(request,'ecommerce/shop-cart.html',contxt)

def shop_add_to_cart_view(request,pk):

    """
    Adds a product with id :pk: to the cart, and displays the items in the cart in the shop-add-to-cart.html template.
    
    :param request: The request object.
    :type request: django.http.HttpRequest
    :param pk: The id of the product to add to the cart.
    :type pk: int
    :return: The rendered shop-add-to-cart.html template.
    :rtype: django.http.HttpResponse
    """

    cart = ShopCart(request)
    
    product = get_object_or_404(ProductBuild,pk=pk)

    cart.add(product=product,qty=1)
    
    
    items =cart_render(cart)
    
    contxt = {"product":product} | items
    
    return render(request,'ecommerce/shop-add-to-cart.html',contxt)

def shop_minus_to_cart_view(request,pk):
    

    """
    Decreases the quantity of a product with id :pk: in the cart, and displays the updated cart items
    in the shop-add-to-cart.html template.

    :param request: The request object.
    :type request: django.http.HttpRequest
    :param pk: The id of the product to decrease in the cart.
    :type pk: int
    :return: The rendered shop-add-to-cart.html template with updated cart items.
    :rtype: django.http.HttpResponse
    """

    cart = ShopCart(request)
    
    product = get_object_or_404(ProductBuild,pk=pk)

    cart.add(product=product,qty=-1)
    
    items =cart_render(cart)
    
    contxt = {"product":product} | items
   
    
    return render(request,'ecommerce/shop-add-to-cart.html',contxt)


def shop_rem_cart_view(request,pk):
    

    """
    Removes a product with id :pk: from the cart, and displays the updated cart items
    in the shop-add-to-cart.html template.

    :param request: The request object.
    :type request: django.http.HttpRequest
    :param pk: The id of the product to remove from the cart.
    :type pk: int
    :return: The rendered shop-add-to-cart.html template with updated cart items.
    :rtype: django.http.HttpResponse
    """

    cart = ShopCart(request)
    
    product = get_object_or_404(ProductBuild,pk=pk)

    cart.remove(product)
    
    items =cart_render(cart)
    
    contxt = {"product":product} | items
    
    return render(request,'ecommerce/shop-add-to-cart.html',contxt)

   
