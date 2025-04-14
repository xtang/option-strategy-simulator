import streamlit as st
import simulator # Import our simulation logic

st.set_page_config(
    page_title="Option Strategy Simulator", # Set the browser tab title
    layout="wide"
)

st.title("Options Strategy Simulator")

st.sidebar.header("Input Parameters")

# --- Input Fields --- Use sidebar for inputs
stock_price = st.sidebar.number_input(
    "Current Stock Price ($)",
    min_value=0.01, value=137.0, step=0.01, format="%.2f"
)
shares = st.sidebar.number_input(
    "Number of Shares",
    min_value=1, value=100, step=1
)

st.sidebar.subheader("Protective Put")
num_put_contracts = st.sidebar.number_input(
    "Number of Put Contracts",
    min_value=0, value=1, step=1
)
strike_put = st.sidebar.number_input(
    "Put Strike Price ($)",
    min_value=0.01, value=130.0, step=0.01, format="%.2f"
)
put_premium = st.sidebar.number_input(
    "Put Premium Paid ($/share)",
    min_value=0.00, value=2.0, step=0.01, format="%.2f"
)

st.sidebar.subheader("Covered Call")
num_call_contracts = st.sidebar.number_input(
    "Number of Call Contracts",
    min_value=0, value=1, step=1
)
strike_call = st.sidebar.number_input(
    "Call Strike Price ($)",
    min_value=0.01, value=145.0, step=0.01, format="%.2f"
)
call_premium = st.sidebar.number_input(
    "Call Premium Received ($/share)",
    min_value=0.00, value=1.5, step=0.01, format="%.2f"
)

st.sidebar.subheader("Plot & Simulation Settings")
price_range_pct = st.sidebar.slider(
    "Future Price Range (+/-%)",
    min_value=5, max_value=50, value=20, step=1, format="%d%%"
)

# Strategy Selection for Plot
all_strategies = ['Stock Only', 'Protective Put', 'Covered Call', 'Collar']
selected_strategies = st.sidebar.multiselect(
    'Select Strategies to Plot',
    all_strategies,
    default=all_strategies  # Default to showing all
)

# --- Calculation and Plotting --- (Main area)
st.header("Simulation Results")

# Add a button to trigger the simulation explicitly if desired
# if st.sidebar.button("Run Simulation"):

# Generate future prices based on input stock price and range
future_prices = simulator.get_future_prices(stock_price, range_pct=price_range_pct/100.0)

# Calculate P/L for all strategies
stock_only, protective_put, covered_call, collar = simulator.calculate_pl(
    stock_price, shares,
    num_put_contracts, strike_put, put_premium,
    num_call_contracts, strike_call, call_premium,
    future_prices
)

# Store results in a dictionary for easier access
strategy_results = {
    'Stock Only': stock_only,
    'Protective Put': protective_put,
    'Covered Call': covered_call,
    'Collar': collar
}

# --- Plotting ---
st.subheader("P/L Plot")

# Check if any strategies are selected
if not selected_strategies:
    st.warning("Please select at least one strategy to plot.")
else:
    # Pass selected strategies and the results dictionary (CORRECTED CALL)
    fig = simulator.plot_pl(
        future_prices, strategy_results, selected_strategies, stock_price
    )
    st.pyplot(fig)

# --- Key Metrics & Summary ---
st.subheader("Inputs & Key Metrics")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Inputs Used:**")
    st.markdown(f"""
    - **Stock:** Current Price: `${stock_price:.2f}`, Shares: `{shares}`
    - **Protective Put:** Contracts: `{num_put_contracts}`, Strike: `${strike_put:.2f}`, Premium Paid/Share: `${put_premium:.2f}`
    - **Covered Call:** Contracts: `{num_call_contracts}`, Strike: `${strike_call:.2f}`, Premium Received/Share: `${call_premium:.2f}`
    - **Price Range Simulated:** +/- {price_range_pct}%
    """)

with col2:
    st.markdown("**Key Metrics:**")
    if not selected_strategies:
        st.info("Select strategies from the sidebar to view metrics.")
    else:
        for strategy in selected_strategies:
            metrics = simulator.calculate_metrics(
                strategy, stock_price, shares,
                num_put_contracts, strike_put, put_premium,
                num_call_contracts, strike_call, call_premium
            )
            st.markdown(f"**{strategy}:**")
            profit_str = f"${metrics['max_profit']:.2f}" if metrics['max_profit'] != float('inf') else "Unlimited"
            loss_str = f"${abs(metrics['max_loss']):.2f}" if metrics['max_loss'] != float('-inf') else "Unlimited"
            be_str = ", ".join([f"${be:.2f}" for be in metrics['breakevens']])
            st.markdown(f"  - Max Profit: {profit_str}")
            st.markdown(f"  - Max Loss: {loss_str}")
            st.markdown(f"  - Breakeven(s): {be_str}")