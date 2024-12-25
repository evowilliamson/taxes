import pandas as pd

# Input and output file names
input_file = "trades_input.tsv"  # Replace with your actual file name
output_file = "trades_with_non_usd_both.tsv"

# Read the tab-separated input file into a DataFrame
df = pd.read_csv(input_file, sep="\t")

# Add a new column 'non_usd_both' indicating whether both source and target currencies are not 'USD'
df['non_usd_both'] = (df['source_currency'] != 'USD') & (df['target_currency'] != 'USD')

# Write the updated DataFrame to a tab-separated file
df.to_csv(output_file, sep="\t", index=False)

print(f"Processed trades with 'non_usd_both' column have been saved to {output_file}.")
