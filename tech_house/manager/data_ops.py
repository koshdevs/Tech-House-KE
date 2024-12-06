from .models import *
import datetime
def get_sales_data(status):
    
    sales  = StoreSales.objects.filter(status=status)
    
    subtotal = round(sum([i.price for i in sales]),2)
    tax = round((subtotal*sales[0].tax)/100 if len(sales) > 0 else 0.00,2)
    total = tax  + subtotal
    total = round(total,2)
    totals  = {'tax':tax,'subtotal':subtotal,'total':total}	
    
    return sales,totals

def gen_order_docs(order_id):
    
    orders = StoreOrders.objects.filter(order_id=order_id)
    
    if len(orders) > 0:
        
        customer_details = StoreOrders.objects.filter(order_id=order_id)[0].customer_details
        delivery_details = StoreOrders.objects.filter(order_id=order_id)[0].delivery_details
        date = orders[0].date
        
    subtotal = round(sum([i.sales.price for i in orders]))
    tax = round((subtotal*orders[0].sales.tax)/100 if len(orders) > 0 else 0.00,2)
    total = tax  + subtotal
    total = round(total,2)
    totals  = {'tax':tax,'subtotal':subtotal,'total':total}
    
    if OrgDetails.objects.count() > 0:
        org = OrgDetails.objects.all()[0] 
        
        
    
    
    
    contxt = {"orders":orders, "customer_details":customer_details,"delivery_details":delivery_details,"totals":totals ,"order_id":order_id,"date":date,"org":org}
    
    return contxt

def gen_order_items_docs(order_id,ids_list):
    

    """
    Generates a context dictionary containing order-related information for the given order ID
    and list of sales IDs. The function retrieves the relevant store orders, customer and delivery
    details, calculates the subtotal, tax, and total, and includes organizational details.

    :param order_id: The ID of the order to generate documents for.
    :type order_id: str
    :param ids_list: A list of sales IDs to filter the orders.
    :type ids_list: list
    :return: A dictionary containing orders, customer details, delivery details, totals, order ID, date, and organizational details.
    :rtype: dict
    """

    orders = StoreOrders.objects.filter(order_id=order_id,sales__pk__in =ids_list)
    
    if len(orders) > 0:
        
        customer_details = StoreOrders.objects.filter(order_id=order_id)[0].customer_details
        delivery_details = StoreOrders.objects.filter(order_id=order_id)[0].delivery_details
        date = orders[0].date
        
    subtotal = round(sum([i.sales.price for i in orders]))
    tax = round((subtotal*orders[0].sales.tax)/100 if len(orders) > 0 else 0.00,2)
    total = tax  + subtotal
    total = round(total,2)
    totals  = {'tax':tax,'subtotal':subtotal,'total':total}
    
    if OrgDetails.objects.count() > 0:
        org = OrgDetails.objects.all()[0] 
        
        
    
    
    
    contxt = {"orders":orders, "customer_details":customer_details,"delivery_details":delivery_details,"totals":totals ,"order_id":order_id,"date":date,"org":org}
    
    return contxt
    
    
def get_sales_by_status(status):    

    sales = StoreSales.objects.filter(status=status)
    
    subtotal = round(sum([i.price for i in sales]),2)
    tax = round((subtotal*sales[0].tax)/100 if len(sales) > 0 else 0.00,2)
    total = tax  + subtotal
    total = round(total,2)
    
    if len(OrgDetails.objects.all()):
        org_details = OrgDetails.objects.all()[0]
    
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    contxt = {"sales":sales, "total":total,"tax":tax,"subtotal":subtotal,"org_details":org_details,"date":date}
    
    return contxt

def get_sales_by_id(ids_list): 
    
    sales = StoreSales.objects.filter(pk__in = ids_list)
    
    subtotal = round(sum([i.price for i in sales]),2)
    tax = round((subtotal*sales[0].tax)/100 if len(sales) > 0 else 0.00,2)
    total = tax  + subtotal
    total = round(total,2)
    
    if len(OrgDetails.objects.all()):
        org_details = OrgDetails.objects.all()[0]
    
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    contxt = {"sales":sales, "total":total,"tax":tax,"subtotal":subtotal,"org_details":org_details,"date":date}
    
    return contxt

def get_sales_summary_data(sales):
    
    qty = sum([sale.quantity for sale in sales])
    subtotal = round(sum([i.price for i in sales]),2)
    tax = round((subtotal*sales[0].tax)/100 if len(sales) > 0 else 0.00,2)
    total = tax  + subtotal
    total = round(total,2)
    
    contxt = {"sales":sales, "total":total,"tax":tax,"subtotal":subtotal,"qty":qty}
    
    return contxt
    
    

    
    

    
def calculate_profit(sales,expenses): 
    
    cost = 0
    price = 0
    
    for sale in sales: 
        
        cost+=sale.product.cost *sale.quantity
        price+=sale.price*sale.quantity
        
        
    profit = round(price - cost - expenses,2)
    
    contxt = {"cost":cost, "revenue":price,"profit":profit,"expenses":expenses}
    
    return contxt
        
    
    
    
    