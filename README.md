# cf_dns_extract

docker run -it --rm -v (Enter file path here):/app -e API_KEY='YOUR_API_KEY' -e ACCOUNT_NAME='CF_ACCOUNT_NAME' -e OUTPUT_FILENAME_PREFIX='SET_YOUR_FILE_NAME' -e OUTPUT_DIR='/app' mainul123/pythonenv:1.0.0 sh -c "curl -O https://raw.githubusercontent.com/mainulhossain123/cf_dns_extract/refs/heads/main/CF_Zone_DNS_Extraction.py && python CF_Zone_DNS_Extraction.py"
