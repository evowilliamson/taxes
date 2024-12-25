import pandas as pd
import sys

# File paths
input_file = "input_file_binance.tsv"  # Replace with the path to your input file
output_file = "output_file_binance.tsv"  # Replace with the desired output file path

try:
    # Step 1: Read the input CSV file
    df = pd.read_csv(input_file)

    # Step 2: Group by 'UTC_Time', 'Operation', and 'Coin', and sum the 'Change'
    grouped_df = (
        df.groupby(["UTC_Time", "Operation", "Coin"], as_index=False)["Change"]
        .sum()
        .rename(columns={"Change": "sum"})
    )

    # Step 3: Save the grouped data to a tab-separated output file
    grouped_df.to_csv(output_file, sep="\t", index=False)

    # Step 4: Read the output TSV file for validation
    output_df = pd.read_csv(output_file, sep="\t")

    # Step 5: Validate the 'UTC_Time' for every two consecutive rows
    for i in range(0, len(output_df) - 1, 2):
        if output_df.iloc[i]["UTC_Time"] != output_df.iloc[i + 1]["UTC_Time"]:
            print(f"Validation failed at row {i + 2} (1-based index)")
            sys.exit(1)

    print(f"Processing and validation completed successfully. Output saved to {output_file}.")

except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)
