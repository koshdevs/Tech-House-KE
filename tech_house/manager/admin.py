from django.contrib import admin
from .models import OrgDetails
# Register your models here.

@admin.register(OrgDetails)
class OrgDetailsAdmin(admin.ModelAdmin):
    list_display = ['name','email','phone','payment','terms']