from .models import ProductBuild,ProductImages,ProductModel
from ecommerce.ecommerce_api.serializers import ProductBuildSerializer
from decimal import Decimal
class ShopCart(): 
    
    def __init__(self,request): 
        
        self.session = request.session
        cart = self.session.get('cart_session_key')
        if not cart:
            cart = self.session['cart_session_key'] = {}
        self.cart = cart
        
    def save(self):
        
        
        self.session['cart_session_key'] = self.cart
        self.session.save() 
    
    def add(self,product,qty):
        product_id = str(product.pk)
        if product_id not in self.cart:
            self.cart[product_id] = {'qty':1,"price":str(product.price)}
        else:
            self.cart[product_id]['qty'] += qty
            
        self.save()
            
    
    def get_items(self):
        product_ids = self.cart.keys()
        products = ProductBuild.objects.filter(pk__in=product_ids)
        cart = self.cart.copy()
        
        for product in products:
            cart[str(product.pk)]['product'] = ProductBuildSerializer(product).data
            
        for item in cart.values():
            item["price"] = item["price"]
            item['total_price'] = item['qty'] * float(item['price'])
            yield item
        
        
            
    
            
              
    def remove(self,product): 
        
        product_id = str(product.pk)
        if product_id in self.cart:
            del self.cart[product_id]
        self.save()
        
    def clear(self):
        
        for key in list(self.cart.keys()):
            del self.cart[key]
        self.save()
    
    
    def __len__(self):
        return sum(item["qty"] for item in self.cart.values())
    
    
    def sub_total_price(self):	
        
        return sum(item["total_price"] for item in self.cart.values())
    

def display_cart_items(items): 
  
    return [{
            
            'product_id': item['product']['id'],
            'product_name': ProductModel.objects.get(pk=item['product']['model']).name,
            'quantity': item['qty'],
            'price': item['price'],
            'total_price': item['qty']*Decimal(item['price']),
            'image': ProductImages.objects.get(pk=item['product']['images'][0]).image.url,	
        }
            
        for item in items
            
            ]
    
def cart_render(cart): 
    

    """
    Render the cart items and item number from a given cart instance.

    Parameters
    ----------
    cart : Cart
        The cart instance to render.

    Returns
    -------
    dict
        A dictionary with two keys: 'items' and 'item_no'. 'items' is a list of
        dictionaries, each representing an item in the cart, and 'item_no' is
        the total number of items in the cart.

    """
    

    items = display_cart_items(cart.get_items())
    item_no = cart.__len__()
    total = cart.sub_total_price()
    return {"items":items,"item_no":item_no,"total":total}
    
    
