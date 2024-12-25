import pandas as pd

# Input and output file names
input_file = "trades_input.tsv"  # Replace with your actual file name
output_file = "stablecoins_used.tsv"

# Read the tab-separated input file into a DataFrame
df = pd.read_csv(input_file, sep="\t")

# Function to check if a currency is a stablecoin
def is_stablecoin(currency):
    return "USD" in currency or "UST" in currency

# Find all unique stablecoins in source_currency and target_currency
stablecoins = set(
    df.loc[df['source_currency'].apply(is_stablecoin), 'source_currency']
).union(
    df.loc[df['target_currency'].apply(is_stablecoin), 'target_currency']
)

# Convert the set of stablecoins to a DataFrame for output
stablecoins_df = pd.DataFrame(stablecoins, columns=["stablecoin"])

# Write the result to a tab-separated file
stablecoins_df.to_csv(output_file, sep="\t", index=False)

print(f"Stablecoins used in the trades have been saved to {output_file}.")
