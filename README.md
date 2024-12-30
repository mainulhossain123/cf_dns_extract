# Cloudflare Zone DNS Extraction

This Python script is designed to extract DNS records from Cloudflare zones and save the extracted data into a CSV file. The script fetches zone and DNS record data via the Cloudflare API and organizes it in a structured format.

* PLEASE NOTE: The script is written to be run inside a docker contaimer image therefore all user inputs need to be placed via environment variables.

## Prerequisites

Before running the script, make sure you have the following:

* **Docker**: This script is designed to run inside a Docker container, making it easy to deploy without worrying about dependencies. You can install Docker from [here](https://www.docker.com/products/docker-desktop).
* **Cloudflare API Key**: Ensure you have a Cloudflare account with an active API key. The API key should have permission to access your zones. You can generate an API key in your Cloudflare account settings.
* ## Prerequisites 
* **Python 3.12 or higher**. Download it from https://www.python.org/downloads/
* **IDE** - I personally used Visual Studio Code but it is upto your preference.
* **Libraries - requests**: Run in Terminal of enviornment or in command prompt **pip install requests**
* **Libraries - datetime**: Run in Terminal of enviornment or in command prompt **pip install datetime**
* **Libraries - csv**: Run in Terminal of enviornment or in command prompt **pip install csv**
* **Libraries - concurrent.futures**: should be part of Python package, used for multi-threading

## Languages, Frameworks and API calls used in the script
The Script uses the following:

- *[Python 3.12.3](https://www.python.org/downloads/release/python-3123/)* as the primary Programming Language.
- *[Visual Studio Code](https://code.visualstudio.com/download)* as the IDE.
- *[Cloudflare V4 DNS records endpoint](https://developers.cloudflare.com/api/resources/dns/subresources/records/methods/create/)* as the secondary endpoint for WAF Authorization header.
- *[Cloudflare V4 Zone list Check](https://developers.cloudflare.com/api/operations/zones-get)* as the primary endpoint for zone Authorization header.
- *[Requests Module](https://pypi.org/project/requests/)* allows us to make HTTP/1.1 request calls.
- *[Datetime Module](https://docs.python.org/3/library/datetime.html)* for usage of current date and time on file naming schemes
- *[Time Module](https://docs.python.org/3/library/time.html)* primarily used in the script to produce delays in the frequency of each request in case of rate-limiting issues
- *[CSV Module](https://docs.python.org/3/library/csv.html)* allows us to write or read CSV files, in this case write all retrieved data to a CSV file.
- *[Concurrent Futures Threadpool Executor Module](https://docs.python.org/3/library/concurrent.futures.html)* allows us to process data in parrallelalism/multi-threading.

## Legal
* This code is in no way affiliated with, authorized, maintained, sponsored or endorsed by Cloudflare or any of its affiliates or subsidiaries. This is an independent and unofficial software. Use at your own risk. Commercial use of this code/repo is strictly prohibited.

**Run the Docker Container:**
 Once the Docker image is available, you can run the script inside the container with the following command. Make sure to replace the placeholders with your actual API key, account name, and desired output directory.
 
   ```bash
    docker run -it --rm \
        -v (Enter Your File Path):/app \
        -e API_KEY='YOUR_API_KEY' \
        -e ACCOUNT_NAME='CF_ACCOUNT_NAME' \
        -e OUTPUT_FILENAME_PREFIX='SET_YOUR_FILE_NAME' \
        -e OUTPUT_DIR='/app' \
        (Load in Your Python Enviornment Container Image) \
        sh -c "curl -O https://raw.githubusercontent.com/mainulhossain123/cf_dns_extract/refs/heads/main/CF_Zone_DNS_Extraction.py && python CF_Zone_DNS_Extraction.py"
   ```
  
  **Explanation of Parameters:**
   - `-v (Enter Your File Path):/app`: This maps the local chosen file path folder on your computer, (Windoes, Linux, MAC) machine to the `/app` directory inside the container, which is the default output location for the CSV file.
   - `-e API_KEY='YOUR_API_KEY'`: Replace `'YOUR_API_KEY'` with your Cloudflare API Bearer Token.
   - `-e ACCOUNT_NAME='CF_ACCOUNT_NAME'`: Replace `'CF_ACCOUNT_NAME'` with your Cloudflare account name.
   - `-e OUTPUT_FILENAME_PREFIX='SET_YOUR_FILE_NAME'`: Provide the file name prefix that will be used to generate the output CSV file.
   - `-e OUTPUT_DIR='/app'`: Define the directory inside the container where the output file will be saved. By default, it's set to `/app`, but you can modify this if needed.

**Writing to CSV**
The data is saved into a CSV file with the specified output filename. The file will contain the following columns:

Zone Name: The name of the Cloudflare zone.
Hostname: The hostname associated with the DNS record.
DNS Type: The type of DNS record (e.g., A, CNAME, etc.).
DNS Value: The value associated with the DNS record (e.g., IP address or target hostname).

```python
def write_to_csv(data, filename):
    """Write collected data to a CSV file."""
    with open(filename, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        # Write header
        csv_writer.writerow(["Zone Name", "Hostname", "DNS Type", "DNS Value"])
        # Write data rows
        csv_writer.writerows(data)
```
