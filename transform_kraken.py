import csv
import os
from datetime import datetime

def process_kraken_trades(input_file, output_file, platform):
    input_dir = "./data_files"
    output_dir = "./output_files"
    ignored_file = os.path.join(output_dir, f"{platform}_ignored.tsv")
    output_file_path = os.path.join(output_dir, output_file)

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    ignored_trades = []
    transformed_rows = []

    with open(os.path.join(input_dir, input_file), mode='r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    # Process trades
    i = 0
    while i < len(rows):
        current_row = rows[i]

        if current_row['type'] != 'trade':
            i += 1
            continue

        if i + 1 >= len(rows):
            ignored_trades.append(current_row)
            break

        next_row = rows[i + 1]

        if current_row['refid'] != next_row['refid']:
            ignored_trades.append(current_row)
            i += 1
            continue

        if current_row['time'] != next_row['time']:
            print(f"Error: Mismatched time for trades with txid {current_row['txid']} and refid {current_row['refid']}")
            return

        # Determine source and target trades
        if float(current_row['amount']) < 0:
            source_trade = current_row
            target_trade = next_row
        else:
            source_trade = next_row
            target_trade = current_row

        # Transform row
        date_time = datetime.strptime(current_row['time'], "%Y-%m-%d %H:%M:%S").strftime("%Y/%m/%d %H:%M:%S")
        source_currency = source_trade['asset']
        source_amount = abs(float(source_trade['amount']))
        target_currency = target_trade['asset']
        target_amount = float(target_trade['amount'])

        transformed_rows.append({
            "date_time": date_time,
            "source_currency": source_currency,
            "source_amount": source_amount,
            "target_currency": target_currency,
            "target_amount": target_amount,
            "platform": platform
        })

        i += 2

    # Sort transformed rows by date_time
    transformed_rows.sort(key=lambda x: x['date_time'])

    # Write ignored trades
    with open(ignored_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys(), delimiter='\t')
        writer.writeheader()
        writer.writerows(ignored_trades)

    # Write transformed trades
    with open(output_file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["date_time", "source_currency", "source_amount", "target_currency", "target_amount", "platform"], delimiter='\t')
        writer.writeheader()
        writer.writerows(transformed_rows)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: python Kraken_transform.py <input_trade_file> <output_file> <platform>")
    else:
        input_trade_file = sys.argv[1]
        output_file = sys.argv[2]
        platform = sys.argv[3]
        process_kraken_trades(input_trade_file, output_file, platform)
