import csv

# File paths
input_file = 'split_input_file.tsv'
output_file = 'split_output_file.tsv'
error_file = 'error_log.tsv'

def process_trades(input_file, output_file, error_file):
    # Initialize counters
    total_input_rows = 0
    total_extra_trades = 0
    total_output_rows = 0
    trade_id = 1  # Initialize trade ID

    # Open files
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile, \
         open(output_file, mode='w', newline='', encoding='utf-8') as outfile, \
         open(error_file, mode='w', newline='', encoding='utf-8') as errfile:

        # Set up readers and writers
        reader = csv.DictReader(infile, delimiter='\t')
        fieldnames = ['id', 'date_time', 'source_currency', 'source_amount', 'target_currency', 'target_amount', 'platform']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter='\t')
        error_writer = csv.DictWriter(errfile, fieldnames=reader.fieldnames, delimiter='\t')

        # Write headers
        writer.writeheader()
        error_writer.writeheader()

        row_id = 0
        # Process each row
        for row in reader:
            row_id += 1
            total_input_rows += 1

            try:
                split = row['split'].strip().upper()
                if split == 'TRUE':
                    int_amt = row.get('int_amt', '').strip()
                    if not int_amt or int_amt == '#N/A':
                        # Log to error file if int_amt is invalid
                        error_writer.writerow(row)
                        continue

                    # Write first trade: source_currency -> USD
                    writer.writerow({
                        'id': trade_id,
                        'date_time': row['date_time'],
                        'source_currency': row['source_currency'],
                        'source_amount': row['source_amount'],
                        'target_currency': 'USD',
                        'target_amount': int_amt,
                        'platform': row['platform']
                    })
                    trade_id += 1
                    total_extra_trades += 1

                    # Write second trade: USD -> target_currency
                    writer.writerow({
                        'id': trade_id,
                        'date_time': row['date_time'],
                        'source_currency': 'USD',
                        'source_amount': int_amt,
                        'target_currency': row['target_currency'],
                        'target_amount': row['target_amount'],
                        'platform': row['platform']
                    })
                    trade_id += 1
                else:
                    # Write original trade
                    writer.writerow({
                        'id': trade_id,
                        'date_time': row['date_time'],
                        'source_currency': row['source_currency'],
                        'source_amount': row['source_amount'],
                        'target_currency': row['target_currency'],
                        'target_amount': row['target_amount'],
                        'platform': row['platform']
                    })
                    trade_id += 1

            except Exception as e:
                # Log problematic rows to the error file
                error_writer.writerow(row)

        # Count total rows in the output file
        total_output_rows = total_input_rows + total_extra_trades

    # Print summary
    print(f"Total rows in input file: {total_input_rows}")
    print(f"Total extra trades created: {total_extra_trades}")
    print(f"Total rows in output file: {total_output_rows}")

# Run the function
process_trades(input_file, output_file, error_file)
