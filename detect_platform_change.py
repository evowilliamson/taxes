import pandas as pd
from datetime import timedelta

# Input and output file names
input_file = "trades_input.tsv"  # Replace with your actual file name
output_file = "platform_changes_10_hours.tsv"

# Read the tab-separated input file into a DataFrame, specifying the header is included
df = pd.read_csv(input_file, sep="\t")

# Convert the date_time column to datetime format
df['date_time'] = pd.to_datetime(df['date_time'], format='%Y/%m/%d %H:%M:%S')

# Sort the DataFrame by date_time
df = df.sort_values(by='date_time').reset_index(drop=True)

# List to store matched trades
output_rows = []

# Compare each trade with subsequent trades
for i in range(len(df) - 1):
    first_trade = df.loc[i]
    second_trade = df.loc[i + 1]
    
    # Check if the platform changes, target_currency of first matches source_currency of second, and time difference < 10 hours
    if (
        first_trade['platform'] != second_trade['platform'] and
        first_trade['target_currency'] == second_trade['source_currency'] and
        (second_trade['date_time'] - first_trade['date_time']) <= timedelta(hours=10)
    ):
        # Add both trades to the output
        output_rows.append(first_trade.to_dict())
        output_rows.append(second_trade.to_dict())

# Deduplicate trades (optional in case of repeated matches)
output_rows = [dict(t) for t in {tuple(d.items()) for d in output_rows}]

# Create an output DataFrame
output_df = pd.DataFrame(output_rows)

# Sort the output by date_time to maintain logical order
output_df = output_df.sort_values(by='date_time')

# Write the result to a tab-separated file
output_df.to_csv(output_file, sep="\t", index=False)

print(f"Trades involved in platform changes have been saved to {output_file}.")
