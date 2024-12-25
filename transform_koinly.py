import csv
from datetime import datetime

def process_trade_file(input_file):
    platform_name = input_file.split('.')[0]
    output_file = f"{platform_name}_output.tsv"
    ignored_trades_file = f"{platform_name}_ignored_trades.tsv"
    assumed_linked_currencies = set()
    valid_rows = []
    ignored_rows = []

    def is_linked_currency_trade(source_amount, target_amount):
        """
        Determines if the trade is likely between linked currencies.
        """
        amount_difference = abs(source_amount - target_amount) / max(source_amount, target_amount)
        return amount_difference < 0.01

    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile, delimiter='\t')

        for row in reader:
            # Skip rows where Type is not "trade"
            if row['Type'] != 'trade':
                continue

            # Extract and format fields
            date_time = datetime.strptime(row['Date (UTC)'], '%Y-%m-%d %H:%M:%S').strftime('%Y/%m/%d %H:%M:%S')
            source_currency = row['From Currency'].split(';')[0]
            source_amount = float(row['From Amount'])
            target_currency = row['To Currency'].split(';')[0]
            target_amount = float(row['To Amount'])

            # Prepare the output row structure
            prepared_row = [
                date_time,
                source_currency,
                source_amount,
                target_currency,
                target_amount,
                platform_name
            ]

            # Check for linked currency trades
            if is_linked_currency_trade(source_amount, target_amount):
                assumed_linked_currencies.add(source_currency)
                assumed_linked_currencies.add(target_currency)
                ignored_rows.append(prepared_row)  # Save the prepared row to the ignored trades file
                continue  # Skip this row

            # Add valid rows to the list
            valid_rows.append(prepared_row)

    # Sort valid rows by date_time
    valid_rows.sort(key=lambda x: x[0])

    # Write the valid trades to the output file
    with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile, delimiter='\t')
        writer.writerow(['date_time', 'source_currency', 'source_amount', 'target_currency', 'target_amount', 'platform'])
        writer.writerows(valid_rows)

    # Write the ignored trades to the ignored trades file
    with open(ignored_trades_file, 'w', encoding='utf-8', newline='') as ignored_file:
        writer = csv.writer(ignored_file, delimiter='\t')
        writer.writerow(['date_time', 'source_currency', 'source_amount', 'target_currency', 'target_amount', 'platform'])
        writer.writerows(ignored_rows)

    # Print the assumed linked currencies
    print("Assumed linked currencies:", sorted(assumed_linked_currencies))

# Example usage
# Replace 'example_file.tsv' with the actual file name
process_trade_file('evm.tsv')
