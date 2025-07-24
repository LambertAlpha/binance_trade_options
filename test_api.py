#!/usr/bin/env python3
import os
import requests
import hmac
import hashlib
import time
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def test_api_connection():
    """测试API连接和密钥配置"""
    API_KEY = os.getenv('API_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY')
    
    print("🔍 测试Binance期权API连接...")
    print("=" * 50)
    
    # 检查API密钥配置
    if not API_KEY or API_KEY == 'your_api_key_here' or API_KEY == 'example':
        print("❌ API_KEY 未正确配置")
        print("请在 .env 文件中设置正确的 API_KEY")
        return False
    
    if not SECRET_KEY or SECRET_KEY == 'your_secret_key_here' or SECRET_KEY == 'example':
        print("❌ SECRET_KEY 未正确配置")
        print("请在 .env 文件中设置正确的 SECRET_KEY")
        return False
    
    print(f"✅ API_KEY: {API_KEY[:8]}...{API_KEY[-8:]}")
    print(f"✅ SECRET_KEY: {SECRET_KEY[:8]}...{SECRET_KEY[-8:]}")
    
    # 1. 测试公开端点（不需要API密钥）
    print("\n📡 测试公开端点...")
    try:
        response = requests.get('https://vapi.binance.com/vapi/v1/ping', timeout=10)
        if response.status_code in [200, 202]:
            print("✅ 公开API连接成功")
        else:
            print(f"❌ 公开API连接失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 网络连接失败: {e}")
        return False
    
    # 2. 测试服务器时间
    print("\n⏰ 测试服务器时间...")
    try:
        response = requests.get('https://vapi.binance.com/vapi/v1/time', timeout=10)
        if response.status_code in [200, 202]:
            if response.content.strip():  # 检查是否有内容
                try:
                    data = response.json()
                    server_time = data.get('data', 0)
                    local_time = int(time.time() * 1000)
                    time_diff = abs(server_time - local_time)
                    
                    print(f"✅ 服务器时间获取成功")
                    print(f"   时间差: {time_diff}ms")
                    
                    if time_diff > 5000:
                        print("⚠️  时间差过大，可能影响签名验证")
                except:
                    print("⚠️  服务器时间响应格式异常")
            else:
                print("⚠️  服务器时间响应为空")
        else:
            print(f"❌ 获取服务器时间失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 获取服务器时间出错: {e}")
    
    # 3. 测试需要API密钥的端点
    print("\n🔐 测试需要API密钥的端点...")
    try:
        headers = {
            'X-MBX-APIKEY': API_KEY,
        }
        
        # 测试账户信息（需要签名）
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
        
        response = requests.get(
            'https://vapi.binance.com/vapi/v1/account',
            headers=headers,
            params=params,
            timeout=10
        )
        
        print(f"账户信息请求状态码: {response.status_code}")
        
        if response.status_code in [200, 202]:
            if response.content.strip():
                try:
                    data = response.json()
                    if data.get('code') == 0:
                        print("✅ API密钥验证成功！")
                        
                        # 显示账户信息
                        account_data = data.get('data', [])
                        if account_data:
                            for asset in account_data:
                                currency = asset.get('currency', 'N/A')
                                balance = asset.get('balance', 'N/A')
                                available = asset.get('available', 'N/A')
                                print(f"   {currency}: 余额={balance}, 可用={available}")
                        return True
                    else:
                        print(f"❌ API返回错误: {data.get('msg', 'Unknown error')}")
                        return False
                except Exception as e:
                    print(f"❌ 解析响应失败: {e}")
                    print(f"原始响应: {response.text[:200]}...")
                    return False
        elif response.status_code == 401:
            print("❌ API密钥验证失败 (401 Unauthorized)")
            print("请检查API密钥是否正确")
            return False
        elif response.status_code == 403:
            print("❌ API权限不足 (403 Forbidden)")
            print("请检查API密钥是否有期权交易权限")
            return False
        else:
            print(f"❌ API请求失败: {response.status_code}")
            print(f"响应内容: {response.text[:200]}...")
            return False
            
    except Exception as e:
        print(f"❌ API测试出错: {e}")
        return False

def get_simple_option_info():
    """获取简单的期权信息用于测试"""
    API_KEY = os.getenv('API_KEY')
    
    if not API_KEY:
        print("❌ 需要API密钥才能获取期权信息")
        return
    
    print("\n📊 获取期权基本信息...")
    try:
        headers = {'X-MBX-APIKEY': API_KEY}
        
        # 尝试获取期权信息（可能需要特殊权限）
        response = requests.get(
            'https://vapi.binance.com/vapi/v1/optionInfo',
            headers=headers,
            timeout=10
        )
        
        print(f"期权信息请求状态码: {response.status_code}")
        
        if response.status_code in [200, 202]:
            if response.content.strip():
                try:
                    data = response.json()
                    if data.get('code') == 0:
                        options = data.get('data', [])
                        print(f"✅ 找到 {len(options)} 个期权合约")
                        
                        # 显示前几个期权
                        for i, option in enumerate(options[:3]):
                            symbol = option.get('symbol', 'N/A')
                            strike = option.get('strikePrice', 'N/A')
                            side = option.get('side', 'N/A')
                            min_qty = option.get('minQty', 'N/A')
                            
                            print(f"   {i+1}. {symbol}")
                            print(f"      行权价: {strike}")
                            print(f"      类型: {'看涨' if side == 'CALL' else '看跌'}")
                            print(f"      最小数量: {min_qty}")
                            
                        if options:
                            recommended = options[0]
                            print(f"\n💡 推荐测试合约: {recommended.get('symbol')}")
                            print(f"   最小数量: {recommended.get('minQty')}")
                            print(f"   建议测试价格: 1.0 USDT (低价测试)")
                            
                    else:
                        print(f"❌ 获取期权信息失败: {data.get('msg')}")
                except Exception as e:
                    print(f"❌ 解析期权信息失败: {e}")
            else:
                print("⚠️  期权信息响应为空")
        else:
            print(f"❌ 无法获取期权信息: {response.status_code}")
            print("可能原因:")
            print("1. 你的地区不支持期权交易")
            print("2. API密钥没有期权交易权限")
            print("3. 需要完成期权交易的资格认证")
            
    except Exception as e:
        print(f"❌ 获取期权信息出错: {e}")

if __name__ == "__main__":
    success = test_api_connection()
    
    if success:
        get_simple_option_info()
        
        print("\n🎯 下一步:")
        print("1. 如果看到期权合约信息，可以选择一个进行测试")
        print("2. 更新 .env 文件中的 SYMBOL、QUANTITY、PRICE")
        print("3. 运行 python trade.py 进行小额测试交易")
    else:
        print("\n❌ API连接测试失败，请:")
        print("1. 检查网络连接")
        print("2. 确认API密钥配置正确")
        print("3. 确认API密钥有必要的权限")
        print("4. 检查Binance是否在你的地区提供期权服务") 