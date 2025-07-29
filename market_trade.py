# 币安市价下单接口
# 接口: /eapi/v1/depth (公开接口，无需签名)
import requests
import argparse
import json

# 币安期权API配置
base_url = "https://eapi.binance.com"
endpoint_path = '/eapi/v1/depth'

# 命令行参数解析
parser = argparse.ArgumentParser(description='获取币安期权订单簿深度数据')
parser.add_argument('--symbol', required=True, help='期权交易对，例如: ETH-250728-3600-C')
parser.add_argument('--quantity', required=True)
parser.add_argument('--side', required=True)

args = parser.parse_args()

# 构建请求参数
params = {
    "symbol": args.symbol,
    "quantity": args.quantity,
    "side": args.side
}


waiting_qty = args.quantity
completed_qty = 0

def get_orderbook(args.symbol):
    # 命令行参数解析
    parser = argparse.ArgumentParser(description='获取币安期权订单簿深度数据')
    parser.add_argument('--symbol', required=True, help='期权交易对，例如: ETH-250728-3600-C')
    parser.add_argument('--limit', type=int, default=100, choices=[10, 20, 50, 100, 500, 1000], 
                        help='返回条目数量 (默认: 100)')

    args = parser.parse_args()

    # 构建请求参数
    params = {
        "symbol": args.symbol,
        "limit": args.limit
    }

    try:
        # 发送请求
        response = requests.get(base_url + endpoint_path, params=params, timeout=10)


    return orderbook 
# 返回像这样的数据{"bids":[["1085","14.34"],["1065","0.42"],["5","10"]],"asks":[["1175","11.74"],["1230","0.42"]],"T":1753791719929,"u":29752}%    


def send_limit_order():
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

    return order_id

def check_order(symbol,order_id):
     /eapi/v1/historyOrders
     symbol	STRING	YES	Option trading pair
orderId	LONG	NO	Returns the orderId and subsequent orders, the most recent order is returned by default
    [
    {
        "orderId": 4611922413427359795,
        "symbol": "BTC-220715-2000-C",
        "price": "18000.00000000",
        "quantity": "-0.50000000",
        "executedQty": "-0.50000000",
        "fee": "3.00000000",
        "side": "SELL",
        "type": "LIMIT",
        "timeInForce": "GTC",
        "reduceOnly": false,
        "postOnly": false,
        "createTime": 1657867694244,
        "updateTime": 1657867888216,
        "status": "FILLED",
        "reason": "0",
        "avgPrice": "18000.00000000",
        "source": "API",
        "clientOrderId": "",
        "priceScale": 2,
        "quantityScale": 2,
        "optionSide": "CALL",
        "quoteAsset": "USDT",
        "mmp": false
    }
]
     return status


     return status
    

def main():
    while completed_qty < args.quantity:
        if args.side == "B":
            print("这个程序只卖不买")
            break

        orderbook = get_orderbook(args.symbol)

        if orderbook.bids(args.symbol) == null:
            print(no bid depth)
            break

        order_qty = orderbook.bids[1]买一的数量

        if order_qty >= waiting_qty:
            qty = waiting_qty
        else:
             qty = order_qty

        # 这个函数实现比买一高五块钱的挂单
        order_id = send_limit_order(qty,symbol)
        print(下单信息)

        # 轮询看订单成交的状态
        check_order(order_id)

        if status = "Filled"订单完成
        else:
            继续轮询

        completed_qty += qty




main()
    
    

    

