from django.db import models
from django.contrib.auth.models import User
from ecommerce.models import ProductBuild
# Create your models here.

class StoreSales(models.Model):
    
    product = models.ForeignKey(ProductBuild, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    
    class Meta:  
        
        verbose_name_plural = "Store Sales"
    