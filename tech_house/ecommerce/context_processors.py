from .cart import ShopCart
from .models import ProductBuild,ProductCategory

def cart(request):
    
    return {
        'cart':ShopCart(request)
    }
    
    
def show_products(request):  
    
    products = ProductBuild.objects.raw("select *from ecommerce_ProductBuild group by serial2")
    
    print(products)
    category = ProductCategory.objects.all()
    
    contxt = {
        
        'products':products,
        'category':category
    }
    
    
    return contxt