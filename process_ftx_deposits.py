import os
import re
import email
from email.policy import default
from datetime import datetime

# Define paths
input_folder = "/home/ivo/Downloads/ftx/deposits"
output_file = "deposits_output.tsv"

# Regular expressions to match the required patterns
deposit_pattern = re.compile(r"deposit of ([\d.]+) (\w+)")
header_pattern = re.compile(r"X-MS-Exchange-CrossTenant-OriginalArrivalTime: (\d{2} \w{3} \d{4} \d{2}:\d{2}:\d{2}\.\d+)")

# Function to convert date-time format
def convert_date_time(date_time_str):
    # Input format: DD month YYYY HH:MM:SS.ms
    # Desired format: YYYY/MM/DD HH:MM:SS
    date_obj = datetime.strptime(date_time_str.split('.')[0], "%d %b %Y %H:%M:%S")
    return date_obj.strftime("%Y/%m/%d %H:%M:%S")

# Open the output file for writing
with open(output_file, "w") as out_file:
    # Write header to the output file
    out_file.write("DateTime\tAmount\tCoin\tFilename\n")

    # Iterate over all .eml files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".eml"):
            file_path = os.path.join(input_folder, filename)

            try:
                # Open and parse the .eml file
                with open(file_path, "r") as eml_file:
                    msg = email.message_from_file(eml_file, policy=default)

                    # Get the email body
                    if msg.is_multipart():
                        body = ""
                        for part in msg.iter_parts():
                            if part.get_content_type() == "text/plain":
                                body = part.get_content()
                                break
                    else:
                        body = msg.get_content()

                    # Search for the deposit pattern in the email body
                    deposit_match = deposit_pattern.search(body)

                    # Search for the date-time in the headers
                    headers = msg.as_string()
                    header_match = header_pattern.search(headers)

                    if deposit_match and header_match:
                        amount, coin = deposit_match.groups()
                        raw_date_time = header_match.group(1)
                        formatted_date_time = convert_date_time(raw_date_time)

                        # Write the extracted data to the output file
                        out_file.write(f"{formatted_date_time}\t{amount}\t{coin}\t{filename}\n")

            except Exception as e:
                print(f"Error processing file {filename}: {e}")

# Remove duplicate lines from the output file
def remove_duplicates(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
    
    # Remove duplicates while preserving order
    unique_lines = list(dict.fromkeys(lines))
    
    # Write back the unique lines
    with open(file_path, "w") as file:
        file.writelines(unique_lines)

# Call the function to remove duplicates
remove_duplicates(output_file)

print(f"Processing complete. Results saved in {output_file}")
