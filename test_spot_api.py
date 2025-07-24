#!/usr/bin/env python3
import requests
import hmac
import hashlib
import time
import os
from dotenv import load_dotenv

load_dotenv()

def test_spot_api():
    """测试现货API是否也被WAF拦截"""
    print("🔍 测试现货API连接...")
    
    API_KEY = os.getenv('API_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY')
    
    # 创建会话
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Connection': 'keep-alive',
    })
    
    # 1. 测试现货公开API
    print("\n1️⃣ 测试现货公开API...")
    try:
        response = session.get('https://api.binance.com/api/v3/ping', timeout=10)
        print(f"现货ping状态码: {response.status_code}")
        print(f"响应内容: '{response.text}'")
        if response.headers.get('x-amzn-waf-action'):
            print(f"WAF状态: {response.headers.get('x-amzn-waf-action')}")
        else:
            print("✅ 现货API未被WAF拦截")
    except Exception as e:
        print(f"❌ 现货ping失败: {e}")
    
    # 2. 测试现货服务器时间
    print("\n2️⃣ 测试现货服务器时间...")
    try:
        response = session.get('https://api.binance.com/api/v3/time', timeout=10)
        print(f"现货时间状态码: {response.status_code}")
        print(f"响应长度: {len(response.content)} bytes")
        if response.content.strip():
            data = response.json()
            print(f"✅ 现货时间获取成功: {data}")
        else:
            print("❌ 现货时间响应为空")
    except Exception as e:
        print(f"❌ 现货时间失败: {e}")
    
    # 3. 测试现货账户信息
    print("\n3️⃣ 测试现货账户信息...")
    if API_KEY and SECRET_KEY:
        try:
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
            
            response = session.get(
                'https://api.binance.com/api/v3/account',
                params=params,
                timeout=10
            )
            
            print(f"现货账户状态码: {response.status_code}")
            print(f"响应长度: {len(response.content)} bytes")
            
            if response.headers.get('x-amzn-waf-action'):
                print(f"❌ 现货账户也被WAF拦截: {response.headers.get('x-amzn-waf-action')}")
            elif response.content.strip():
                data = response.json()
                print(f"✅ 现货账户信息获取成功")
                # 显示余额
                balances = data.get('balances', [])
                non_zero = [b for b in balances if float(b.get('free', 0)) > 0 or float(b.get('locked', 0)) > 0]
                print(f"非零余额资产数量: {len(non_zero)}")
            else:
                print("❌ 现货账户响应为空")
                
        except Exception as e:
            print(f"❌ 现货账户测试失败: {e}")

def compare_endpoints():
    """对比不同端点的行为"""
    print("\n🔄 对比分析:")
    print("=" * 50)
    
    endpoints = [
        ('现货ping', 'https://api.binance.com/api/v3/ping'),
        ('期权ping', 'https://vapi.binance.com/vapi/v1/ping'),
        ('现货时间', 'https://api.binance.com/api/v3/time'),
        ('期权时间', 'https://vapi.binance.com/vapi/v1/time'),
    ]
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    })
    
    for name, url in endpoints:
        print(f"\n📊 {name}: {url}")
        try:
            response = session.get(url, timeout=10)
            waf_action = response.headers.get('x-amzn-waf-action', 'none')
            has_content = 'Yes' if response.content.strip() else 'No'
            
            print(f"   状态码: {response.status_code}")
            print(f"   WAF状态: {waf_action}")
            print(f"   有内容: {has_content}")
            
            if waf_action == 'challenge':
                print(f"   ❌ 被WAF拦截")
            elif has_content == 'Yes':
                print(f"   ✅ 正常")
            else:
                print(f"   ⚠️  异常")
                
        except Exception as e:
            print(f"   ❌ 请求失败: {e}")

if __name__ == "__main__":
    test_spot_api()
    compare_endpoints()
    
    print(f"\n💡 结论分析:")
    print("如果现货API正常而期权API被拦截，说明:")
    print("1. 你的IP地址和API密钥都是正常的")
    print("2. 问题特定于期权API端点")
    print("3. 可能是期权服务的地区限制或特殊保护")
    
    print(f"\n🎯 建议解决方案:")
    print("1. 优先：联系Binance客服确认期权API可用性")
    print("2. 尝试：使用VPN连接到Binance主要服务区域（如新加坡）")
    print("3. 备选：先开发现货交易功能，等期权问题解决后迁移") 