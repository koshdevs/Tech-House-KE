from .models import StoreSales
def get_sales_data(status):
    
    sales  = StoreSales.objects.filter(status=status)
    
    subtotal = round(sum([i.price for i in sales]),2)
    tax = round((subtotal*sales[0].tax)/100 if len(sales) > 0 else 0.00,2)
    total = tax  + subtotal
    total = round(total,2)
    totals  = {'tax':tax,'subtotal':subtotal,'total':total}	
    
    return sales,totals
    
    