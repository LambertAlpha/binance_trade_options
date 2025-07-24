#!/usr/bin/env python3
import hmac
import hashlib
import requests
import time
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 从环境变量获取配置
API_KEY = os.getenv('API_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')

# 验证必要的配置
if not API_KEY:
    raise ValueError("请在 .env 文件中设置 API_KEY")

if not SECRET_KEY:
    raise ValueError("请在 .env 文件中设置 SECRET_KEY")

# 设置期权交易请求参数
params = {
    'symbol':       os.getenv('SYMBOL', 'BTC-200730-9000-C'),  # 期权交易对，例如：BTC-200730-9000-C
    'side':         os.getenv('SIDE', 'BUY'),                   # 买卖方向：SELL, BUY
    'type':         os.getenv('TYPE', 'LIMIT'),                 # 订单类型：LIMIT (期权只支持限价单)
    'quantity':     os.getenv('QUANTITY', '1'),                 # 订单数量
    'price':        os.getenv('PRICE', '100'),                  # 订单价格
    'timeInForce':  os.getenv('TIME_IN_FORCE', 'GTC'),          # 订单有效期（默认GTC）
    'reduceOnly':   os.getenv('REDUCE_ONLY', 'false'),          # 是否仅减仓（默认false）
    'postOnly':     os.getenv('POST_ONLY', 'false'),            # 是否仅挂单（默认false）
    'newOrderRespType': os.getenv('NEW_ORDER_RESP_TYPE', 'ACK'), # 响应类型：ACK, RESULT
    'clientOrderId': os.getenv('CLIENT_ORDER_ID', ''),          # 用户自定义订单ID
    'isMmp':        os.getenv('IS_MMP', 'false'),               # 是否做市商保护订单
    'recvWindow':   os.getenv('RECV_WINDOW', '5000'),           # 接收窗口
}

# 移除空值参数
params = {k: v for k, v in params.items() if v != ''}

# 参数中加时间戳
timestamp = int(time.time() * 1000)  # 以毫秒为单位的 UNIX 时间戳
params['timestamp'] = timestamp

# 生成签名
query_string = '&'.join([f'{param}={value}' for param, value in params.items()])
signature = hmac.new(
    SECRET_KEY.encode('utf-8'),
    query_string.encode('utf-8'),
    hashlib.sha256
).hexdigest()
params['signature'] = signature

# 发送请求
headers = {
    'X-MBX-APIKEY': API_KEY,
}

try:
    print("发送期权交易请求...")
    print(f"交易对: {params['symbol']}")
    print(f"方向: {params['side']}")
    print(f"数量: {params['quantity']}")
    print(f"价格: {params['price']}")
    
    response = requests.post(
        'https://vapi.binance.com/vapi/v1/order',
        headers=headers,
        data=params,
    )
    
    if response.status_code in [200, 202]:
        result = response.json()
        print(f"✅ 期权交易请求成功 (状态码: {response.status_code}):")
        print(f"订单ID: {result.get('orderId', 'N/A')}")
        print(f"交易对: {result.get('symbol', 'N/A')}")
        print(f"价格: {result.get('price', 'N/A')}")
        print(f"数量: {result.get('quantity', 'N/A')}")
        print(f"方向: {result.get('side', 'N/A')}")
        print(f"类型: {result.get('type', 'N/A')}")
        print(f"创建时间: {result.get('createDate', result.get('createTime', 'N/A'))}")
        
        # 如果是RESULT响应类型，显示更多信息
        if params.get('newOrderRespType') == 'RESULT':
            print(f"已执行数量: {result.get('executedQty', 'N/A')}")
            print(f"手续费: {result.get('fee', 'N/A')}")
            print(f"订单状态: {result.get('status', 'N/A')}")
            print(f"平均价格: {result.get('avgPrice', 'N/A')}")
            print(f"期权类型: {result.get('optionSide', 'N/A')}")
            print(f"计价资产: {result.get('quoteAsset', 'N/A')}")
    else:
        print(f"❌ 期权交易请求失败，状态码: {response.status_code}")
        print(f"错误信息: {response.text}")
        
except requests.exceptions.RequestException as e:
    print(f"❌ 网络请求错误: {e}")
except Exception as e:
    print(f"❌ 发生未知错误: {e}")