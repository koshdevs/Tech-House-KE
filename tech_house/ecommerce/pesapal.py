import requests
from requests.auth import *
import os
import json
from dotenv import load_dotenv
load_dotenv()

def get_access_token():
    
    consumer_key = "qkio1BGGYAXTu2JOfm7XSXNruoZsrqEW"
    consumer_secret = "osGQ364R49cXKeOYSpaOnT++rHs="
    
    URL = os.getenv('PESAPAL_SANDBOX_AUTH')
    print(URL)
    
    headers = {'Accept': 'application/json', 
               'Content-Type': 'application/json', 
               }
    
    data = {
        "consumer_key": str(consumer_key),
        "consumer_secret": str(consumer_secret),
    
    }
    
    response = requests.post(URL,json.dumps(data), headers=headers)
    
    print(response.json())
    
    if response.status_code == 200:
        print(f'Access token: {response.json()["token"]}')
    else:
        print(f'Access token failed. Error: {response.json()["error"]}')
        
    return response.json()["token"]
    
def register_ipn(): 
    
    headers = {'Accept': 'application/json', 
               'Content-Type': 'application/json', 
               'Authorization': f'Bearer {get_access_token()}'
               }
    
    URL = os.getenv('PESAPAL_SANDBOX_REGISTER_IPN')
    
    
    
    data = {
    "url": "http://192.168.1.3:8080/ipn",
    "ipn_notification_type": "GET",

   }
    
    response = requests.post(URL,json.dumps(data), headers=headers)
    
    print(response.json())
    
    if response.status_code == 200:
        print(f'IPN registration successful. IPN URL: {response.json()["ipn_id"]}')
    else:
        print(f'IPN registration failed. Error: {response.json()["error"]}')
        
        
        
    return response.json()["ipn_id"]
    
    
    
def payment_request_page(data):
    
    
    URL = os.getenv('PESAPAL_SANDBOX_SUBMIT_ORDER')
    
    headers = {'Accept': 'application/json', 
               'Content-Type': 'application/json',
               'Authorization': f'Bearer {get_access_token()}'}
    
    

    response = requests.post(URL,json.dumps(data), headers=headers)
    
    print(response.json())
    if response.status_code == 200:
       
        print(f'Redirect to: {response.json()["redirect_url"]}')
    else:
        print(f'Payment failed. Error: {response.json()["error"]}')
        
        
        
    return response.json()
    
    
    
    