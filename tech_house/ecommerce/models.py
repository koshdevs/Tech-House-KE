from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ProductCategory(models.Model):
    
    name = models.CharField(max_length=100)
    
    def __str__(self):
        
        return self.name
    class Meta:
        
        verbose_name_plural = 'Product Categories'    
class ProductBrand(models.Model):
    
    name = models.CharField(max_length=100)
    category = models.ForeignKey(ProductCategory,null=True,on_delete=models.CASCADE)
    
    def __str__(self):
        
        return self.name
    
    class Meta:
        
        verbose_name_plural = 'Product Brands'
        
class ProductModel(models.Model):
    
    name = models.CharField(max_length=100)
    SKU = models.CharField(max_length=100)
    
    def __str__(self):
        
        return self.name
    
    class Meta:
        
        verbose_name_plural = 'Product Models'
        
class ProductOrigin(models.Model):
    
    name = models.CharField(max_length=100)
    
    def __str__(self):
        
        return self.name
    class Meta:
        
        verbose_name_plural = 'Product Origin'

class ProductFeatures(models.Model):
    
    name = models.CharField(max_length=100)
    specifications = models.CharField(max_length=200)
    
    
    def __str__(self):
        
        return self.name + "-" + self.specifications
    
    class Meta:
        
        verbose_name_plural = 'Product Features'
        
class ProductImages (models.Model):
    
    angle = models.CharField(max_length=100)
    image = models.ImageField(default='default.jpg', upload_to="products_pics")
        
        
class ProductBuild(models.Model):
    
    serial1 = models.CharField(max_length=100)
    serial2 = models.CharField(max_length=100,null=True,blank=True)
    category = models.ForeignKey(ProductCategory,on_delete=models.CASCADE)
    brand = models.ForeignKey(ProductBrand,on_delete=models.CASCADE)
    model = models.ForeignKey(ProductModel,on_delete=models.CASCADE)
    origin = models.ForeignKey(ProductOrigin,on_delete=models.CASCADE)
    features = models.ManyToManyField(ProductFeatures)
    images = models.ManyToManyField(ProductImages)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    was = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    status = models.CharField(max_length=200,choices=(('in-stock','in-stock'),('out-stock','out-stock'),('low','low')))
    stage = models.CharField(max_length=100,default='in-stock',choices=(('in-stock','in-stock'),('sold','sold'),('returned','returned')))
    overview = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        
        return self.model.name
    
    class Meta:
        
        verbose_name_plural = "Create Product"
        
    