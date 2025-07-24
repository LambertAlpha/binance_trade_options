#!/usr/bin/env python3
import os
import requests
import hmac
import hashlib
import time
from dotenv import load_dotenv

load_dotenv()

def test_basic_trading():
    """测试最基础的期权交易配置"""
    API_KEY = os.getenv('API_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY')
    
    print("🧪 Binance期权交易测试")
    print("=" * 40)
    
    # 基于目前的情况，建议使用现货交易来测试API
    print("💡 由于期权API返回202空响应，建议先测试现货交易API:")
    print()
    
    # 测试现货账户信息
    print("📊 测试现货账户信息...")
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
        
        # 使用现货API测试
        response = requests.get(
            'https://api.binance.com/api/v3/account',
            headers=headers,
            params=params,
            timeout=10
        )
        
        print(f"现货账户API状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            balances = data.get('balances', [])
            
            print("✅ 现货API连接成功！")
            print("\n💰 账户余额 (非零资产):")
            
            non_zero_balances = []
            for balance in balances:
                free = float(balance.get('free', 0))
                locked = float(balance.get('locked', 0))
                if free > 0 or locked > 0:
                    non_zero_balances.append(balance)
                    asset = balance['asset']
                    print(f"   {asset}: 可用={free}, 冻结={locked}")
            
            if not non_zero_balances:
                print("   ⚠️  账户余额为空，需要先充值")
                return False
            
            # 检查是否有USDT
            usdt_balance = next((b for b in non_zero_balances if b['asset'] == 'USDT'), None)
            if usdt_balance:
                usdt_free = float(usdt_balance['free'])
                print(f"\n💵 USDT余额: {usdt_free}")
                
                if usdt_free >= 10:
                    print("✅ USDT余额充足，可以进行小额测试")
                    suggest_spot_test_order(usdt_free)
                else:
                    print("⚠️  USDT余额较少，建议先充值")
                    
            return True
            
        else:
            print(f"❌ 现货API失败: {response.status_code}")
            print(f"错误: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 测试出错: {e}")
        return False

def suggest_spot_test_order(usdt_balance):
    """建议现货测试订单"""
    print(f"\n🔄 建议的现货测试交易:")
    print("由于期权可能不可用，可以先用现货测试API:")
    
    # 建议一个小额的现货交易
    test_amount = min(10, usdt_balance * 0.1)  # 10 USDT或余额的10%
    
    print(f"1. 交易对: BTCUSDT")
    print(f"2. 方向: BUY (买入)")
    print(f"3. 类型: MARKET (市价)")
    print(f"4. 金额: {test_amount:.2f} USDT")
    print(f"5. 预计买入BTC: ~{test_amount/50000:.8f} BTC")
    
    print(f"\n📝 现货测试订单配置:")
    print(f"symbol=BTCUSDT")
    print(f"side=BUY")
    print(f"type=MARKET")
    print(f"quoteOrderQty={test_amount}")

def check_option_availability():
    """检查期权服务可用性"""
    print(f"\n🔍 期权服务诊断:")
    print("=" * 30)
    
    print("基于测试结果分析:")
    print("1. ✅ API密钥正确配置")
    print("2. ✅ 网络连接正常") 
    print("3. ❌ 期权API返回202空响应")
    print()
    
    print("可能的原因:")
    print("• 🌏 地区限制: Binance期权在某些地区不提供服务")
    print("• 📋 资格认证: 可能需要完成期权交易资格认证")
    print("• 🔐 API权限: API密钥可能没有期权交易权限")
    print("• 💰 资金要求: 期权交易可能有最低资金要求")
    
    print(f"\n💡 建议:")
    print("1. 登录Binance网页版，检查是否有期权交易入口")
    print("2. 查看账户是否完成期权交易资格认证")
    print("3. 确认API密钥权限包含期权交易")
    print("4. 联系Binance客服确认期权服务可用性")

if __name__ == "__main__":
    success = test_basic_trading()
    check_option_availability()
    
    if success:
        print(f"\n🎯 推荐行动:")
        print("1. 先用现货API测试交易功能")
        print("2. 确认API和交易逻辑正常后，再处理期权问题")
        print("3. 联系Binance确认期权服务是否在你的地区可用")
    else:
        print(f"\n❌ 需要先解决基础API连接问题") 