#!/usr/bin/env python3
import hmac
import hashlib
import requests
import time
import os
import json
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

def create_session():
    """创建一个配置了完整请求头的会话"""
    session = requests.Session()
    
    # 模拟浏览器请求头，绕过WAF检测
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
    })
    
    return session

def make_signed_request(session, method, url, params=None, data=None):
    """发送签名请求，包含完整的错误处理"""
    try:
        print(f"📡 发送请求到: {url}")
        print(f"🔧 方法: {method}")
        print(f"📋 参数: {params or data}")
        
        if method.upper() == 'GET':
            response = session.get(url, params=params, timeout=30)
        else:
            response = session.post(url, data=data, timeout=30)
        
        print(f"📊 响应状态码: {response.status_code}")
        print(f"📏 响应长度: {len(response.content)} bytes")
        print(f"🔍 响应头信息:")
        for key, value in response.headers.items():
            if key.lower() in ['x-amzn-waf-action', 'x-cache', 'server']:
                print(f"    {key}: {value}")
        
        # 检查WAF拦截
        if response.headers.get('x-amzn-waf-action') == 'challenge':
            print("❌ 请求被AWS WAF拦截！")
            print("💡 建议解决方法:")
            print("   1. 使用VPN更换IP地址")
            print("   2. 降低请求频率")
            print("   3. 联系Binance客服申请API白名单")
            return None
        
        # 检查响应内容
        if not response.content.strip():
            print("❌ 收到空响应")
            print(f"原始响应: '{response.text}'")
            return None
        
        # 尝试JSON解析
        try:
            return response.json()
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析失败: {e}")
            print(f"原始响应内容: {response.text[:500]}")
            return None
            
    except requests.exceptions.Timeout:
        print("❌ 请求超时")
        return None
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败")
        return None
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return None

def place_option_order():
    """下单期权交易"""
    # 创建会话
    session = create_session()
    
    # 设置期权交易请求参数
    params = {
        'symbol':       os.getenv('SYMBOL', 'ETH-250725-3600-C'),
        'side':         os.getenv('SIDE', 'BUY'),
        'type':         os.getenv('TYPE', 'LIMIT'),
        'quantity':     os.getenv('QUANTITY', '0.1'),
        'price':        os.getenv('PRICE', '55'),
        'timeInForce':  os.getenv('TIME_IN_FORCE', 'GTC'),
        'reduceOnly':   os.getenv('REDUCE_ONLY', 'false'),
        'postOnly':     os.getenv('POST_ONLY', 'false'),
        'newOrderRespType': os.getenv('NEW_ORDER_RESP_TYPE', 'ACK'),
        'clientOrderId': os.getenv('CLIENT_ORDER_ID', ''),
        'isMmp':        os.getenv('IS_MMP', 'false'),
        'recvWindow':   os.getenv('RECV_WINDOW', '5000'),
    }
    
    # 移除空值参数
    params = {k: v for k, v in params.items() if v != ''}
    
    # 参数中加时间戳
    timestamp = int(time.time() * 1000)
    params['timestamp'] = timestamp
    
    # 生成签名
    query_string = '&'.join([f'{param}={value}' for param, value in params.items()])
    signature = hmac.new(
        SECRET_KEY.encode('utf-8'),
        query_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    params['signature'] = signature
    
    # 设置API密钥头
    session.headers['X-MBX-APIKEY'] = API_KEY
    
    print("🚀 发送期权交易请求...")
    print(f"交易对: {params['symbol']}")
    print(f"方向: {params['side']}")
    print(f"数量: {params['quantity']}")
    print(f"价格: {params['price']}")
    
    # 发送请求
    result = make_signed_request(
        session=session,
        method='POST',
        url='https://vapi.binance.com/vapi/v1/order',
        data=params
    )
    
    if result:
        print(f"✅ 期权交易请求成功:")
        print(f"订单ID: {result.get('orderId', 'N/A')}")
        print(f"交易对: {result.get('symbol', 'N/A')}")
        print(f"价格: {result.get('price', 'N/A')}")
        print(f"数量: {result.get('quantity', 'N/A')}")
        print(f"方向: {result.get('side', 'N/A')}")
        print(f"类型: {result.get('type', 'N/A')}")
        print(f"创建时间: {result.get('createDate', result.get('createTime', 'N/A'))}")
        return True
    else:
        print("❌ 期权交易请求失败")
        return False

def test_waf_bypass():
    """测试WAF绕过效果"""
    print("🧪 测试WAF绕过效果...")
    session = create_session()
    
    # 测试服务器时间
    print("\n1️⃣ 测试服务器时间...")
    result = make_signed_request(session, 'GET', 'https://vapi.binance.com/vapi/v1/time')
    if result:
        print(f"✅ 服务器时间获取成功: {result}")
    
    # 测试账户信息
    print("\n2️⃣ 测试账户信息...")
    timestamp = int(time.time() * 1000)
    params = {
        'timestamp': timestamp,
        'recvWindow': 5000
    }
    
    query_string = '&'.join([f'{k}={v}' for k, v in params.items()])
    signature = hmac.new(
        SECRET_KEY.encode('utf-8'),
        query_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    params['signature'] = signature
    
    session.headers['X-MBX-APIKEY'] = API_KEY
    result = make_signed_request(session, 'GET', 'https://vapi.binance.com/vapi/v1/account', params=params)
    
    if result:
        print(f"✅ 账户信息获取成功")
        return True
    else:
        print("❌ 账户信息获取失败")
        return False

if __name__ == "__main__":
    print("🔧 使用改进的请求方法...")
    
    # 先测试WAF绕过
    if test_waf_bypass():
        print("\n" + "="*50)
        print("✅ WAF绕过测试成功，开始交易...")
        place_option_order()
    else:
        print("\n❌ WAF绕过失败，请尝试以下解决方案:")
        print("1. 🌐 使用VPN更换IP地址")
        print("2. ⏰ 降低请求频率，增加延迟")
        print("3. 📞 联系Binance客服申请API白名单")
        print("4. 🔄 尝试使用不同的网络环境") 