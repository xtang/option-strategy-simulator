import numpy as np
import matplotlib.pyplot as plt

# 当前股价
stock_price = 137.0

# 股票持仓
shares = 100

# Protective Put 参数
strike_put = 130.0       # Put 行权价
put_premium = 2.0        # Put 权利金（每股）

# Covered Call 参数
strike_call = 145.0      # Call 行权价
call_premium = 1.5       # Call 权利金（每股）

# 模拟未来股价范围
future_prices = np.arange(110, 161, 1)  # 从 $110 到 $160，步长为 $1

# 初始化盈亏列表
stock_only = []
protective_put = []
covered_call = []
collar = []

for price in future_prices:
    # 股票本身盈亏
    stock_pl = (price - stock_price) * shares

    # Protective Put 盈亏
    put_pl = max(strike_put - price, 0) * shares - put_premium * shares
    total_protective = stock_pl + put_pl

    # Covered Call 盈亏
    if price > strike_call:
        call_pl = call_premium * shares - (price - strike_call) * shares
    else:
        call_pl = call_premium * shares
    total_covered = stock_pl + call_pl

    # Collar 策略盈亏
    collar_total = stock_pl + put_pl + call_pl

    # 记录每种策略的总盈亏
    stock_only.append(stock_pl)
    protective_put.append(total_protective)
    covered_call.append(total_covered)
    collar.append(collar_total)

# 绘制盈亏图表
plt.figure(figsize=(10, 6))
plt.plot(future_prices, stock_only, label='Stock Only', linestyle='--')
plt.plot(future_prices, protective_put, label='Protective Put')
plt.plot(future_prices, covered_call, label='Covered Call')
plt.plot(future_prices, collar, label='Collar')
plt.xlabel('GOOGL Price at Expiry ($)')
plt.ylabel('Total P/L ($)')
plt.title('P/L of GOOGL Hedging Strategies')
plt.legend()
plt.grid(True)
plt.axhline(0, color='black', linewidth=0.5)
plt.tight_layout()
plt.show()
