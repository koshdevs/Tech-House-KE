from rest_framework import serializers
from ecommerce.models import ProductBuild


class ProductBuildSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProductBuild
        fields = '__all__'