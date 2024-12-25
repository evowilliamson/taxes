import pandas as pd

# Input file name
input_file = "trades_input.tsv"  # Replace with your actual file name

# Currencies to exclude
excluded_currencies = {"ETH", "BTC", "USD", "EUR"}

# Read the tab-separated input file into a DataFrame
df = pd.read_csv(input_file, sep="\t")

# Filter rows where both source_currency and target_currency are not in the excluded list
filtered_pairs = df[
    (~df['source_currency'].isin(excluded_currencies)) &
    (~df['target_currency'].isin(excluded_currencies))
]

# Extract unique currency pairs in the format "source/target"
unique_pairs = filtered_pairs[['source_currency', 'target_currency']].drop_duplicates()
unique_pairs['pair'] = unique_pairs['source_currency'] + "/" + unique_pairs['target_currency']

# Output the unique pairs to the console
for pair in unique_pairs['pair']:
    print(pair)
