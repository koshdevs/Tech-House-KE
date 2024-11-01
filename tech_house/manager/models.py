from django.db import models
from django.contrib.auth.models import User
from ecommerce.models import ProductBuild
# Create your models here.

class StoreSales(models.Model):
    
    product = models.ForeignKey(ProductBuild, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, )
    tax= models.DecimalField(max_digits=10,default=16.00, decimal_places=2)   
    date = models.DateField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=200,choices=(('cart','cart'),('ínvoiced','invoiced'),('sold','sold'),('returned','returned'),('delivered','delivered')))
    
    
    class Meta:  
        
        verbose_name_plural = "Store Sales"

class CustomerDetails(models.Model):
    
    name = models.CharField(max_length=100,null=True, blank=True) 
    company_name = models.CharField(max_length=100,null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15,null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    terms = models.TextField(null=True, blank=True)
    order_id = models.CharField(max_length=100,null=True, blank=True)
    
    class Meta:
        
        verbose_name_plural = "Customer Details"
    
        
class StoreOrders(models.Model):
    
    order_id = models.CharField(max_length=100)
    sales = models.ForeignKey(StoreSales, on_delete=models.CASCADE)
    customer_details = models.ForeignKey(CustomerDetails,null=True, on_delete=models.SET_NULL)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        
        verbose_name_plural = "Store Orders"
    
        
        
class OrgDetails(models.Model):
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    payment = models.TextField()
    terms = models.TextField()
    logo = models.ImageField(default='',upload_to="org_pics")
    
    class Meta: 
        
        verbose_name_plural = "Org Details"
        
        
        
    
    
    