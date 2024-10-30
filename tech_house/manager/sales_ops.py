from .models import StoreSales
def get_sales_data(status):
    
    sales  = StoreSales.objects.filter(status=status)
    tax = sum([i.tax for i in sales])
    subtotal = sum([i.price for i in sales])
    total = tax  + subtotal
    
    totals  = {'tax':tax,'subtotal':subtotal,'total':total}	
    
    return sales,totals
    
    