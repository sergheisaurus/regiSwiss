import json
import requests
from bs4 import BeautifulSoup
import sys

# Load the JSON file with company data
with open("final_data.json", "r", encoding="utf-8") as file:
    companies = json.load(file)

# Base URL for VAT details
BASE_URL = "https://www.uid.admin.ch/Detail.aspx?uid_id="
SUFFIX = "&lang=fr"

# Iterate over companies and scrape VAT data
for index, company in enumerate(companies):
    uid = company["company_uid"]
    url = BASE_URL + uid + SUFFIX
    sys.stdout.write(f"\rChecking VAT status for company {index + 1} / {len(companies)}")
    sys.stdout.flush()

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"\nError fetching {url}: {e}")
        continue

    soup = BeautifulSoup(response.text, "html.parser")
    vat_section = soup.find("div", id="cphContent_pnlVAT")

    vat_status = "Not Found"
    vat_date = "N/A"

    if vat_section:
        status_label = vat_section.find("label", id="cphContent_ctl49_lbl_ddlVATStatus")
        status_value = (
            status_label.find_next("div").text.strip() if status_label else "Not Found"
        )

        if status_value.lower() == "actif":
            vat_status = "Active"
            date_label = vat_section.find(
                "label", id="cphContent_ctl51_lbl_datVATBegin"
            )
            date_value = (
                date_label.find_next("div").text.strip() if date_label else "N/A"
            )
            vat_date = date_value
        else:
            vat_status = "Inactive"

    company["VAT_status"] = vat_status
    company["VAT_start_date"] = vat_date

# Save updated data to JSON
with open("final_data_vat.json", "w", encoding="utf-8") as outfile:
    json.dump(companies, outfile, indent=4, ensure_ascii=False)

print("\nVAT check complete. Data saved to final_data_vat.json")
