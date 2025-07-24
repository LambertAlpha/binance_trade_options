#!/usr/bin/env python3
import requests
import time
import hmac
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()

def test_network_detailed():
    """详细的网络连接测试"""
    print("🌐 详细网络连接诊断")
    print("=" * 50)
    
    API_KEY = os.getenv('API_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY')
    
    # 1. 测试DNS解析
    print("1️⃣ 测试DNS解析...")
    import socket
    try:
        ip = socket.gethostbyname('vapi.binance.com')
        print(f"✅ vapi.binance.com 解析到: {ip}")
    except Exception as e:
        print(f"❌ DNS解析失败: {e}")
        return False
    
    # 2. 测试基础HTTP连接 
    print("\n2️⃣ 测试基础HTTP连接...")
    try:
        response = requests.get('https://vapi.binance.com/vapi/v1/ping', timeout=10)
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        print(f"响应内容: '{response.text}'")
        print(f"响应长度: {len(response.content)} bytes")
        
        if response.status_code == 200:
            print("✅ 基础连接正常")
        else:
            print(f"⚠️ 状态码异常: {response.status_code}")
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        return False
    
    # 3. 测试服务器时间 - 详细版
    print("\n3️⃣ 测试服务器时间（详细）...")
    try:
        response = requests.get('https://vapi.binance.com/vapi/v1/time', timeout=10)
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        print(f"原始响应: '{response.text}'")
        print(f"响应长度: {len(response.content)} bytes")
        
        if response.text.strip():
            try:
                data = response.json()
                print(f"✅ JSON解析成功: {data}")
            except Exception as json_err:
                print(f"❌ JSON解析失败: {json_err}")
        else:
            print("❌ 响应为空！")
            
    except Exception as e:
        print(f"❌ 请求失败: {e}")
    
    # 4. 测试不同的请求方式
    print("\n4️⃣ 测试不同请求配置...")
    
    # 测试不同的User-Agent
    headers_list = [
        {},
        {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'},
        {'User-Agent': 'python-requests/2.32.4'},
    ]
    
    for i, headers in enumerate(headers_list):
        print(f"\n测试配置 {i+1}: {headers}")
        try:
            response = requests.get('https://vapi.binance.com/vapi/v1/time', 
                                 headers=headers, timeout=10)
            print(f"  状态码: {response.status_code}")
            print(f"  响应长度: {len(response.content)}")
            print(f"  有内容: {'是' if response.text.strip() else '否'}")
        except Exception as e:
            print(f"  ❌ 失败: {e}")
    
    # 5. 测试账户API - 详细诊断
    print("\n5️⃣ 测试账户API（详细诊断）...")
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
            
            headers = {'X-MBX-APIKEY': API_KEY}
            
            print(f"请求URL: https://vapi.binance.com/vapi/v1/account")
            print(f"请求头: {headers}")
            print(f"请求参数: {params}")
            
            response = requests.get(
                'https://vapi.binance.com/vapi/v1/account',
                headers=headers,
                params=params,
                timeout=10
            )
            
            print(f"响应状态码: {response.status_code}")
            print(f"响应头: {dict(response.headers)}")
            print(f"原始响应: '{response.text}'")
            print(f"响应长度: {len(response.content)} bytes")
            
            if response.text.strip():
                try:
                    data = response.json()
                    print(f"✅ JSON解析成功")
                    print(f"响应数据: {data}")
                except Exception as json_err:
                    print(f"❌ JSON解析失败: {json_err}")
            else:
                print("❌ 账户API返回空响应！这就是问题所在！")
                
        except Exception as e:
            print(f"❌ 账户API测试失败: {e}")
    
    # 6. 网络诊断建议
    print("\n6️⃣ 网络诊断建议:")
    print("根据测试结果，可能的解决方案：")
    print("• 如果ping正常但时间/账户API返回空，可能是:")
    print("  - 网络代理问题")
    print("  - ISP对Binance的限制")
    print("  - 防火墙拦截")
    print("• 尝试使用VPN或更换网络环境")
    print("• 检查系统代理设置")

if __name__ == "__main__":
    test_network_detailed() 