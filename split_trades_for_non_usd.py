import csv
import os
import sys

def process_trades(input_file, output_file):
    trades = []
    trade_id = 1

    # Construct full paths
    input_path = os.path.join('./data_files', input_file)
    output_path = os.path.join('./output_files', output_file)

    # Read the input file
    with open(input_path, 'r', newline='') as infile:
        reader = csv.DictReader(infile, delimiter='\t')
        for row in reader:
            if row['split'] == 'FALSE':
                # Copy row as is for split = FALSE
                trades.append({
                    'id': trade_id,
                    'date_time': row['date_time'],
                    'source_currency': row['source_currency'],
                    'source_amount': row['src_amount'],
                    'target_currency': row['target_currency'],
                    'target_amount': row['tgt_amount'],
                    'platform': row['platform'],
                })
                trade_id += 1
            elif row['split'] == 'TRUE':
                # Create Sell Row
                trades.append({
                    'id': trade_id,
                    'date_time': row['date_time'],
                    'source_currency': row['source_currency'],
                    'source_amount': row['src_amount'],
                    'target_currency': 'USD',
                    'target_amount': row['int_amt'],
                    'platform': row['platform'],
                })
                trade_id += 1

                # Create Buy Row
                trades.append({
                    'id': trade_id,
                    'date_time': row['date_time'],
                    'source_currency': 'USD',
                    'source_amount': row['int_amt'],
                    'target_currency': row['target_currency'],
                    'target_amount': row['tgt_amount'],
                    'platform': row['platform'],
                })
                trade_id += 1

    # Write to the output file
    with open(output_path, 'w', newline='') as outfile:
        fieldnames = ['id', 'date_time', 'source_currency', 'source_amount', 'target_currency', 'target_amount', 'platform']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
        writer.writerows(trades)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    process_trades(input_file, output_file)
