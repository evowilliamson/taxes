import pandas as pd
from datetime import datetime, timedelta

# Initial inventory
initial_inventory = {
    "EUR": 0,
    "USD": 0,
    "BTC": 0,
    "ETH": 0,
    "LTC": 0,
    "PAXG": 0,
}

# Currencies of interest
currencies_of_interest = ["EUR", "USD", "BTC", "ETH", "LTC", "PAXG"]

# Function to calculate inventory over time
def calculate_inventory(input_file, output_file):
    # Read the input file
    trades = pd.read_csv(input_file, sep="\t")

    # Convert date_time to datetime and sort by it
    trades['date_time'] = pd.to_datetime(trades['date_time'])
    trades.sort_values('date_time', inplace=True)

    # Create a DataFrame for inventory tracking
    start_date = trades['date_time'].min().date()
    end_date = trades['date_time'].max().date()
    date_range = pd.date_range(start=start_date, end=end_date)

    inventory = pd.DataFrame(index=date_range, columns=currencies_of_interest, dtype=float)

    # Initialize inventory with the initial values
    for currency, amount in initial_inventory.items():
        inventory.loc[inventory.index[0], currency] = amount

    # Process trades
    for _, trade in trades.iterrows():
        trade_date = pd.Timestamp(trade['date_time'].date())  # Ensure consistent type with inventory index
        source_currency = trade['source_currency']
        source_amount = trade['source_amount']
        target_currency = trade['target_currency']
        target_amount = trade['target_amount']

        # Update inventory for the specific trade date
        if source_currency in inventory.columns:
            inventory.loc[trade_date, source_currency] -= source_amount

        if target_currency in inventory.columns:
            inventory.loc[trade_date, target_currency] += target_amount

        # Propagate the inventory forward to the next days
        if trade_date != inventory.index[-1]:  # Ensure not to propagate past the last day
            for col in inventory.columns:
                inventory.loc[trade_date + timedelta(days=1):, col] = inventory.loc[trade_date, col]

    # Add columns for the highest and lowest inventory levels and their dates
    peak_data = {
        "Currency": [],
        "Highest Inventory": [],
        "Highest Date": [],
        "Lowest Inventory": [],
        "Lowest Date": []
    }

    for currency in currencies_of_interest:
        peak_data["Currency"].append(currency)
        peak_data["Highest Inventory"].append(inventory[currency].max())
        peak_data["Highest Date"].append(inventory[currency].idxmax().strftime('%Y-%m-%d'))
        peak_data["Lowest Inventory"].append(inventory[currency].min())
        peak_data["Lowest Date"].append(inventory[currency].idxmin().strftime('%Y-%m-%d'))

    # Save inventory to file
    inventory.reset_index(inplace=True)
    inventory.rename(columns={"index": "date"}, inplace=True)
    inventory.to_csv(output_file, sep="\t", index=False)

    # Print peak information
    peak_df = pd.DataFrame(peak_data)

    # Format to avoid scientific notation
    pd.set_option('display.float_format', '{:.6f}'.format)

    print("Peak Inventory Data:")
    print(peak_df)

# Example usage
input_file = "trades_input.tsv"  # Replace with your input file
output_file = "inventory_output.tsv"  # Replace with your desired output file
calculate_inventory(input_file, output_file)
