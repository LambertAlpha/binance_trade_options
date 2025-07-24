import requests
import hmac
import hashlib
import time
import urllib.parse

api_key = "" 
secret_key= "" 
base_url = "https://eapi.binance.com"
endpoint_path = '/eapi/v1/order'
timestamp = round(time.time()*1000)
params = {
    "symbol": "ETH-250725-3600-C",
    "side": "BUY",
    "type": "LIMIT",
    "quantity": 0.1,
    "price": 55, 
    "timeInForce": "GTC",
    "timestamp": timestamp
}

querystring = urllib.parse.urlencode(params)
signature = hmac.new(secret_key.encode('utf-8'),msg = querystring.encode('utf-8'), digestmod = hashlib.sha256).hexdigest()
url = base_url + endpoint_path + "?" + querystring + "&signature=" + signature
print(url)

payload = {}
headers= {
    'X-MBX-APIKEY': api_key
}

response = requests.request("POST",url, headers=headers, data = payload)
print(response.status_code)
print(response.text)