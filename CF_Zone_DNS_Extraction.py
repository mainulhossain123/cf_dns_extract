import requests
import csv
import os
from datetime import datetime, timezone
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Fetch API key and account name from environment variables
API_KEY = os.getenv("API_KEY")  # Ensure to set this as an environment variable
ACCOUNT_NAME = os.getenv("ACCOUNT_NAME")  # Ensure to set this as an environment variable
OUTPUT_PREFIX = os.getenv("OUTPUT_FILENAME_PREFIX") # Default Set to CF if not set

if not API_KEY or not ACCOUNT_NAME:
    raise ValueError("Both API_KEY and ACCOUNT_NAME must be set as environment variables.")

# Sanitize the account name to make it file-system safe
#safe_account_name = ACCOUNT_NAME.replace(" ", "_").replace("/", "_")
Prefix_file_name = OUTPUT_PREFIX.replace(" ", "_").replace("/", "_")
OUTPUT_FILENAME = f'{Prefix_file_name}_{datetime.now(timezone.utc).strftime("%Y-%m-%d %H_%M_%S(UTC)")}.csv'

# Create a session to reuse HTTP connections
session = requests.Session()

def get_zones(api_key, account_name, page, per_page):
    """Fetch zones for the specified account."""
    url = "https://api.cloudflare.com/client/v4/zones"
    headers = {"Authorization": f"Bearer {api_key}"}
    params = {"page": page, "per_page": per_page}
    
    retries = 3
    for _ in range(retries):
        response = session.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            if data['success'] and data['result']:
                return [zone for zone in data['result'] if zone['account']['name'] == account_name]
        time.sleep(1)
    return []

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
    
    # Fetch all zones
    print("Fetching zones...")
    while True:
        zones = get_zones(API_KEY, ACCOUNT_NAME, page, per_page)
        if zones:
            all_zones.extend(zones)
            page += 1
        else:
            break

    print(f"Total zones fetched: {len(all_zones)}")

    # Use ThreadPoolExecutor to fetch DNS records in parallel
    dns_data = []
    print("Fetching DNS records...")
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_zone = {executor.submit(fetch_zone_data, zone, API_KEY): zone for zone in all_zones}
        for future in as_completed(future_to_zone):
            try:
                dns_data.extend(future.result())
            except Exception as e:
                print(f"Error processing zone: {e}")

    # Write results to CSV
    print(f"Writing data to {OUTPUT_FILENAME}...")
    write_to_csv(dns_data, OUTPUT_FILENAME)
    print("Done!")
