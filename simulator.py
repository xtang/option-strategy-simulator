import numpy as np
import matplotlib.pyplot as plt

def calculate_pl(stock_price, shares,
                   num_put_contracts, strike_put, put_premium_per_share,
                   num_call_contracts, strike_call, call_premium_per_share,
                   future_prices):
    """Calculates P/L for different strategies based on contract counts and per-share premiums."""
    stock_only_list = []
    protective_put_list = []
    covered_call_list = []
    collar_list = []

    shares_per_contract = 100

    # Calculate total premiums based on per-share values and contract count
    total_put_premium_paid = put_premium_per_share * shares_per_contract * num_put_contracts
    total_call_premium_received = call_premium_per_share * shares_per_contract * num_call_contracts

    for price in future_prices:
        # 1. Stock only P/L
        stock_pl = (price - stock_price) * shares

        # 2. Option P/L Components
        # Put P/L = (Value Change from Strike * Shares Controlled) - Total Premium Paid
        put_value_per_share = max(strike_put - price, 0)
        put_value_change = put_value_per_share * shares_per_contract * num_put_contracts
        put_total_pl = put_value_change - total_put_premium_paid

        # Call P/L = Total Premium Received - (Obligation Change from Strike * Shares Controlled)
        call_obligation_per_share = max(price - strike_call, 0) # Obligation is positive loss if exercised
        call_obligation_change = call_obligation_per_share * shares_per_contract * num_call_contracts
        call_total_pl = total_call_premium_received - call_obligation_change

        # 3. Strategy Totals
        total_protective = stock_pl + put_total_pl
        total_covered = stock_pl + call_total_pl
        collar_total = stock_pl + put_total_pl + call_total_pl

        # Append results
        stock_only_list.append(stock_pl)
        protective_put_list.append(total_protective)
        covered_call_list.append(total_covered)
        collar_list.append(collar_total)

    return stock_only_list, protective_put_list, covered_call_list, collar_list

def plot_pl(future_prices, strategy_results, selected_strategies, stock_price):
    """Generates a P/L plot for selected strategies and returns the Matplotlib figure object."""
    fig, ax = plt.subplots(figsize=(10, 6))

    # Define plot styles (optional, for visual distinction)
    styles = {
        'Stock Only': {'linestyle': '--', 'color': 'black'},
        'Protective Put': {'linestyle': '-', 'color': 'blue'},
        'Covered Call': {'linestyle': '-', 'color': 'red'},
        'Collar': {'linestyle': '-', 'color': 'green'}
    }

    # Plot only selected strategies
    for strategy_name in selected_strategies:
        if strategy_name in strategy_results:
            style = styles.get(strategy_name, {}) # Get style or empty dict
            ax.plot(future_prices,
                    strategy_results[strategy_name],
                    label=strategy_name,
                    linestyle=style.get('linestyle', '-'), # Default linestyle
                    color=style.get('color') # Use specified color or default cycle
                   )

    # Add vertical line for current stock price
    ax.axvline(stock_price, color='grey', linestyle=':', linewidth=1, label=f'Current Price (${stock_price:.2f})')

    ax.set_xlabel('Stock Price at Expiry ($)')
    ax.set_ylabel('Total P/L ($)')
    ax.set_title('P/L of Selected Hedging Strategies')
    ax.legend()
    ax.grid(True)
    ax.axhline(0, color='black', linewidth=0.5)
    fig.tight_layout()

    return fig

def get_future_prices(current_price, range_pct=0.20):
    """Generates a range of future prices around the current price."""
    min_price = current_price * (1 - range_pct)
    max_price = current_price * (1 + range_pct)
    # Ensure a reasonable number of steps, e.g., 50-100
    num_steps = max(50, int((max_price - min_price) * 2)) # Adjust step size based on range
    return np.linspace(min_price, max_price, num=num_steps)

# --- Metric Calculation Functions ---

def calculate_metrics(strategy_name, stock_price, shares,
                      num_put_contracts, strike_put, put_premium_per_share,
                      num_call_contracts, strike_call, call_premium_per_share):
    """Calculates max profit/loss/breakevens using per-share premiums."""

    shares_per_contract = 100
    # Calculate total premiums from per-share values
    total_put_premium = put_premium_per_share * shares_per_contract * num_put_contracts
    total_call_premium = call_premium_per_share * shares_per_contract * num_call_contracts

    max_profit = np.inf
    max_loss = -np.inf
    breakevens = []

    # --- Calculations based on strategy ---
    if strategy_name == 'Stock Only':
        max_profit = np.inf
        max_loss = -stock_price * shares # Theoretical max loss if stock goes to 0
        breakevens = [stock_price]

    elif strategy_name == 'Protective Put':
        if num_put_contracts == 0: # Treat as stock only if no puts
             return calculate_metrics('Stock Only', stock_price, shares, 0,0,0,0,0,0)
        cost_basis_per_share = stock_price + (total_put_premium / (num_put_contracts * shares_per_contract))
        # Note: Assumes 1 contract per 100 shares for simplicity in breakeven calc
        # A more precise calculation would require considering if shares != num_put_contracts * 100
        max_profit = np.inf
        max_loss = (strike_put - stock_price) * shares - total_put_premium
        # Breakeven = Initial Stock Price + Total Put Premium / Shares_covered_by_puts
        # Simplified assumption: breakeven happens when stock gain offsets put premium cost
        breakevens = [stock_price + total_put_premium / shares]

    elif strategy_name == 'Covered Call':
        if num_call_contracts == 0: # Treat as stock only if no calls
            return calculate_metrics('Stock Only', stock_price, shares, 0,0,0,0,0,0)
        # Max profit occurs if price finishes at or above call strike
        max_profit = (strike_call - stock_price) * shares + total_call_premium
        max_loss = -stock_price * shares + total_call_premium # If stock goes to 0
        # Breakeven = Initial Stock Price - Total Call Premium / Shares
        breakevens = [stock_price - total_call_premium / shares]

    elif strategy_name == 'Collar':
        if num_put_contracts == 0 or num_call_contracts == 0:
             # Handle cases where it's just a put or call, or stock only
             if num_put_contracts > 0: strategy_name = 'Protective Put'
             elif num_call_contracts > 0: strategy_name = 'Covered Call'
             else: strategy_name = 'Stock Only'
             return calculate_metrics(strategy_name, stock_price, shares, num_put_contracts, strike_put, put_premium_per_share, num_call_contracts, strike_call, call_premium_per_share)

        net_premium = total_call_premium - total_put_premium
        # Max profit if price finishes at or above call strike
        max_profit = (strike_call - stock_price) * shares + net_premium
        # Max loss if price finishes at or below put strike
        max_loss = (strike_put - stock_price) * shares + net_premium
        # Breakeven = Stock Price + (Total Put Premium - Total Call Premium) / Shares
        # This formula correctly uses the total premiums calculated above
        breakevens = [stock_price + (total_put_premium - total_call_premium) / shares]

    return {
        "max_profit": max_profit,
        "max_loss": max_loss,
        "breakevens": breakevens
    }

# ... existing code ...