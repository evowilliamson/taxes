import os
import csv
import sys

def replace_currency(currency, stablecoins_list, not_stablecoins_list):
    """
    Replace currency based on the stablecoins and not_stablecoins lists.
    """
    if currency in stablecoins_list:
        return 'USD'
    if any(substring in currency for substring in ['US', 'FRAX', 'DAI']) and currency not in not_stablecoins_list:
        return 'USD'
    return currency

def process_trades(input_file, output_file, platform, stablecoins_list, not_stablecoins_list):
    """
    Process the trade file based on the given rules and write the output file.
    """
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' does not exist.")
        return

    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.DictReader(infile, delimiter='\t')
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()

        for row in reader:
            # Filter by platform
            if row['platform'] != platform:
                continue

            # Replace currencies based on the rules
            source_currency = replace_currency(row['source_currency'], stablecoins_list, not_stablecoins_list)
            target_currency = replace_currency(row['target_currency'], stablecoins_list, not_stablecoins_list)

            # Skip trades where both currencies are 'USD'
            if source_currency == 'USD' and target_currency == 'USD':
                continue

            # Write updated trade to output
            row['source_currency'] = source_currency
            row['target_currency'] = target_currency
            writer.writerow(row)

if __name__ == "__main__":
    # Command-line arguments
    if len(sys.argv) != 4:
        print("Usage: python convert_usd_stablecoins.py <input_file> <output_file> <platform>")
        sys.exit(1)

    input_file = os.path.join('./data_files', sys.argv[1])
    output_file = os.path.join('./output_files', sys.argv[2])
    platform = sys.argv[3]

    # Stablecoins and not stablecoins lists
    stablecoins_list = ['FRAX', 'UST', 'USTC', 'MIM', 'CASH', 'DAI']
    not_stablecoins_list = ['CUSDC']

    # Process the trade file
    process_trades(input_file, output_file, platform, stablecoins_list, not_stablecoins_list)

    print(f"Processing complete. Output file generated at: {output_file}")
