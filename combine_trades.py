import pandas as pd
from datetime import datetime

# Function to load trades and calculate capital gains
def calculate_capital_gains(input_file, output_file, initial_inventory):
    # Read the input file with correct date parsing (MM/DD/YYYY format)
    trades_df = pd.read_csv(input_file, sep='\t', parse_dates=['time'], dayfirst=False)
    
    # Initialize inventory with initial balances as per 01/01/2022
    inventory = initial_inventory.copy()

    # FIFO tracking for each currency
    fifo_inventory = {
        'USD': [],
        'EUR': [],
        'PAXG': [],
        'XMR': [],
        'BTC': [],
        'ETH': [],
        'XRP': [],
        'PYTH': [],
        'RUNE': []
    }

    # List to store results including profit and matched trade ids
    results = []

    # Iterate through all trades and apply FIFO logic
    for _, row in trades_df.iterrows():
        source_currency = row['source_currency']
        source_amount = row['source_amount']
        buy_currency = row['buy_currency']
        buy_amount = row['buy_amount']
        trade_id = row['id']
        
        matched_with_id = None
        profit = None
        
        # Process sales (when source currency is sold for another currency)
        if source_currency != buy_currency:
            # FIFO matching of previous purchases
            if buy_currency in fifo_inventory:
                remaining_amount = source_amount
                for i, (amount, matched_id) in enumerate(fifo_inventory[buy_currency]):
                    if remaining_amount <= 0:
                        break
                    if amount > 0:
                        # Matching logic: the FIFO method matches earlier purchases with the sale
                        matched_with_id = matched_id
                        amount_to_sell = min(amount, remaining_amount)
                        profit = (amount_to_sell * buy_amount) - (amount_to_sell * amount)  # Profit = sale amount * sale price - purchase amount * purchase price
                        remaining_amount -= amount_to_sell
                        # Decrease the FIFO inventory for the matched amount
                        fifo_inventory[buy_currency][i] = (amount - amount_to_sell, matched_id)

            # After the sale, record the profit and the trade that was matched
            results.append({
                'id': trade_id,
                'time': row['time'],
                'source_currency': source_currency,
                'source_amount': source_amount,
                'buy_currency': buy_currency,
                'buy_amount': buy_amount,
                'profit': profit if profit else 0,  # Fill with 0 if no profit
                'matched_with_id': matched_with_id
            })

        else:
            # Record the purchase and add to FIFO inventory
            fifo_inventory[buy_currency].append((buy_amount, trade_id))

    # Save results to output file
    output_df = pd.DataFrame(results)
    output_df.to_csv(output_file, sep='\t', index=False)

# Define the initial inventory (balance as of 01/01/2022)
initial_inventory = {
    'EUR': 500000,
    'USD': 500000
}

# Define the input and output file paths
input_file = 'input_trades_for_taxes.tsv'
output_file = 'output_trades_with_profits.tsv'

# Call the function to calculate capital gains and write to the output file
calculate_capital_gains(input_file, output_file, initial_inventory)
