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
    tag_name = models.CharField(max_length=100,null=True)
    image = models.ImageField(default='default.jpg', upload_to="products_pics")
    
    def __str__(self): 
        
        return self.tag_name if not "None"  else self.angle
    
    class Meta:
        
        verbose_name_plural = 'Product Images'
    

class ProductPriceRange(models.Model):
    
    range = models.CharField(max_length=100, blank=True,null=True)
    
    def __str__(self): 
        
        return self.range
    
    class Meta:
        
        verbose_name_plural = 'Product Price Range'
    
class ProductSubCategory(models.Model):
    
    name = models.CharField(max_length=100,blank=True,null=True)
    decscription = models.TextField(blank=True,null=True)
    
    def __str__(self): 
        
        return self.name
    
    class Meta:
        
        verbose_name_plural = 'Product Sub Category'
    
class ProductProcessor(models.Model):
    
    processor = models.CharField(max_length=100,blank=True,null=True)
    decsription = models.TextField(blank=True,null=True)
    
    def __str__(self): 
        
        return self.processor
    
    class Meta:
        
        verbose_name_plural = 'Product Processor'
    
class ProductGeneration(models.Model):
    
     generation = models.CharField(max_length=100,blank=True,null=True)
     decsription = models.TextField(blank=True,null=True)
     
     def __str__(self): 
        
        return self.generation
     
     class Meta:
        
        verbose_name_plural = 'Product Generation'
    
class ProductMemory(models.Model):
    
    memory = models.CharField(max_length=100,blank=True,null=True)
    decsription = models.TextField(blank=True,null=True)
    
    def __str__(self):
        return self.memory
    
    class Meta:
        
        verbose_name_plural = "Product Memory"
        
        
class ProductBuild(models.Model):
    
    serial1 = models.CharField(max_length=100)
    serial2 = models.CharField(max_length=100,null=True,blank=True)
    category = models.ForeignKey(ProductCategory,on_delete=models.CASCADE)
    sub_category = models.ForeignKey(ProductSubCategory,on_delete=models.CASCADE,blank=True,null=True)
    brand = models.ForeignKey(ProductBrand,on_delete=models.CASCADE)
    model = models.ForeignKey(ProductModel,on_delete=models.CASCADE)
    origin = models.ForeignKey(ProductOrigin,on_delete=models.CASCADE)
    features = models.ManyToManyField(ProductFeatures)
    processor = models.ForeignKey(ProductProcessor,on_delete=models.CASCADE,blank=True,null=True)
    generation = models.ForeignKey(ProductGeneration,on_delete=models.CASCADE,blank=True,null=True)
    memory = models.ForeignKey(ProductMemory,on_delete=models.CASCADE,blank=True,null=True)
    images = models.ManyToManyField(ProductImages)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    was = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    tax= models.DecimalField(max_digits=10,default=16.00, decimal_places=2) 
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
        

class DeliveryCategory(models.Model):
    
    name = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    
    def __str__(self):
        
        return self.name
    
    class Meta:
        
        verbose_name_plural = "Delivery Categories"
        
        
class OrgProfile(models.Model):
    
    fb_link = models.CharField(max_length=100)
    x_link = models.CharField(max_length=100)
    ig_link = models.CharField(max_length=100)
    wa_link = models.CharField(max_length=100)
    pi_link =models.CharField(max_length=100)
    th_link = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    logo = models.ImageField(default='',upload_to="org_pics") 
    name = models.CharField(max_length=100)
    others = models.TextField()
    
    class Meta:
        
        verbose_name_plural = "Org Profile"
        
        
class advert(models.Model): 
    
    name = models.CharField(max_length=100)
    image = models.ImageField(default='default.jpg', upload_to="advert_pics")
    link = models.CharField(max_length=100)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    
class ProductReview(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductBuild, on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    class Meta:
        
        verbose_name_plural = "Product Review"
    
    
    
    
    
    
   
        
    