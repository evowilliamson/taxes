import csv
import sys
import glob

def copy_koinly_files(input_pattern, output_file):
    combined_data = []
    headers_set = False  # To ensure headers are written only once

    # Find all files matching the pattern in the ./data_files directory
    input_files = glob.glob(f"./data_files/{input_pattern}")

    if not input_files:
        print(f"No files found matching the pattern: {input_pattern}")
        sys.exit(1)

    # Open the output file in the ./output_files directory
    output_path = f"./output_files/{output_file}"
    with open(output_path, 'w', newline='') as f_output:
        writer = None

        for input_file in input_files:
            with open(input_file, 'r') as f_input:
                reader = csv.DictReader(f_input, delimiter=',')  # Input files are comma-separated
                print(f"Processing file: {input_file}")  # Debugging: show the file being processed

                # Initialize the writer with the headers from the first file
                if not headers_set:
                    writer = csv.DictWriter(f_output, fieldnames=reader.fieldnames, delimiter='\t')  # Output is tab-separated
                    writer.writeheader()
                    headers_set = True

                # Append all rows to the output file
                for row in reader:
                    writer.writerow(row)

    print(f"All data copied to: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python join_koinly.py <input_file_pattern> <output_file>")
        sys.exit(1)

    input_pattern = sys.argv[1]
    output_file = sys.argv[2]

    copy_koinly_files(input_pattern, output_file)
