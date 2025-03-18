from django.core.cache import cache
from .cart import ShopCart,cart_render
from .models import ProductBuild,ProductCategory,OrgProfile


def cart(request):
    
    return {
        'cart':ShopCart(request)
    }
    
    
def show_products(request):  
    
    products = ProductBuild.objects.all()
    
    print(products)
    category = ProductCategory.objects.all()
    
    contxt = {
        
        'products':products,
        'category':category
    }
    
    
    return contxt


def show_org_profile(request): 
    
    
    profile = cache.get('org-profile')
    
    if profile is None:
        
        profile = OrgProfile.objects.all()
        
        cache.set('org-profile', profile, timeout=2400)
    
    if len(profile) > 0: 
        
        profile = profile[0] 
    
    contxt = {
        
        'profile':profile
    }
    
    return contxt
    


