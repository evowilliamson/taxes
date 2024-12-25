import csv
import sys
from datetime import datetime

def transform_koinly(input_file, output_file, platform):
    output_data = []

    # Read the input trade file
    with open(input_file, 'r') as f:
        reader = csv.DictReader(f, delimiter='\t')

        for row in reader:
            # Skip rows where Type is not "trade"
            if row['Type'] != 'trade':
                continue

            # Extract and transform fields
            date_time = datetime.strptime(row['Date (UTC)'], '%Y-%m-%d %H:%M:%S').strftime('%Y/%m/%d %H:%M:%S')
            source_currency = row['From Currency'].split(';')[0]
            source_amount = row['From Amount']
            target_currency = row['To Currency'].split(';')[0]
            target_amount = row['To Amount']

            # Append the transformed data to the list
            output_data.append({
                'date_time': date_time,
                'source_currency': source_currency,
                'source_amount': source_amount,
                'target_currency': target_currency,
                'target_amount': target_amount,
                'platform': platform
            })

    # Sort the output data by date_time
    output_data.sort(key=lambda x: x['date_time'])

    # Write the transformed and sorted data to the output file
    with open(output_file, 'w', newline='') as f:
        fieldnames = ['date_time', 'source_currency', 'source_amount', 'target_currency', 'target_amount', 'platform']
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
        writer.writerows(output_data)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python Transform_koinly.py <input_file> <output_file> <platform>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    platform = sys.argv[3]

    transform_koinly(input_file, output_file, platform)
