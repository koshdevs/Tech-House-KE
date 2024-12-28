from django.shortcuts import render,get_object_or_404
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import ProductBuild,ProductCategory,ProductReview
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
    

    products = cache.get('eco-products')
    categories = cache.get('eco-categories')
    
    if products is None:
        
        products = ProductBuild.objects.all()
        cache.set('eco-products', products, timeout=2400)
    
    ''' Pagination '''
    
    if categories is None:
        
        categories = ProductCategory.objects.all()
        cache.set('eco-categories', categories, timeout=2400)
        
   
  
        
        
    cart = ShopCart(request)
    
    items = cart_render(cart)
    
    
  
  
    contxt = {"products":products,"categories":categories} | items

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
    
    reviews = ProductReview.objects.filter(product__pk=pk).order_by('-updated_on')
    
    
    contxt = {"product":product,"reviews":reviews} | items
    
    return render(request,'ecommerce/shop-details.html',contxt)

def shop_cart_view(request):
    
    cart = ShopCart(request)
    
    items = cart_render(cart)
    
    contxt = items
    
    print(contxt)
    
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


def shop_plus_to_cart(request,pk): 
    
    cart = ShopCart(request)
    
    product = get_object_or_404(ProductBuild,pk=pk)

    cart.add(product=product,qty=1)
    
    
    items =cart_render(cart)
    
    contxt = {"product":product} | items
    
    return render(request,'ecommerce/shop-cart-page-change.html',contxt)
    
    


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
   
    
    return render(request,'ecommerce/shop-cart-page-change.html',contxt)


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
    
    contxt = {"product":product,"pk":pk} | items
    
    return render(request,'ecommerce/shop-add-to-cart.html',contxt)






def filter_products_by_brand(request,brand_id):
    
    products = ProductBuild.objects.filter(brand__pk=brand_id)
    
    if len(products) > 10: 
        
        products = products[:10]
        
    else: 
        
        products  = products 
        
        
    
    return render(request,'ecommerce/shop-filter-by-brand.html',{"products":products})


def filter_by_sub_category(request,sub_category_id):
    
    products = ProductBuild.objects.filter(sub_category__pk=sub_category_id)
    categories = cache.get("eco-categories")
    
    if len(products) > 10: 
        
        products = products[:10]
        
    else: 
        
        products  = products 
        
    if categories is None:
        
        categories = ProductCategory.objects.all()
        cache.set('eco-categories', categories, timeout=2400)
        
    cart = ShopCart(request)
    
    items = cart_render(cart)
    
    
  
  
    contxt = {"products":products,"categories":categories} | items
        
    return render(request,'ecommerce/shop-sub-category.html',contxt)

def filter_by_price_range(request):
    
    if request.method == "POST":
    
        price = request.POST.get('price')
        
        min = int(price.split('-')[0])
        max = int(price.split('-')[1])
        
        
        print(max)
        
        products = ProductBuild.objects.filter(price__range=(min,max)).order_by('-price')
        
        if len(products) > 10: 
            
            products = products[:10]
            
        else: 
            
            products  = products 
            
            
        return render(request,'ecommerce/shop-filter-by-brand.html',{"products":products})
    
def sort_products(request):
    
    sort_by =  request.GET.get('basic')
    
    
    
    if sort_by == "1":
        
        products = ProductBuild.objects.order_by('price')
    
    elif sort_by == "2":
        
        products = ProductBuild.objects.order_by('-price') 
        
    elif sort_by == "3":
        
        products = ProductBuild.objects.order_by('price')
        
    else: 
        
        products = ProductBuild.objects.all()
        
    if len(products) > 10: 
            
        products = products[:10]
            
    else: 
            
        products  = products    
    
        
    
    return render(request,'ecommerce/shop-filter-by-brand.html',{"products":products})         
    
    


def search_products(request):
    

    """
    Searches for products based on a query parameter. If the query parameter is provided, it filters products
    whose category name, brand name, model name, or feature specifications contain the query value. If the query
    parameter is empty, it renders all products. The result is rendered as shop-products-search-results.html.
    
    :param request: The HTTP request object.
    :type request: django.http.HttpRequest
    :return: The rendered shop-products-search-results.html template with filtered products.
    :rtype: django.http.HttpResponse
    """

    query = request.GET.get('query')
    
    products = ProductBuild.objects.filter(
    Q(category__name__contains=query) |
            Q(brand__name__contains=query) |  
                Q(model__name__contains=query) | 
                    Q(features__specifications__contains=query)).distinct()
    
   
    
    return render(request,'ecommerce/shop-products-search-results.html',{"products":products})

def csrf_failure_403(request,reason="Error as a result of cross forgery protection"): 
    
    
    """
    Handles CSRF failure and returns a 403 Forbidden error page.
    
    :param request: The request object.
    :type request: django.http.HttpRequest
    :param reason: The reason for the CSRF failure.
    :type reason: str    
    :return: The rendered 403 Forbidden error page.
    :rtype: django.http.HttpResponse
    """
    
    
    contxt = {"reason":reason}
    
    

    return render(request,'403_csrf_failure.html',contxt,status=403)

#=====================Reviews Management ======================

def create_product_review(request): 
    

    """
    Creates a product review.
    
    If the request is a POST, it creates a product review based on the POST data. If the user is authenticated, it creates a new
    ProductReview object with the user, product_id, review, and rating. If the user is not authenticated, it sets a message
    indicating that the user must be logged in to create a review. Finally, it renders the shop-products-review.html template
    with the reviews and message.
    
    :param request: The HTTP request object.
    :type request: django.http.HttpRequest
    :return: The rendered shop-products-review.html template with the reviews and message.
    :rtype: django.http.HttpResponse
    """

    if request.method == 'POST': 
        
        id = request.POST.get('product_id') #product_id
        review=request.POST.get('review')
        rating = request.POST.get('rating')
        
        
        if request.user.is_authenticated:
        
            review = ProductReview(
                
                user=request.user,product_id=id,review=review,rating=rating	
                
                )
            
            review.save()
            
            msg = "<strong style='color:green'>Review updated successfully</strong>"
            
        else: 
            
            msg = "<strong style='color:red'>User not logged in</strong>"
            #return redirect('eco-login')
            
            
        
        reviews = ProductReview.objects.filter(product__pk=id).order_by('-updated_on')
        
        contxt = {"reviews": reviews,"msg": msg}
        
        return render(request,'ecommerce/shop-products-review.html',contxt)
    
    
def edit_product_review(request): 
    
    if request.method == 'POST':
        
        product_id = request.POST.get('product_edit_id')
        review_id = request.POST.get('review_edit_id')
        review=request.POST.get('review_edit')
        rating = request.POST.get('rating_edit')
        
        
        review_ = ProductReview.objects.get(pk=review_id)
        
        review_.review = review
        review_.rating = rating
        
        review_.save()
        
        msg = "<strong style='color:green'>Review updated successfully</strong>"
        
        reviews = ProductReview.objects.filter(product__pk=product_id).order_by('-updated_on')
        
        contxt = {"reviews": reviews,"msg": msg}
        
        return render(request,'ecommerce/shop-products-review.html',contxt)


def delete_product_review(request): 
    
    if request.method == 'POST':
        
        review_id = request.POST.get('review_delete_id')
        print(review_id)
        product_id = request.POST.get('product_delete_id')
        
        review_ = ProductReview.objects.get(pk=review_id)
        
        review_.delete()
        
        msg = "<strong style='color:green'>Review deleted successfully</strong>"
        
        reviews = ProductReview.objects.filter(product__pk=product_id).order_by('-updated_on')
        
        contxt = {"reviews": reviews,"msg": msg}
        
        return render(request,'ecommerce/shop-products-review.html',contxt)
    
    

        
        
        
    
    
    
    

   