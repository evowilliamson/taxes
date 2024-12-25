import csv
import sys
from datetime import datetime

# Define the list of currencies for processing
currency_list = ["ETH", "MSOL", "SOL", "BTC", "AVAX", "BNB", "FTM"]

def process_trades(input_file, output_file, platform):
    ignored_trades = []
    output_trades = []

    # Read the trade file from ./data_files
    input_path = f"./data_files/{input_file}"
    with open(input_path, 'r') as f:
        reader = csv.DictReader(f, delimiter='\t')
        trades = list(reader)

    # Process each trade
    for trade in trades:
        original_from_currency = trade['source_currency']
        original_to_currency = trade['target_currency']
        from_currency = original_from_currency
        to_currency = original_to_currency

        # Replace currencies based on rules
        for currency in currency_list:
            if currency != "SOL":
                if currency in to_currency:
                    to_currency = currency
                if currency in from_currency:
                    from_currency = currency
            else:
                if "SOL" in to_currency and "MSOL" not in to_currency and "SOLUST" not in to_currency:
                    to_currency = "SOL"
                if "SOL" in from_currency and "MSOL" not in from_currency and "SOLUST" not in from_currency:
                    from_currency = "SOL"

        # Classify the trade
        if from_currency == to_currency:
            ignored_trades.append({
                'date_time': trade['date_time'],
                'source_currency': original_from_currency,
                'source_amount': trade['source_amount'],
                'target_currency': original_to_currency,
                'target_amount': trade['target_amount'],
                'platform': trade['platform']
            })
        else:
            output_trades.append({
                'date_time': trade['date_time'],
                'source_currency': from_currency,
                'source_amount': trade['source_amount'],
                'target_currency': to_currency,
                'target_amount': trade['target_amount'],
                'platform': trade['platform']
            })

    # Sort output trades by date_time
    output_trades.sort(key=lambda x: datetime.strptime(x['date_time'], '%Y/%m/%d %H:%M:%S'))

    # Write ignored trades to ./output_files/<platform>_ignored.tsv
    ignored_path = f"./output_files/{platform}_ignored.tsv"
    with open(ignored_path, 'w', newline='') as ignored_file:
        fieldnames = ['date_time', 'source_currency', 'source_amount', 'target_currency', 'target_amount', 'platform']
        writer = csv.DictWriter(ignored_file, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
        writer.writerows(ignored_trades)

    # Write output trades to the specified output file
    output_path = f"./output_files/{output_file}"
    with open(output_path, 'w', newline='') as output_file:
        fieldnames = ['date_time', 'source_currency', 'source_amount', 'target_currency', 'target_amount', 'platform']
        writer = csv.DictWriter(output_file, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
        writer.writerows(output_trades)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python Remove_wrapped_coins.py <input_trade_file> <output_file> <platform>")
        sys.exit(1)

    input_trade_file = sys.argv[1]
    output_file = sys.argv[2]
    platform = sys.argv[3]

    process_trades(input_trade_file, output_file, platform)
