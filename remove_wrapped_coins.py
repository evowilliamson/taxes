import csv
from datetime import datetime
import sys

# Define the list of currencies for processing
currency_list = ["ETH", "MSOL", "SOL", "BTC"]

def process_trade_file(input_file, output_file, platform):
    ignored_trades = []
    output_trades = []

    # Read the trade file
    with open(input_file, 'r') as f:
        reader = csv.DictReader(f, delimiter='\t')
        trades = list(reader)

    # Process each trade
    for trade in trades:
        from_currency = trade['source_currency']
        to_currency = trade['target_currency']

        # Replace currencies based on rules
        for currency in currency_list:
            if currency != "SOL":
                if currency in to_currency:
                    to_currency = currency
                if currency in from_currency:
                    from_currency = currency
            else:
                if "SOL" in to_currency and "MSOL" not in to_currency:
                    to_currency = "SOL"
                if "SOL" in from_currency and "MSOL" not in from_currency:
                    from_currency = "SOL"

        # Update the trade with replaced currencies
        trade['source_currency'] = from_currency
        trade['target_currency'] = to_currency

        # Classify the trade
        if from_currency == to_currency:
            ignored_trades.append(trade)
        else:
            output_trades.append(trade)

    # Sort output trades by date_time
    output_trades.sort(key=lambda x: datetime.strptime(x['date_time'], '%Y/%m/%d %H:%M:%S'))

    # Write ignored trades to <platform>_ignored.tsv
    with open(f"{platform}_ignored.tsv", 'w', newline='') as ignored_file:
        writer = csv.DictWriter(ignored_file, fieldnames=trades[0].keys(), delimiter='\t')
        writer.writeheader()
        writer.writerows(ignored_trades)

    # Write output trades to the specified output file
    with open(output_file, 'w', newline='') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=trades[0].keys(), delimiter='\t')
        writer.writeheader()
        writer.writerows(output_trades)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python Remove_wrapped_coins.py <input_file> <output_file> <platform>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    platform = sys.argv[3]

    process_trade_file(input_file, output_file, platform)
