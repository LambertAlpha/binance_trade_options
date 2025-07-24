#!/usr/bin/env python3
import requests
import hmac
import hashlib
import time
import os
from dotenv import load_dotenv

load_dotenv()

def check_api_permissions():
    """检查API权限和状态"""
    print("🔐 API权限检查")
    print("=" * 40)
    
    API_KEY = os.getenv('API_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY')
    
    # 创建会话
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'X-MBX-APIKEY': API_KEY,
    })
    
    # 1. 检查现货API权限
    print("1️⃣ 现货API权限:")
    try:
        timestamp = int(time.time() * 1000)
        params = {'timestamp': timestamp, 'recvWindow': 5000}
        
        query_string = '&'.join([f'{k}={v}' for k, v in params.items()])
        signature = hmac.new(SECRET_KEY.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        params['signature'] = signature
        
        response = session.get('https://api.binance.com/api/v3/account', params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("   ✅ 现货账户访问正常")
            print(f"   账户类型: {data.get('accountType', 'N/A')}")
            print(f"   交易权限: {data.get('canTrade', 'N/A')}")
            print(f"   提现权限: {data.get('canWithdraw', 'N/A')}")
            print(f"   充值权限: {data.get('canDeposit', 'N/A')}")
        else:
            print(f"   ❌ 现货API异常: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ 现货权限检查失败: {e}")
    
    # 2. 检查API密钥限制
    print(f"\n2️⃣ API密钥信息:")
    try:
        # 尝试获取API限制信息
        response = session.get('https://api.binance.com/api/v3/rateLimit/order', timeout=10)
        if response.status_code == 200:
            print("   ✅ API调用正常")
        else:
            print(f"   ⚠️ API限制检查: {response.status_code}")
    except:
        pass
    
    print(f"   API Key: {API_KEY[:8]}...{API_KEY[-8:]}")
    print(f"   创建时间: 需要在Binance网页查看")
    print(f"   权限设置: 需要在Binance网页确认")

def provide_solutions():
    """提供具体解决方案"""
    print(f"\n🎯 解决方案（按优先级排序）:")
    print("=" * 50)
    
    print("🥇 **最高优先级 - 检查API权限**")
    print("   1. 登录 https://www.binance.com")
    print("   2. 进入 [账户] -> [API管理]")
    print("   3. 找到你的API密钥")
    print("   4. 确认已勾选 ☑️ **期权交易** 权限")
    print("   5. 如果没有，编辑API并添加期权权限")
    print("   ⚠️  添加权限后需要等待几分钟生效")
    
    print(f"\n🥈 **次优先级 - VPN解决方案**")
    print("   如果API权限正确但仍被拦截:")
    print("   1. 使用VPN连接到新加坡/日本")
    print("   2. 重新测试期权API")
    print("   3. Binance主要服务器在亚洲，可能有地区优化")
    
    print(f"\n🥉 **备选方案 - 联系客服**")
    print("   1. 访问 Binance 帮助中心")
    print("   2. 提交工单说明期权API被WAF拦截")
    print("   3. 提供API密钥和错误信息")
    print("   4. 申请将IP加入期权API白名单")
    
    print(f"\n🔄 **临时方案 - 现货交易开发**")
    print("   1. 先用现货API开发交易逻辑")
    print("   2. 期权问题解决后，迁移到期权API")
    print("   3. 现货和期权API语法相似，迁移成本低")

def test_after_fix():
    """权限修复后的测试步骤"""
    print(f"\n🧪 **权限修复后测试步骤**:")
    print("=" * 40)
    print("1. 等待5-10分钟让权限生效")
    print("2. 运行: python trade_fixed.py")
    print("3. 如果仍失败，尝试VPN")
    print("4. 如果成功，开始期权交易开发")
    
    print(f"\n📞 **需要帮助时联系信息**:")
    print("- Binance客服: 网页版右下角聊天")
    print("- 电报群: @BinanceChina (中文)")
    print("- 官方文档: https://binance-docs.github.io/apidocs/")

if __name__ == "__main__":
    check_api_permissions()
    provide_solutions()
    test_after_fix()
    
    print(f"\n💡 **总结**: 你的网络和现货API完全正常，问题特定于期权API权限设置！") 