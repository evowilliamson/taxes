import pandas as pd

# Input and output file names
input_file = "trades_input.tsv"  # Replace with your actual file name
output_file = "filtered_trades.tsv"

# Read the tab-separated input file into a DataFrame
df = pd.read_csv(input_file, sep="\t")

# Filter out rows where both source_currency and target_currency are 'USD'
filtered_df = df[~(((df['source_currency'] == 'USD') & (df['target_currency'] == 'USD')) |
                   ((df['source_currency'] == 'BTC') & (df['target_currency'] == 'BTC')))]

# Write the filtered DataFrame to a tab-separated file
filtered_df.to_csv(output_file, sep="\t", index=False)

print(f"Filtered trades have been saved to {output_file}.")
