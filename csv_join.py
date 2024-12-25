import os
import pandas as pd

# Directory containing the CSV files
directory = "/home/ivo/Downloads/ethereum"
# Output file path
output_file = "/home/ivo/Downloads/ethereum/eth_all.csv"

# List to hold DataFrames
dataframes = []

# Iterate through all files in the directory
for filename in os.listdir(directory):
    # Check if the file is a CSV file
    if filename.endswith(".csv"):
        file_path = os.path.join(directory, filename)
        # Read the CSV file and append it to the list of DataFrames
        df = pd.read_csv(file_path)
        dataframes.append(df)

# Combine all DataFrames into one
combined_df = pd.concat(dataframes, ignore_index=True)

# Write the combined DataFrame to a new CSV file
combined_df.to_csv(output_file, index=False)

print(f"Combined CSV file created: {output_file}")