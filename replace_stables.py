import pandas as pd

# Input and output file names
input_file = "trades_input.tsv"  # Replace with your actual file name
output_file = "trades_output.tsv"

# List of stablecoins to be replaced with "USD"
stablecoins = {"BUSD", "UST", "USDC", "USDN", "USDT", "USD"}

# Read the tab-separated input file into a DataFrame
df = pd.read_csv(input_file, sep="\t")

# Replace stablecoins in the source_currency and target_currency columns
df['source_currency'] = df['source_currency'].apply(lambda x: 'USD' if x in stablecoins else x)
df['target_currency'] = df['target_currency'].apply(lambda x: 'USD' if x in stablecoins else x)

# Write the modified DataFrame to a tab-separated file
df.to_csv(output_file, sep="\t", index=False)

print(f"Processed trades have been saved to {output_file}.")
