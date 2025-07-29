# /eapi/v1/blockTrades
# Recent Block Trades List (近期大宗交易列表)
# 这是一个特殊的列表，显示的是私下协商达成的大额交易，通常被称为“大宗交易”或场外交易 (OTC)。
# python get_blocktrades.py \
# --symbol BTC-250728-119500-P \
# --limit 100

import requests
import argparse
import json

# 币安期权API配置
base_url = "https://eapi.binance.com"
endpoint_path = '/eapi/v1/blockTrades'

# 命令行参数解析
parser = argparse.ArgumentParser(description='获取币安期权订单簿深度数据')
parser.add_argument('--symbol', required=True, help='期权交易对，例如: ETH-250728-3700-C')
parser.add_argument('--limit', type=int, default=100, choices=[100, 500], 
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
        print(data)

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