# 获取币安期权订单簿深度数据
# 接口: /eapi/v1/depth (公开接口，无需签名)
import requests
import argparse
import json

# 币安期权API配置
base_url = "https://eapi.binance.com"
endpoint_path = '/eapi/v1/depth'

# 命令行参数解析
parser = argparse.ArgumentParser(description='获取币安期权订单簿深度数据')
parser.add_argument('--symbol', required=True, help='期权交易对，例如: ETH-250729-3600-C')
parser.add_argument('--limit', type=int, default=100, choices=[10, 20, 50, 100, 500, 1000], 
                    help='返回条目数量 (默认: 100)')

args = parser.parse_args()

# 构建请求参数
params = {
    "symbol": args.symbol,
    "limit": args.limit
}

try:
    # 发送请求
    response = requests.get(base_url + endpoint_path, params=params, timeout=10)
    
    print(f"请求URL: {response.url}")
    print(f"响应状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("\n✅ 获取订单簿成功:")
        print(f"交易对: {args.symbol}")
        print(f"更新时间: {data.get('T', 'N/A')}")
        print(f"更新ID: {data.get('u', 'N/A')}")
        
        # 格式化输出买单
        bids = data.get('bids', [])
        print(f"\n📈 买单 (Bids) - 共 {len(bids)} 条:")
        for i, bid in enumerate(bids[:10]):  # 只显示前10条
            print(f"  {i+1:2d}. 价格: {bid[0]:>10} | 数量: {bid[1]:>10}")
        
        # 格式化输出卖单  
        asks = data.get('asks', [])
        print(f"\n📉 卖单 (Asks) - 共 {len(asks)} 条:")
        for i, ask in enumerate(asks[:10]):  # 只显示前10条
            print(f"  {i+1:2d}. 价格: {ask[0]:>10} | 数量: {ask[1]:>10}")
            
        # 计算买卖价差
        if bids and asks:
            best_bid = float(bids[0][0])
            best_ask = float(asks[0][0])
            spread = best_ask - best_bid
            spread_pct = (spread / best_ask) * 100 if best_ask > 0 else 0
            print(f"\n💰 价差信息:")
            print(f"  最高买价: {best_bid}")
            print(f"  最低卖价: {best_ask}")
            print(f"  价差: {spread:.6f} ({spread_pct:.3f}%)")
    else:
        print(f"❌ 请求失败: {response.status_code}")
        try:
            error_data = response.json()
            print(f"错误信息: {error_data}")
        except:
            print(f"错误信息: {response.text}")

except requests.exceptions.Timeout:
    print("❌ 请求超时，请检查网络连接")
except requests.exceptions.RequestException as e:
    print(f"❌ 网络请求错误: {e}")
except json.JSONDecodeError:
    print("❌ 响应数据解析失败")
except Exception as e:
    print(f"❌ 发生未知错误: {e}")    