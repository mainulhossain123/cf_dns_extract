# 🔍 Cloudflare DNS Records Export Tool

This Python script retrieves all DNS records from your Cloudflare account, filtered by Account Name, and saves them into a CSV file. It uses parallel processing to speed up DNS record collection and includes built-in support for containerized environments (e.g., Docker).

---
## 🚀 Features
*✅ Authenticates using a Cloudflare API token (via environment variable)
*🔍 Filters zones by your Cloudflare Account Name
*📄 Exports DNS records (A, CNAME, MX, TXT, etc.) into a clean CSV format
*⚡ Fast DNS record fetching using ThreadPoolExecutor
*📁 Compatible with containerized environments (e.g., output defaults to /app)
*🔄 Handles pagination for large Cloudflare accounts
---

## 🧠 Requirements
* Python 3.7+
*Cloudflare API token with at least Zone.Read and DNS.Read permissions
*Installed Python packages: requests

Install dependencies:
```bash
pip install requests
```

## 🔐 Environment Variables

| Variable                | Required   | Description
|-------------------------|----------------------------------------
| `API_KEY`               | ✅        |  Your Cloudflare API token
| `ACCOUNT_NAME`          | ✅        |  Your Cloudflare account name     
| `OUTPUT_FIELD_PREFIX`   | ✅        |  Prefix for the output CSV file (e.g., CF_DNS)      
| `OUTPUT_DIR`            | ❌        |  Output directory for the CSV file (default: /app)

Set environment variables (example on Linux/macOS):
```bash
export API_KEY=your_cloudflare_token
export ACCOUNT_NAME="Your Corp Name"
export OUTPUT_FILENAME_PREFIX=CF_DNS_Export
```

## 🧪 Example Usage
Once your environment is set up:
```bash
python export_dns_records.py
```
Sample Output:
```swift
Output file will be saved to: /app/CF_DNS_Export.csv
Fetching zones...
Fetched page 1, 12 matching zones
Total zones fetched: 12
Fetching DNS records...
Writing data to /app/CF_DNS_Export.csv...
Done!
```

## 🗃️ Output
The output is a CSV file structured as follows:

|  Zone Name  |    Hostname      | DNS Type |     DNS Value    |
| example.com | www.example.com  |     A    |     192.0.2.1    |
| example.com | mail.example.com |     MX   | mail.example.com |


## 💡 Notes
* The script uses pagination to fetch zones in chunks of 100.
* If the OUTPUT_FILENAME_PREFIX is not provided via env, the script will prompt you to enter it.
* It automatically sanitizes the filename (e.g., removes spaces and slashes).\

##🐳 Docker Compatibility
If you're using this script inside a Docker container:
  * Make sure /app exists and is mounted as a volume.
  * The default output directory will be /app.\

## ❓Troubleshooting
* No zones returned: Make sure your ACCOUNT_NAME matches exactly what's shown in the Cloudflare dashboard.
* Empty CSV: Your API token might lack Zone and DNS permissions.

## 🤝 Contributing
Pull requests are welcome. For major changes:
* Fork the repo
* Create a feature branch
* Test your changes
* ubmit a PR with context

## 📝 License
This project is licensed under the MIT License

## 📬 Contact
For issues, questions, or feature requests, please contact:
Author: Mainul Hossain
Email: hossainmainul83@gmail.com
