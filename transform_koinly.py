import csv
import sys
import glob
from datetime import datetime

def transform_koinly_files(input_pattern, output_file, platform):
    combined_data = []

    # Find all files matching the pattern in the ./data_files directory
    input_files = glob.glob(f"./data_files/{input_pattern}")

    if not input_files:
        print(f"No files found matching the pattern: {input_pattern}")
        sys.exit(1)

    for input_file in input_files:
        with open(input_file, 'r') as f:
            reader = csv.DictReader(f, delimiter=',')  # Input files are comma-separated
            print(f"Headers in file: {reader.fieldnames}")  # Debugging headers

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

                # Append transformed data to the combined list
                combined_data.append({
                    'date_time': date_time,
                    'source_currency': source_currency,
                    'source_amount': source_amount,
                    'target_currency': target_currency,
                    'target_amount': target_amount,
                    'platform': platform
                })

    # Sort combined data by date_time
    combined_data.sort(key=lambda x: datetime.strptime(x['date_time'], '%Y/%m/%d %H:%M:%S'))

    # Write sorted data to the output file in the ./output_files directory
    output_path = f"./output_files/{output_file}"
    with open(output_path, 'w', newline='') as f:
        fieldnames = ['date_time', 'source_currency', 'source_amount', 'target_currency', 'target_amount', 'platform']
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='\t')  # Output file is tab-separated
        writer.writeheader()
        writer.writerows(combined_data)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python Transform_koinly.py <input_file_pattern> <output_file> <platform>")
        sys.exit(1)

    input_pattern = sys.argv[1]
    output_file = sys.argv[2]
    platform = sys.argv[3]

    transform_koinly_files(input_pattern, output_file, platform)
