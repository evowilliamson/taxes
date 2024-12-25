import pandas as pd
import datetime

def load_conversion_rates(conversion_file):
    # Load the conversion file into a pandas DataFrame
    conversion_df = pd.read_csv(conversion_file, sep='\t', parse_dates=['Date'], dayfirst=False)
    # Ensure the 'Date' column is in the correct format
    conversion_df['Date'] = pd.to_datetime(conversion_df['Date'], format='%m/%d/%Y')
    return conversion_df

def process_trades(trade_file, conversion_files):
    # Load the trades file into a pandas DataFrame
    trades_df = pd.read_csv(trade_file, sep='\t', parse_dates=['time'], dayfirst=False)
    
    # Ensure the 'time' column is in the correct format
    trades_df['time'] = pd.to_datetime(trades_df['time'], format='%m/%d/%Y')

    new_trades = []
    
    # Iterate over the rows of the trades DataFrame
    for index, row in trades_df.iterrows():
        sell_asset = row['sell_asset_usd']
        buy_asset = row['buy_asset_usd']
        
        # If the trade is between non-USD assets (e.g., XMR/BTC, ETH/XRP), we need to split it into two trades
        if '/' in sell_asset and '/' in buy_asset:
            # Look up conversion rates for the specific assets (XMR/BTC, ETH/XRP, etc.) based on the date
            conversion_file = f"{sell_asset}{buy_asset}.tsv"
            conversion_df = load_conversion_rates(conversion_file)
            
            # Check if conversion rates are available for the specific date
            date_conversion = conversion_df[conversion_df['Date'] == row['time']]
            if not date_conversion.empty:
                conversion_rate = date_conversion.iloc[0]['value']
                
                # Create two new trades: one for the sell to USD and one for USD to buy
                new_trades.append({
                    'time': row['time'],
                    'sell_asset_usd': sell_asset,
                    'sell_amount_usd': row['sell_amount_usd'] * conversion_rate,
                    'buy_asset_usd': 'USD',
                    'buy_amount_usd': row['sell_amount_usd']
                })
                new_trades.append({
                    'time': row['time'],
                    'sell_asset_usd': 'USD',
                    'sell_amount_usd': row['buy_amount_usd'],
                    'buy_asset_usd': buy_asset,
                    'buy_amount_usd': row['buy_amount_usd'] / conversion_rate
                })
            else:
                print(f"No conversion rate found for {sell_asset}/{buy_asset} on {row['time']}")
        else:
            # For trades that involve USD or stablecoins, we just copy the row as is
            new_trades.append({
                'time': row['time'],
                'sell_asset_usd': sell_asset,
                'sell_amount_usd': row['sell_amount_usd'],
                'buy_asset_usd': buy_asset,
                'buy_amount_usd': row['buy_amount_usd']
            })

    # Convert the new trades list back into a DataFrame
    new_trades_df = pd.DataFrame(new_trades)
    
    return new_trades_df

# Example usage
trade_file = 'trades.tsv'  # Path to your trades file
conversion_files = ['XMRBTC.tsv', 'ETHXRP.tsv']  # Conversion rate files for XMR/BTC, ETH/XRP

new_trades_df = process_trades(trade_file, conversion_files)

# Save the processed trades to a new file
new_trades_df.to_csv('processed_trades.tsv', sep='\t', index=False)
