#!/usr/bin/env python3
import requests
import os
from dotenv import load_dotenv
import json
from datetime import datetime

# 加载环境变量
load_dotenv()

# 从环境变量获取配置
API_KEY = os.getenv('API_KEY')

def get_option_info():
    """获取期权交易对信息"""
    try:
        headers = {
            'X-MBX-APIKEY': API_KEY,
        } if API_KEY else {}
        
        # 获取期权交易对信息
        response = requests.get(
            'https://vapi.binance.com/vapi/v1/exchangeInfo',
            headers=headers
        )
        
        if response.status_code in [200, 202]:
            data = response.json()
            
            print("🔍 当前可用的期权合约:")
            print("=" * 80)
            
            option_symbols = data.get('data', {}).get('optionSymbols', [])
            
            if not option_symbols:
                print("❌ 没有找到可用的期权合约")
                return None
                
            # 按到期时间排序
            option_symbols.sort(key=lambda x: x.get('expiryDate', 0))
            
            suitable_options = []
            
            for idx, option in enumerate(option_symbols[:10]):  # 显示前10个
                symbol = option.get('symbol', 'N/A')
                strike_price = option.get('strikePrice', 'N/A')
                side = option.get('side', 'N/A')
                min_qty = option.get('minQty', 'N/A')
                expiry_date = option.get('expiryDate', 0)
                underlying = option.get('underlying', 'N/A')
                
                # 转换到期时间
                if expiry_date:
                    expiry_str = datetime.fromtimestamp(expiry_date/1000).strftime('%Y-%m-%d %H:%M')
                else:
                    expiry_str = 'N/A'
                
                print(f"\n📋 {idx+1}. {symbol}")
                print(f"   标的资产: {underlying}")
                print(f"   行权价: {strike_price}")
                print(f"   类型: {'看涨期权' if side == 'CALL' else '看跌期权'}")
                print(f"   最小数量: {min_qty}")
                print(f"   到期时间: {expiry_str}")
                
                # 收集适合测试的期权（最小数量较小的）
                try:
                    if float(min_qty) <= 0.01:
                        suitable_options.append({
                            'symbol': symbol,
                            'minQty': min_qty,
                            'side': side,
                            'strikePrice': strike_price,
                            'underlying': underlying
                        })
                except:
                    pass
            
            return suitable_options
            
        else:
            print(f"❌ 获取期权信息失败，状态码: {response.status_code}")
            print(f"错误信息: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        return None

def get_option_prices(symbols):
    """获取期权当前价格"""
    try:
        headers = {
            'X-MBX-APIKEY': API_KEY,
        } if API_KEY else {}
        
        print("\n💰 获取期权当前价格:")
        print("=" * 50)
        
        for symbol_info in symbols[:5]:  # 只查前5个
            symbol = symbol_info['symbol']
            
            response = requests.get(
                f'https://vapi.binance.com/vapi/v1/ticker?symbol={symbol}',
                headers=headers
            )
            
            if response.status_code in [200, 202]:
                data = response.json()
                ticker_data = data.get('data', [])
                
                if ticker_data:
                    ticker = ticker_data[0]
                    last_price = ticker.get('lastPrice', '0')
                    
                    print(f"\n📊 {symbol}")
                    print(f"   当前价格: {last_price} USDT")
                    print(f"   最小数量: {symbol_info['minQty']}")
                    print(f"   类型: {'看涨' if symbol_info['side'] == 'CALL' else '看跌'}")
                    
                    # 计算最小订单金额
                    try:
                        min_amount = float(last_price) * float(symbol_info['minQty'])
                        print(f"   最小订单金额: {min_amount:.4f} USDT")
                        
                        # 推荐适合测试的订单
                        if min_amount < 50:  # 小于50 USDT的适合测试
                            print(f"   ✅ 适合测试 (金额较小)")
                            
                            # 生成测试订单建议
                            test_price = max(0.01, float(last_price) * 0.8)  # 比当前价格低20%
                            print(f"   💡 建议测试价格: {test_price:.4f} USDT")
                            print(f"   💡 建议测试数量: {symbol_info['minQty']}")
                            
                    except:
                        print(f"   ⚠️  无法计算最小金额")
                        
            else:
                print(f"   ❌ 获取 {symbol} 价格失败")
                
    except Exception as e:
        print(f"❌ 获取价格时发生错误: {e}")

def generate_test_order_suggestion(suitable_options):
    """生成测试订单建议"""
    if not suitable_options:
        print("\n❌ 没有找到适合的期权合约进行测试")
        return
        
    print("\n🎯 推荐测试订单:")
    print("=" * 50)
    
    # 选择第一个适合的期权
    recommended = suitable_options[0]
    
    print(f"交易对: {recommended['symbol']}")
    print(f"最小数量: {recommended['minQty']}")
    print(f"类型: {'看涨期权' if recommended['side'] == 'CALL' else '看跌期权'}")
    
    # 生成.env配置建议
    print(f"\n📝 更新你的 .env 文件:")
    print(f"SYMBOL={recommended['symbol']}")
    print(f"QUANTITY={recommended['minQty']}")
    print(f"PRICE=0.01")  # 很低的价格用于测试
    print(f"SIDE=BUY")
    print(f"TYPE=LIMIT")

if __name__ == "__main__":
    print("🔍 正在查询Binance期权交易信息...")
    
    # 获取期权信息
    suitable_options = get_option_info()
    
    if suitable_options:
        # 获取价格信息
        get_option_prices(suitable_options)
        
        # 生成测试订单建议
        generate_test_order_suggestion(suitable_options)
    else:
        print("\n❌ 无法获取期权信息，请检查:")
        print("1. 网络连接是否正常")
        print("2. API密钥是否正确配置")
        print("3. Binance是否在你的地区提供期权服务") 