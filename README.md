# Binance 期权交易工具

这是一个用于在 Binance 交易所进行期权交易的 Python 工具。

## 环境要求

- Python 3.8+
- pip

## 安装步骤

### 1. 快速启动（包括环境配置）
```bash
# 使用 venv (推荐)
python3 -m venv venv

# 激活虚拟环境
# macOS/Linux:
source venv/bin/activate
# Windows:
# venv\Scripts\activate
```

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量
复制 `env.example` 文件并重命名为 `.env`：
```bash
cp env.example .env
```

编辑 `.env` 文件，填入您的配置：
```env
# Binance API 配置
API_KEY=your_api_key_here
PRIVATE_KEY_PATH=test-prv-key.pem

# 期权交易配置
SYMBOL=BTC-200730-9000-C
SIDE=BUY
TYPE=LIMIT
TIME_IN_FORCE=GTC
QUANTITY=1
PRICE=100

# 高级期权交易参数
REDUCE_ONLY=false
POST_ONLY=false
NEW_ORDER_RESP_TYPE=ACK
CLIENT_ORDER_ID=
IS_MMP=false
RECV_WINDOW=5000
```

## 使用方法

### 查询期权合约信息
```bash
python option_info.py
```

### 运行期权交易脚本
```bash
python trade.py
```

### 配置说明

#### 基础参数
- `API_KEY`: 您的 Binance API Key
- `PRIVATE_KEY_PATH`: 私钥文件路径
- `SYMBOL`: 期权交易对符号 (例如: BTC-200730-9000-C)
- `SIDE`: 交易方向 (BUY/SELL)
- `TYPE`: 订单类型 (期权只支持 LIMIT)
- `TIME_IN_FORCE`: 订单有效期 (GTC/IOC/FOK)
- `QUANTITY`: 交易数量
- `PRICE`: 交易价格

#### 高级参数
- `REDUCE_ONLY`: 是否仅减仓 (true/false)
- `POST_ONLY`: 是否仅挂单 (true/false)
- `NEW_ORDER_RESP_TYPE`: 响应类型 (ACK/RESULT)
- `CLIENT_ORDER_ID`: 用户自定义订单ID
- `IS_MMP`: 是否做市商保护订单 (true/false)
- `RECV_WINDOW`: 接收窗口 (毫秒)

### 期权交易对格式说明

期权交易对格式：`{标的资产}-{到期日}-{行权价}-{期权类型}`

示例：
- `BTC-200730-9000-C`: BTC看涨期权，2020年7月30日到期，行权价9000
- `BTC-200730-9000-P`: BTC看跌期权，2020年7月30日到期，行权价9000
- `ETH-200731-200-C`: ETH看涨期权，2020年7月31日到期，行权价200

## 安全注意事项

⚠️ **重要安全提醒**：

1. **永远不要**将您的 API Key 和私钥提交到版本控制系统
2. 确保 `.env` 文件已添加到 `.gitignore`
3. 定期轮换您的 API Key
4. 在生产环境中使用强密码保护私钥文件
5. 期权交易具有高风险，请谨慎操作

## 项目结构

```
binance_trade_options/
├── trade.py              # 主期权交易脚本
├── option_info.py        # 期权信息查询工具
├── requirements.txt      # Python 依赖
├── README.md            # 项目说明
├── env.example          # 环境变量模板
├── .gitignore           # Git 忽略文件
├── run.sh               # 快速启动脚本
└── venv/                # 虚拟环境 (不提交到版本控制)
```

## 依赖包说明

- `requests`: HTTP 请求库
- `cryptography`: 加密和签名功能
- `python-dotenv`: 环境变量管理

## 故障排除

### 常见问题

1. **权限错误**: 确保私钥文件有正确的读取权限
2. **API 错误**: 检查 API Key 是否正确配置
3. **网络错误**: 确保网络连接正常
4. **期权合约错误**: 确保期权交易对符号格式正确
5. **参数错误**: 检查交易参数是否在合理范围内

### 获取帮助

如果遇到问题，请检查：
- API Key 是否有效且具有期权交易权限
- 私钥文件是否存在且格式正确
- 网络连接是否正常
- 期权交易对符号是否正确
- 交易参数是否合理