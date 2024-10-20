from django.contrib import admin
from .models import *

# Register your models here.


admin.site.register(ProductFeatures)
admin.site.register(ProductImages)

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    search_fields = ["name"]
@admin.register(ProductBrand)
class ProductBrandAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    
@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    search_fields = ["name"]

@admin.register(ProductOrigin)
class ProductOriginAdmin(admin.ModelAdmin): 
    search_fields = ["name"]

@admin.register(ProductBuild)
class ProductBuildAdmin(admin.ModelAdmin):
    filter_horizontal = ("features",)
    autocomplete_fields = ["brand","category","model","origin"]	
    


