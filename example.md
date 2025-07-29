<!-- 示例终端命令 -->
python simple_trade.py \
  --symbol "ETH-250730-3700-P" \
  --side BUY \
  --quantity 0.1 \
  --price 2

python get_orderbook.py \
  --symbol BTC-250730-119500-P \
  --limit 10

python get_blocktrades.py \
--symbol BTC-250728-119500-P \
--limit 10

python market_trade.py --symbol ETH-250730-3700-P \
--quantity 1 \
--premium 2

<!-- 参数合集 -->
symbol	STRING	YES	Option trading pair, e.g BTC-200730-9000-C
side	ENUM	YES	Buy/sell direction: SELL, BUY
type	ENUM	YES	Order Type: LIMIT(only support limit)
quantity	DECIMAL	YES	Order Quantity
price	DECIMAL	NO	Order Price
timeInForce	ENUM	NO	Time in force method（Default GTC）
reduceOnly	BOOLEAN	NO	Reduce Only（Default false）
postOnly	BOOLEAN	NO	Post Only（Default false）
newOrderRespType	ENUM	NO	"ACK", "RESULT", Default "ACK"
clientOrderId	STRING	NO	User-defined order ID cannot be repeated in pending orders
isMmp	BOOLEAN	NO	is market maker protection order, true/false
recvWindow	LONG	NO	
timestamp	LONG	YES