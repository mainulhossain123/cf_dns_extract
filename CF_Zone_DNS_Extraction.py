import requests
import csv
import os
from datetime import datetime, timezone
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Fetch environment variables for API key, account ID, and output location
API_KEY = os.getenv("API_KEY")  # Ensure to set this as an environment variable
ACCOUNT_ID = os.getenv("ACCOUNT_ID")  # Ensure to set this as an environment variable
OUTPUT_PREFIX = os.getenv("OUTPUT_FILENAME_PREFIX")  # No default, must be provided or prompted

# Validate API_KEY and ACCOUNT_ID
if not API_KEY or not ACCOUNT_ID:
    raise ValueError("Both API_KEY and ACCOUNT_ID must be set as environment variables.")

# Prompt for output prefix if not provided
if not OUTPUT_PREFIX:
    print("Error: OUTPUT_FILENAME_PREFIX is not set.")
    OUTPUT_PREFIX = input("Please enter a file name prefix (e.g., CF_D): ").strip()

    if not OUTPUT_PREFIX:
        raise ValueError("A valid file name prefix is required to proceed.")

# Sanitize the output prefix
OUTPUT_PREFIX = OUTPUT_PREFIX.replace(" ", "_").replace("/", "_")

# Ensure the filename ends with .csv
if not OUTPUT_PREFIX.endswith(".csv"):
    OUTPUT_PREFIX += ".csv"

# Default to /app as the output directory for container compatibility
DEFAULT_OUTPUT_DIR = "/app"
OUTPUT_DIR = os.getenv("OUTPUT_DIR", DEFAULT_OUTPUT_DIR)  # Use default /app if not set

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Generate full output path
FULL_OUTPUT_PATH = os.path.join(OUTPUT_DIR, OUTPUT_PREFIX)

# Output file information
print(f"Output file will be saved to: {FULL_OUTPUT_PATH}")

# Create a session to reuse HTTP connections
session = requests.Session()

def get_zones(api_key, account_id, page, per_page):
    """Fetch zones for the specified account."""
    url = "https://api.cloudflare.com/client/v4/zones"
    headers = {"Authorization": f"Bearer {api_key}"}
    params = {"page": page, "per_page": per_page}
    
    retries = 3
    for _ in range(retries):
        response = session.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and isinstance(data.get('result'), list):
                return data['result']  # Return the list of zones
        time.sleep(1)
    return []  # Return an empty list if no valid result

def get_dns_records(zone_id, api_key):
    """Fetch DNS records for a specific zone."""
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    retries = 3
    for _ in range(retries):
        response = session.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get('result', [])
        time.sleep(1)
    return []

def fetch_zone_data(zone, api_key):
    """Fetch DNS records for a zone and format the data."""
    dns_records = get_dns_records(zone['id'], api_key)
    zone_data = []
    for record in dns_records:
        zone_data.append([
            zone['name'],  # Zone Name
            record['name'],  # Hostname
            record['type'],  # DNS Type
            record['content']  # DNS Value
        ])
    return zone_data

def write_to_csv(data, filename):
    """Write collected data to a CSV file."""
    with open(filename, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        # Write header
        csv_writer.writerow(["Zone Name", "Hostname", "DNS Type", "DNS Value"])
        # Write data rows
        csv_writer.writerows(data)

if __name__ == "__main__":
    page = 1
    per_page = 100
    all_zones = []
    
    # Fetch all zones across all pages
    print("Fetching zones...")
    while True:
        zones = get_zones(API_KEY, ACCOUNT_ID, page, per_page)
        if not zones:  # Stop when no zones are returned (end of pagination)
            break
        # Filter zones by account ID
        matching_zones = [zone for zone in zones if zone['account']['id'] == ACCOUNT_ID]
        all_zones.extend(matching_zones)
        print(f"Fetched page {page}, {len(matching_zones)} matching zones")
        page += 1


    print(f"Total zones fetched: {len(all_zones)}")

    # Use ThreadPoolExecutor to fetch DNS records in parallel
    dns_data = []
    print("Fetching DNS records...")
    with ThreadPoolExecutor(max_workers=12) as executor:
        future_to_zone = {executor.submit(fetch_zone_data, zone, API_KEY): zone for zone in all_zones}
        for future in as_completed(future_to_zone):
            try:
                dns_data.extend(future.result())
            except Exception as e:
                print(f"Error processing zone: {e}")

    # Write results to CSV
    print(f"Writing data to {FULL_OUTPUT_PATH}...")
    write_to_csv(dns_data, FULL_OUTPUT_PATH)
    print("Done!")

