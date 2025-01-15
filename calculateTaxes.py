from collections import defaultdict, deque
import csv
import os
from datetime import datetime
from decimal import Decimal

def process_trades(input_file, output_file):
    # Initialize dictionaries for purchases and sales
    purchases = defaultdict(deque)
    sales = defaultdict(list)

    # Step 1: Parse input file and classify trades into purchases and sales
    with open(input_file, 'r') as infile:
        reader = csv.DictReader(infile, delimiter='\t')
        for row in reader:
            trade_id = int(row['id'])
            date = row['date_time']
            source_currency = row['source_currency']
            source_amount = Decimal(row['source_amount'])
            target_currency = row['target_currency']
            target_amount = Decimal(row['target_amount'])

            if source_currency == "USD" and target_currency != "USD":
                # It's a purchase
                purchases[target_currency].append({
                    "id": trade_id,
                    "date": date,
                    "usd_paid": source_amount,
                    "amount": target_amount
                })
            elif source_currency != "USD" and target_currency == "USD":
                # It's a sale
                sales[source_currency].append({
                    "id": trade_id,
                    "date": date,
                    "usd_received": target_amount,
                    "amount": source_amount,
                    "profit": Decimal('0.00'),
                    "matched_with_ids": [],
                    "unmatched_amount": ""
                })

    # Step 2: Matching phase
    for currency, sales_list in sales.items():
        purchase_deque = purchases[currency]

        for sale in sales_list:
            while sale['amount'] > 0:
                if not purchase_deque:
                    # Mark sale as unmatched
                    sale['unmatched_amount'] = sale['amount']
                    print(f"Unmatched sale: Amount {sale['amount']} {currency} Trade ID {sale['id']} Date {sale['date']} ")
                    break

                purchase = purchase_deque[0]  # Peek at the earliest purchase

                if sale['date'] >= purchase['date']:
                    # Proceed with matching logic (partial or full match)
                    if purchase['amount'] < sale['amount']:
                        # Partial match logic
                        purchase_deque.popleft()  # Remove fully matched purchase
                        if not purchase_deque:
                            usd_received_sale = sale['usd_received']
                        else:
                            usd_received_sale = sale['usd_received'] * (purchase['amount'] / sale['amount'])
                        sale['profit'] += usd_received_sale - purchase['usd_paid']
                        sale['matched_with_ids'].append(purchase['id'])
                        sale['usd_received'] -= usd_received_sale
                        sale['amount'] -= purchase['amount']
                    else:
                        # Full match logic
                        usd_paid_purchase = (sale['amount'] / purchase['amount']) * purchase['usd_paid']
                        usd_received_sale = sale['usd_received']

                        purchase['amount'] -= sale['amount']
                        purchase['usd_paid'] -= usd_paid_purchase

                        sale['profit'] += sale['usd_received'] - usd_paid_purchase
                        sale['matched_with_ids'].append(purchase['id'])
                        sale['amount'] = Decimal('0.00')  # Sale fully matched

                        sale['usd_received'] -= usd_received_sale  # This line should be included

                        if purchase['amount'] == Decimal('0.00'):
                            purchase_deque.popleft()  # Remove fully matched purchase
                else:
                    # If the earliest purchase date is after the sale date, stop matching for this sale
                    sale['unmatched_amount'] = sale['amount']
                    break

    return sales

def write_output(input_file, output_file, sales):
    """Writes the processed trades to the output file."""
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.DictReader(infile, delimiter='\t')  # Use tab as the delimiter
        fieldnames = reader.fieldnames + ['profit', 'matched_with_ids', 'unmatched_amount']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter='\t')  # Tab-separated output

        writer.writeheader()
        for row in reader:
            # Ensure the row is valid
            if 'id' not in row:
                continue

            trade_id = int(row['id'])
            source_currency = row['source_currency']
            target_currency = row['target_currency']

            if source_currency != 'USD':  # It's a sale
                sales_list = sales[source_currency]
                sale = next((s for s in sales_list if s['id'] == trade_id), None)
                if sale:
                    row['profit'] = round(sale['profit'], 2)
                    row['matched_with_ids'] = ';'.join(map(str, sale['matched_with_ids']))
                    row['unmatched_amount'] = sale['unmatched_amount']
            else:
                row['profit'] = ''
                row['matched_with_ids'] = ''
                row['unmatched_amount'] = ''

            writer.writerow(row)

if __name__ == "__main__":
    input_dir = "data_files"
    output_dir = "output_files"
    input_file = os.path.join(input_dir, "splitted.tsv")
    output_file = os.path.join(output_dir, "output_trades_for_taxes.tsv")

    try:
        sales = process_trades(input_file, output_file)
        write_output(input_file, output_file, sales)
        print(f"Processing completed. Results saved to {output_file}")
    except RuntimeError as e:
        print(str(e))
