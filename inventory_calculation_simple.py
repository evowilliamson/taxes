import csv
from collections import defaultdict

# Starting inventory
inventory = {
    "EUR": 100000,
    "USD": 100000,
    "PAXG": 0,
    "BTC": 0,
    "LTC": 0,
    "ETH": 0,
    "SOL": 0,
    "LUNA": 0
}

# Initialize peak and minimum inventory trackers
peak_inventory = inventory.copy()
min_inventory = {coin: float("inf") for coin in inventory}

# Update minimum inventory, ignoring starting value of 0
for coin, amount in inventory.items():
    if amount > 0:
        min_inventory[coin] = amount

# Read and process trades from the input file
input_file = "input_trades.tsv"
output_file = "output_inventory.tsv"

def process_trades(file_path, output_path):
    global inventory, peak_inventory, min_inventory

    def normalize_currency(currency):
        # Add mappings if needed (e.g., WBTC -> BTC)
        return currency

    no_btc = 0

    with open(file_path, "r", newline="") as csvfile, open(output_path, "w", newline="") as outfile:
        reader = csv.DictReader(csvfile, delimiter="\t")
        fieldnames = ["date_time", "platform"] + list(inventory.keys())
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()

        for row in reader:
            date_time = row["date_time"]
            platform = row["platform"]
            source_currency = normalize_currency(row["source_currency"])
            source_amount = float(row["source_amount"])
            target_currency = normalize_currency(row["target_currency"])
            target_amount = float(row["target_amount"])

            # Subtract source amount from inventory if tracked
            if source_currency in inventory:
                inventory[source_currency] -= source_amount
                if source_currency == "BTC":
                    no_btc -= source_amount
                # Update minimum inventory, if applicable
                if inventory[source_currency] != 0:
                    min_inventory[source_currency] = min(
                        min_inventory[source_currency], inventory[source_currency]
                    )

            # Add target amount to inventory if tracked
            if target_currency in inventory:
                inventory[target_currency] += target_amount
                if target_currency == "BTC":
                    no_btc += target_amount
                # Update peak inventory, if applicable
                peak_inventory[target_currency] = max(
                    peak_inventory[target_currency], inventory[target_currency]
                )

            # Debugging print to verify accuracy
            print(f"Processing trade: {row}")
            print(f"Source: {source_currency}, Amount: {source_amount}")
            print(f"Target: {target_currency}, Amount: {target_amount}")
            print(f"Updated Inventory: {inventory}")

            # Write the current inventory state to the output file
            row_data = {"date_time": date_time, "platform": platform}
            row_data.update({coin: round(inventory[coin], 8) for coin in inventory})
            writer.writerow(row_data)


        print("fjdskfjdskljfd" + str(no_btc))

# Process the input trades and write to output file
process_trades(input_file, output_file)

# Replace `float("inf")` in min_inventory with `0` for coins that remained untracked or had no positive inventory
for coin, min_val in min_inventory.items():
    if min_val == float("inf") or min_val == 0:
        min_inventory[coin] = 0

# Print final inventory and peak/min values
print("Final Inventory:")
for coin, amount in inventory.items():
    print(f"{coin}: {amount:.8f}")

print("\nPeak Inventory:")
for coin, amount in peak_inventory.items():
    print(f"{coin}: {amount:.8f}")

print("\nMinimum Inventory:")
for coin, amount in min_inventory.items():
    print(f"{coin}: {amount:.8f}")
