from .cart import ShopCart

def cart(request):
    
    return {
        'cart':ShopCart(request)
    }