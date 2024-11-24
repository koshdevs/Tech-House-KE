from django.contrib import admin
from .models import OrgDetails,StoreSales
# Register your models here.

@admin.register(OrgDetails)
class OrgDetailsAdmin(admin.ModelAdmin):
    list_display = ['name','email','phone','payment','terms']
    
@admin.register(StoreSales)
class StoreSalesAdmin(admin.ModelAdmin):
    list_display = ['product__serial1','product__category__name','product__model__name','product__brand__name','product__origin__name','quantity','price']	
    
