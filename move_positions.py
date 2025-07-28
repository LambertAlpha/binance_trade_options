import hmac
import hashlib
import time
import requests
import json
from urllib.parse import urlencode

# --- 1. 配置您的API密钥 (请务必使用母账户的密钥) ---
API_KEY = '你的母账户API_KEY'
SECRET_KEY = '你的母账户SECRET_KEY'
BASE_URL = 'https://api.binance.com'

# --- 2. 设置请求参数 ---
params = {
    'fromUserEmail': 'masteraccount@example.com',  # 源账户邮箱（母账户或子账户）
    'toUserEmail': 'subaccount@example.com',       # 目标账户邮箱（母账户或子账户）
    'productType': 'UM',                           # 仅支持 "UM" (U本位合约)
    'timestamp': int(time.time() * 1000)
}

# --- 3. 设置orderArgs参数 (支持多个仓位转移，最多10个) ---
# 注意：这里使用特殊的URL编码格式，不是JSON
# positionSide 支持: BOTH, LONG, SHORT
# quantity 必须为正数
order_args = [
    {
        'symbol': 'BTCUSDT',
        'quantity': '0.001',      # 转移数量，必须为正数字符串 ⚠️注意：这是BTC数量，不是USDT价值！
        'positionSide': 'BOTH'    # 仓位方向: BOTH(单向持仓), LONG(多头), SHORT(空头)
    }
    # 可以添加更多仓位，最多10个
    # {
    #     'symbol': 'ETHUSDT', 
    #     'quantity': '0.01',
    #     'positionSide': 'BOTH'
    # }
]

# 将orderArgs转换为URL参数格式
for i, order in enumerate(order_args):
    params[f'orderArgs[{i}].symbol'] = order['symbol']
    params[f'orderArgs[{i}].quantity'] = order['quantity']
    params[f'orderArgs[{i}].positionSide'] = order['positionSide']

# 可选：设置接收窗口时间（毫秒）
# params['recvWindow'] = 5000

# --- 4. 生成签名 ---
query_string = urlencode(params, doseq=True)  # doseq=True 处理列表参数
signature = hmac.new(SECRET_KEY.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
params['signature'] = signature

# --- 5. 发送POST请求 ---
headers = {
    'X-MBX-APIKEY': API_KEY
}

endpoint_path = "/sapi/v1/sub-account/futures/move-position"
url = f"{BASE_URL}{endpoint_path}"

print(f"正在向以下URL发送POST请求: {url}")
print(f"请求参数: {query_string}")

try:
    response = requests.post(url, headers=headers, params=params)
    response.raise_for_status()
    
    # --- 6. 解读返回结果 ---
    result = response.json()
    print("\nAPI Response:")
    print(json.dumps(result, indent=2))

    # 检查移仓结果
    if 'movePositionOrders' in result:
        print("\n移仓操作完成！详细结果:")
        for order in result['movePositionOrders']:
            if order.get('success'):
                print(f"✅ {order['symbol']}: {order['quantity']} 从 {order['fromUserEmail']} 转移到 {order['toUserEmail']} 成功")
                print(f"   价格类型: {order['priceType']}, 价格: {order['price']}, 方向: {order['side']}")
            else:
                print(f"❌ {order['symbol']}: 转移失败")
    else:
        print(f"\n移仓失败。可能的错误信息: {result}")

except requests.exceptions.RequestException as e:
    print(f"请求发生错误: {e}")
    if hasattr(e, 'response') and e.response:
        try:
            error_detail = e.response.json()
            print(f"错误详情: {json.dumps(error_detail, indent=2)}")
        except:
            print(f"错误详情: {e.response.text}")