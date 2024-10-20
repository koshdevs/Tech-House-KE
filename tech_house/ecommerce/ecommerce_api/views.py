from rest_framework.response import Response
from rest_framework.decorators import api_view
from ecommerce.models import ProductBuild
from .serializers import ProductBuildSerializer



@api_view(['GET']) 
def ProductsApiView(request):
    
    products = ProductBuild.objects.all()
    
    products = ProductBuildSerializer(products, many=True)
    
    
    
    return Response(products.data)

@api_view(['GET']) 
def ProductsDetailsApiView(request,pk):
    
    product = ProductBuild.objects.get(pk=pk)
    
    product = ProductBuildSerializer(product, many=False)
    
    
    
    return Response(product.data)