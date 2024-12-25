import pandas as pd

# Define input and output file paths
input_file = "trades_input.tsv"  # Replace with your input file name
output_file = "trades_filtered.tsv"  # Output file name

# Load the TSV file into a DataFrame
trades_df = pd.read_csv(input_file, sep="\t")

# Filter out rows where both sell_asset_usd and buy_asset_usd are "USD"
filtered_trades = trades_df[
    ~((trades_df["sell_asset_usd"] == "USD") & (trades_df["buy_asset_usd"] == "USD"))
]

# Save the filtered trades to a new TSV file
filtered_trades.to_csv(output_file, sep="\t", index=False)

print(f"Filtered trades saved to {output_file}")
