from rest_framework.response import Response
from rest_framework.decorators import api_view



@api_view(['GET']) 
def ProductsApiView(request):
    products = ""
    
    contxt = {"products":products}
    
    return Response(contxt)