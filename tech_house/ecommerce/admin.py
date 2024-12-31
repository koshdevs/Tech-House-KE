from django.contrib import admin
from .models import *

# Register your models here.


admin.site.register(ProductFeatures)
admin.site.register(ProductImages)

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    
@admin.register(ProductSubCategory)
class ProductSubCategoryAdmin(admin.ModelAdmin):
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
    
@admin.register(ProductProcessor)
class ProductProcessorAdmin(admin.ModelAdmin):
    search_fields = ["processor"]
    
@admin.register(ProductGeneration)
class ProductGenerationAdmin(admin.ModelAdmin):
    search_fields = ["generation"]
    
@admin.register(ProductMemory)
class ProductMemoryAdmin(admin.ModelAdmin):
    search_fields = ["memory"]

@admin.register(ProductBuild)
class ProductBuildAdmin(admin.ModelAdmin):
    list_display = ["serial1", "category", "brand", "model", "origin","cost","price","tax","stage","status","updated_on","created_on"]
    search_fields = ("serial1","category__name","brand__name","model__name","origin__name",)
    filter_horizontal = ("features",)
    autocomplete_fields = ["brand","category","model","origin"]	
    
admin.site.register(OrgProfile)
admin.site.register(advert)
admin.site.register(ProductReview)
admin.site.register(DeliveryCategory)
    


