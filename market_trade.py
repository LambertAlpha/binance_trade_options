# 币安期权市价卖单程序 - 贴卖一卖（比卖一便宜挂单）
# python market_trade.py --symbol ETH-250728-3600-C --quantity 0.1 --discount 2.0
# python market_trade.py --symbol ETH-250730-3700-P \
# --quantity 1 \
# --discount 2
import requests
import argparse
import json
import time
import hmac
import hashlib
import urllib.parse
from datetime import datetime

# 币安期权API配置
BASE_URL = "https://eapi.binance.com"
ORDERBOOK_ENDPOINT = '/eapi/v1/depth'
ORDER_ENDPOINT = '/eapi/v1/order'
OPEN_ORDERS_ENDPOINT = '/eapi/v1/openOrders'
HISTORY_ORDERS_ENDPOINT = '/eapi/v1/historyOrders'

# API密钥配置 - 请填入你的实际密钥
API_KEY = ""  # 请替换为你的实际API Key
SECRET_KEY = ""  # 请替换为你的实际Secret Key

def get_timestamp():
    """获取当前时间戳"""
    return int(time.time() * 1000)

def create_signature(query_string, secret_key):
    """创建签名"""
    return hmac.new(
        secret_key.encode('utf-8'),
        query_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

def get_orderbook(symbol, limit=100):
    """获取订单簿深度数据"""
    params = {
        "symbol": symbol,
        "limit": limit
    }
    
    try:
        response = requests.get(BASE_URL + ORDERBOOK_ENDPOINT, params=params, timeout=10)
        response.raise_for_status()
        orderbook = response.json()
        
        if 'bids' not in orderbook or 'asks' not in orderbook:
            print(f"获取订单簿失败: {orderbook}")
            return None
            
        return orderbook
        
    except requests.exceptions.RequestException as e:
        print(f"获取订单簿失败: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"解析订单簿数据失败: {e}")
        return None

def send_limit_order(symbol, side, quantity, price):
    """发送限价订单"""
    timestamp = get_timestamp()
    
    params = {
        "symbol": symbol,
        "side": side,
        "type": "LIMIT",
        "quantity": str(quantity),
        "price": str(price),
        "timeInForce": "GTC",
        "timestamp": timestamp
    }
    
    # 创建查询字符串和签名
    query_string = urllib.parse.urlencode(params)
    signature = create_signature(query_string, SECRET_KEY)
    
    # 构建完整URL
    url = f"{BASE_URL}{ORDER_ENDPOINT}?{query_string}&signature={signature}"
    
    headers = {
        'X-MBX-APIKEY': API_KEY,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    try:
        response = requests.post(url, headers=headers, timeout=10)
        response.raise_for_status()
        order_result = response.json()
        
        if 'orderId' in order_result:
            print(f"下单成功! 订单ID: {order_result['orderId']}, 价格: {price}, 数量: {quantity}")
            return order_result['orderId']
        else:
            print(f"下单失败: {order_result}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"下单请求失败: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"解析下单响应失败: {e}")
        return None

def check_order_status(symbol, order_id):
    """查询订单状态 - 先查开放订单，再查历史订单"""
    timestamp = get_timestamp()
    
    # 第一步: 查询开放订单 (活跃状态: ACCEPTED, PARTIALLY_FILLED)
    params = {
        "symbol": symbol,
        "timestamp": timestamp
    }
    
    query_string = urllib.parse.urlencode(params)
    signature = create_signature(query_string, SECRET_KEY)
    
    url = f"{BASE_URL}{OPEN_ORDERS_ENDPOINT}?{query_string}&signature={signature}"
    
    headers = {
        'X-MBX-APIKEY': API_KEY
    }
    
    try:
        # 查询开放订单
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        open_orders = response.json()
        
        # 在开放订单中查找
        for order in open_orders:
            if order['orderId'] == order_id:
                status = order['status']
                executed_qty = float(order['executedQty'])
                print(f"订单在开放列表中: 状态={status}, 已成交={executed_qty}")
                return status, executed_qty
        
        # 第二步: 如果不在开放订单中，查询历史订单 (完成状态: FILLED, CANCELLED, REJECTED)
        print(f"订单不在开放列表中，查询历史订单...")
        
        history_params = {
            "symbol": symbol,
            "orderId": order_id,
            "timestamp": get_timestamp()  # 重新获取时间戳
        }
        
        history_query_string = urllib.parse.urlencode(history_params)
        history_signature = create_signature(history_query_string, SECRET_KEY)
        
        history_url = f"{BASE_URL}{HISTORY_ORDERS_ENDPOINT}?{history_query_string}&signature={history_signature}"
        
        history_response = requests.get(history_url, headers=headers, timeout=10)
        history_response.raise_for_status()
        history_orders = history_response.json()
        
        # 在历史订单中查找
        for order in history_orders:
            if order['orderId'] == order_id:
                status = order['status']
                executed_qty = float(order['executedQty'])
                
                # 如果订单被拒绝，显示拒绝原因
                if status == "REJECTED":
                    reject_reason = order.get('reason', '未知原因')
                    print(f"订单在历史列表中: 状态={status}, 已成交={executed_qty}, 拒绝原因={reject_reason}")
                else:
                    print(f"订单在历史列表中: 状态={status}, 已成交={executed_qty}")
                
                return status, executed_qty
        
        # 如果两个地方都找不到，可能是订单ID错误或网络问题s
        print(f"警告: 订单ID {order_id} 在开放订单和历史订单中都未找到")
        return None, 0
        
    except requests.exceptions.RequestException as e:
        print(f"查询订单状态失败: {e}")
        return None, 0
    except json.JSONDecodeError as e:
        print(f"解析订单状态响应失败: {e}")
        return None, 0

def main():
    # 命令行参数解析
    parser = argparse.ArgumentParser(description='币安期权贴卖一卖程序')
    parser.add_argument('--symbol', required=True, help='期权交易对，例如: ETH-250728-3600-C')
    parser.add_argument('--quantity', type=float, required=True, help='总卖出数量')
    parser.add_argument('--side', default='SELL', help='交易方向(默认: SELL)')
    parser.add_argument('--discount', type=float, default=5.0, help='相对卖一的折扣(默认: 5.0)')
    
    args = parser.parse_args()
    
    # 检查API密钥配置
    if API_KEY == "your_api_key_here" or SECRET_KEY == "your_secret_key_here":
        print("错误: 请先配置你的API密钥!")
        print("请在代码中将API_KEY和SECRET_KEY替换为你的实际密钥")
        return
    
    # 检查是否为卖单
    if args.side.upper() != "SELL":
        print("这个程序只支持卖出(SELL)操作")
        return
    
    completed_qty = 0.0
    
    print(f"开始执行期权卖出程序")
    print(f"交易对: {args.symbol}")
    print(f"总数量: {args.quantity}")
    print(f"折扣: {args.discount}")
    print("-" * 50)
    
    while completed_qty < args.quantity:
        remaining_qty = args.quantity - completed_qty
        print(f"剩余待卖数量: {remaining_qty}")
        
        # 获取订单簿
        orderbook = get_orderbook(args.symbol)
        if not orderbook or not orderbook.get('bids') or not orderbook.get('asks'):
            print("无法获取订单簿或无买卖单深度，等待5秒后重试...")
            time.sleep(5)
            continue
        
        # 获取买一和卖一价格数量
        best_bid_price = float(orderbook['bids'][0][0])
        best_bid_qty = float(orderbook['bids'][0][1])
        best_ask_price = float(orderbook['asks'][0][0])
        best_ask_qty = float(orderbook['asks'][0][1])
        
        print(f"当前买一: 价格={best_bid_price}, 数量={best_bid_qty}")
        print(f"当前卖一: 价格={best_ask_price}, 数量={best_ask_qty}")
        
        if best_ask_qty == 0:
            print("卖一数量为0，等待5秒后重试...")
            time.sleep(5)
            continue
        
        # 计算挂单价格（比卖一便宜指定折扣）
        calculated_price = best_ask_price - args.discount
        
        # 检查价格逻辑：如果计算价格等于或比买一便宜，直接挂卖一
        if calculated_price <= best_bid_price:
            order_price = best_ask_price
            print(f"计算价格{calculated_price}过低（≤买一{best_bid_price}），直接挂卖一价格: {order_price}")
        else:
            order_price = calculated_price
            print(f"挂单价格: {order_price} (卖一{best_ask_price} - 折扣{args.discount})")
        
        # 计算本次挂单数量（不超过卖一数量和剩余数量）
        order_qty = min(best_ask_qty, remaining_qty)
        
        print(f"挂单信息: 价格={order_price}, 数量={order_qty}")
        
        # 发送限价卖单
        order_id = send_limit_order(args.symbol, "SELL", order_qty, order_price)
        
        if not order_id:
            print("下单失败，等待5秒后重试...")
            time.sleep(5)
            continue
        
        # 轮询订单状态
        print("开始监控订单状态...")
        while True:
            status, executed_qty = check_order_status(args.symbol, order_id)
            
            if status is None:
                print("查询订单状态失败，等待3秒后重试...")
                time.sleep(3)
                continue
            
            if status == "FILLED":
                print(f"订单完全成交! 成交数量: {order_qty}")
                completed_qty += order_qty
                break
            elif status == "PARTIALLY_FILLED":
                print(f"订单部分成交, 已成交: {executed_qty}")
                # 可以选择继续等待或取消订单重新挂单
                time.sleep(2)
            elif status == "ACCEPTED":
                print("订单已接受，等待成交...")
                time.sleep(2)
            else:
                print(f"订单状态: {status}, 退出监控")
                break
        
        print(f"当前已完成数量: {completed_qty}/{args.quantity}")
        print("-" * 50)
        
        # 避免过于频繁的请求
        time.sleep(1)
    
    print(f"程序执行完成! 总成交数量: {completed_qty}")

if __name__ == "__main__":
    main()