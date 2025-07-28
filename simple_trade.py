import requests
import hmac
import hashlib
import time
import urllib.parse
import argparse

api_key = "vd39E0LUaYLqm4RpMSUyqXjBgpPhMhD0N0gFlUkZGChDV9SntE4QGjsKZTtImb7Q" 
secret_key= "BJpWrnknAMMkqD0ORljZKo6raWEmxr3vot6Bok5DDXH3222LxRldtRP6KK5cYeD6" 
base_url = "https://eapi.binance.com"
endpoint_path = '/eapi/v1/order'
timestamp = round(time.time()*1000)

parser = argparse.ArgumentParser(description='币安期权交易脚本')

parser.add_argument('--symbol', required=True, help='交易标的，例如: ETH-250725-3600-C')
parser.add_argument('--side', choices=['BUY', 'SELL'], required=True, help='交易方向: BUY 或 SELL')
parser.add_argument('--type', default='LIMIT', choices=['LIMIT', 'MARKET'], help='订单类型: LIMIT 或 MARKET (默认: LIMIT)')
parser.add_argument('--quantity', type=float, required=True, help='交易数量')
parser.add_argument('--price', type=float, help='价格 (LIMIT订单必须)')
parser.add_argument('--time-in-force', default='GTC', choices=['GTC', 'IOC', 'FOK'], 
                    help='订单有效期类型 (默认: GTC)')

args = parser.parse_args()

params = {
    "symbol": args.symbol,
    "side": args.side,
    "type": args.type,
    "quantity": args.quantity,
    "price": args.price, 
    "timeInForce": args.time_in_force,
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