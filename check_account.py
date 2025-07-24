#!/usr/bin/env python3
import os
import requests
import hmac
import hashlib
import time
from dotenv import load_dotenv
import json

load_dotenv()

def check_proxy_and_network():
    """检查网络和代理设置"""
    print("🌐 网络和代理检查")
    print("=" * 40)
    
    # 检查本地IP
    print("📍 检查当前IP地址...")
    try:
        # 使用多个服务检查IP
        ip_services = [
            'https://api.ipify.org?format=json',
            'https://httpbin.org/ip',
            'https://api.myip.com'
        ]
        
        for service in ip_services:
            try:
                response = requests.get(service, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    ip = data.get('ip') or data.get('origin') or data.get('IP')
                    print(f"✅ 当前IP: {ip}")
                    
                    # 简单的地区判断
                    if service == 'https://api.myip.com':
                        country = data.get('country')
                        if country:
                            print(f"   地区: {country}")
                    break
            except:
                continue
    except Exception as e:
        print(f"❌ 无法获取IP信息: {e}")
    
    # 检查代理设置
    print(f"\n🔧 检查代理环境变量:")
    proxy_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy']
    proxy_found = False
    
    for var in proxy_vars:
        value = os.environ.get(var)
        if value:
            proxy_found = True
            print(f"   {var}: {value}")
    
    if not proxy_found:
        print("   ℹ️  未检测到代理环境变量")
        print("   💡 如果使用VPN，可能是系统级代理")

def get_detailed_balance():
    """获取详细的账户余额和价值"""
    API_KEY = os.getenv('API_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY')
    
    print(f"\n💰 详细账户余额分析")
    print("=" * 40)
    
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
        
        # 获取账户信息
        response = requests.get(
            'https://api.binance.com/api/v3/account',
            headers=headers,
            params=params,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            balances = data.get('balances', [])
            
            # 获取主要币种的价格
            major_assets = {}
            price_response = requests.get('https://api.binance.com/api/v3/ticker/price')
            if price_response.status_code == 200:
                prices = {item['symbol']: float(item['price']) for item in price_response.json()}
                
                # 计算有价值的资产
                valuable_assets = []
                total_usdt_value = 0
                
                for balance in balances:
                    asset = balance['asset']
                    free = float(balance.get('free', 0))
                    locked = float(balance.get('locked', 0))
                    total = free + locked
                    
                    if total > 0:
                        # 计算USDT价值
                        usdt_value = 0
                        if asset == 'USDT':
                            usdt_value = total
                        elif asset == 'USDC' or asset == 'BUSD':
                            usdt_value = total  # 假设1:1
                        else:
                            # 尝试获取对USDT的价格
                            symbol_variations = [f"{asset}USDT", f"{asset}BUSD", f"{asset}USDC"]
                            for symbol in symbol_variations:
                                if symbol in prices:
                                    usdt_value = total * prices[symbol]
                                    break
                        
                        if usdt_value > 0.01:  # 价值超过0.01 USDT的资产
                            valuable_assets.append({
                                'asset': asset,
                                'free': free,
                                'locked': locked,
                                'total': total,
                                'usdt_value': usdt_value
                            })
                            total_usdt_value += usdt_value
                
                # 按价值排序
                valuable_assets.sort(key=lambda x: x['usdt_value'], reverse=True)
                
                print(f"💎 有价值的资产 (总价值: ${total_usdt_value:.2f}):")
                for asset_info in valuable_assets:
                    asset = asset_info['asset']
                    free = asset_info['free']
                    locked = asset_info['locked']
                    usdt_value = asset_info['usdt_value']
                    
                    print(f"   {asset}: {free:.8f} (价值: ${usdt_value:.2f})")
                    if locked > 0:
                        print(f"      冻结: {locked:.8f}")
                
                # 分析资金充足性
                print(f"\n📊 资金分析:")
                print(f"   总资产价值: ${total_usdt_value:.2f}")
                
                if total_usdt_value >= 1000:
                    print("   ✅ 资金充足，可以进行期权交易")
                elif total_usdt_value >= 100:
                    print("   ⚠️  资金中等，可以小额测试")
                else:
                    print("   ❌ 资金较少，可能影响期权交易")
                
                # 检查稳定币余额
                stable_coins = ['USDT', 'USDC', 'BUSD', 'FDUSD']
                stable_balance = sum(asset_info['usdt_value'] for asset_info in valuable_assets 
                                   if asset_info['asset'] in stable_coins)
                
                print(f"   稳定币余额: ${stable_balance:.2f}")
                
                if stable_balance < 10:
                    print("   💡 建议：转换一些资产为USDT用于期权交易")
                
                return total_usdt_value >= 100
                
        else:
            print(f"❌ 获取账户信息失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 获取余额失败: {e}")
        return False

def check_futures_account():
    """检查合约账户余额"""
    API_KEY = os.getenv('API_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY')
    
    print(f"\n📈 合约账户检查")
    print("=" * 30)
    
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
        
        # 检查USDT-M合约账户
        response = requests.get(
            'https://fapi.binance.com/fapi/v2/account',
            headers=headers,
            params=params,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            total_wallet_balance = data.get('totalWalletBalance', '0')
            available_balance = data.get('availableBalance', '0')
            
            print(f"✅ USDT-M合约账户:")
            print(f"   总余额: {total_wallet_balance} USDT")
            print(f"   可用余额: {available_balance} USDT")
            
            return float(available_balance) > 0
            
        else:
            print(f"⚠️  合约账户访问失败: {response.status_code}")
            if response.status_code == 401:
                print("   可能API密钥没有合约交易权限")
            return False
            
    except Exception as e:
        print(f"❌ 检查合约账户失败: {e}")
        return False

def test_option_with_proxy_info():
    """使用代理信息测试期权API"""
    API_KEY = os.getenv('API_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY')
    
    print(f"\n🎯 期权API测试 (考虑代理)")
    print("=" * 35)
    
    try:
        # 设置请求会话以便处理代理
        session = requests.Session()
        
        # 如果有代理设置，使用它们
        proxies = {}
        if os.environ.get('HTTP_PROXY'):
            proxies['http'] = os.environ.get('HTTP_PROXY')
        if os.environ.get('HTTPS_PROXY'):
            proxies['https'] = os.environ.get('HTTPS_PROXY')
        
        if proxies:
            session.proxies.update(proxies)
            print(f"📡 使用代理: {proxies}")
        
        headers = {'X-MBX-APIKEY': API_KEY}
        
        # 测试期权基本信息端点
        response = session.get(
            'https://vapi.binance.com/vapi/v1/ping',
            headers=headers,
            timeout=15
        )
        
        print(f"期权Ping状态码: {response.status_code}")
        print(f"响应长度: {len(response.content) if response.content else 0} bytes")
        
        if response.status_code == 202 and not response.content.strip():
            print("❌ 仍然是202空响应")
            print("💡 这表明期权服务在当前地区/账户不可用")
            
            # 提供具体建议
            print(f"\n🔍 可能的解决方案:")
            print("1. 检查Binance网页版是否有期权入口")
            print("2. 联系客服确认期权服务地区支持")
            print("3. 考虑使用合约交易作为替代")
        
        return False
        
    except Exception as e:
        print(f"❌ 期权测试失败: {e}")
        return False

if __name__ == "__main__":
    check_proxy_and_network()
    
    balance_sufficient = get_detailed_balance()
    
    futures_available = check_futures_account()
    
    test_option_with_proxy_info()
    
    print(f"\n📋 总结:")
    print("=" * 20)
    print(f"💰 现货资金充足: {'✅' if balance_sufficient else '❌'}")
    print(f"📈 合约账户可用: {'✅' if futures_available else '❌'}")
    print(f"🎯 期权服务: ❌ 不可用")
    
    if balance_sufficient:
        print(f"\n💡 建议:")
        if futures_available:
            print("• 资金充足，可以尝试合约交易作为期权替代")
        else:
            print("• 考虑将资金划转到合约账户进行衍生品交易")
        print("• 或者联系Binance客服确认期权服务可用性") 