import re
from datetime import datetime

# Input and output file names
input_file = "input.txt"
output_file = "kraken_euro_deposits.tsv"

# Function to process the input file and generate the output
def process_deposits(input_file, output_file):
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        # Write the header to the output file
        outfile.write("Date\tAmount\n")

        lines = infile.readlines()
        i = 0
        while i < len(lines):
            line = lines[i].strip()

            if line == "Deposited Euro":
                # Get the date on the next line
                i += 1
                date_line = lines[i].strip()

                # Format the date
                date_match = re.match(r"(\w+ \d{1,2}, \d{4}) at (\d{2}:\d{2})", date_line)
                if date_match:
                    date_str = f"{date_match.group(1)} {date_match.group(2)}"
                    date = datetime.strptime(date_str, "%B %d, %Y %H:%M")
                    formatted_date = date.strftime("%Y/%m/%d %H:%M")
                else:
                    raise ValueError(f"Invalid date format: {date_line}")

                # Get the amount on the next line
                i += 1
                amount_line = lines[i].strip()
                amount_match = re.match(r"€([\d,]+\.\d{2})", amount_line)
                if amount_match:
                    amount = amount_match.group(1).replace(",", "")
                else:
                    raise ValueError(f"Invalid amount format: {amount_line}")

                # Write the formatted date and amount to the output file
                outfile.write(f"{formatted_date}\t{amount}\n")

            # Move to the next line
            i += 1

# Execute the script
if __name__ == "__main__":
    process_deposits(input_file, output_file)
    print(f"Processed deposits written to {output_file}")