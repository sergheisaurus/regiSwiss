import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import sys

# Load the JSON file with company data
with open("extracted_data.json", "r", encoding="utf-8") as file:
    companies = json.load(file)

# Base URL for company details
BASE_URL = "https://hrc.ne.ch/hrcintapp/companyReport.action?lang=FR&companyOfsUid="
SUFFIX = "&showHeader=false&showBookmark=false"

# List to store extracted data
final_data = []

# Iterate over companies and scrape data
for index, company in enumerate(companies):
    uid = company["company_uid"]
    url = BASE_URL + uid + SUFFIX
    sys.stdout.write(f"\rScraping company {index + 1} / {len(companies)}")
    sys.stdout.flush()

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"\nError fetching {url}: {e}")
        continue

    soup = BeautifulSoup(response.text, "html.parser")
    admin_section = soup.find("a", id="adm")

    admin_entries = []
    if admin_section:
        table = admin_section.find_next("table")
        if table:
            rows = table.find_all("tr")[2:]  # Skip headers
            for row in rows:
                cols = row.find_all("td")
                if len(cols) >= 2:
                    full_name = cols[0].text.strip()
                    role = cols[1].text.strip()

                    # Split the name into three parts: Name, Origin, Domicile
                    name_parts = [part.strip() for part in full_name.split(",")]
                    name = name_parts[0] if len(name_parts) > 0 else ""
                    origin = name_parts[1] if len(name_parts) > 1 else ""
                    domicile = name_parts[2] if len(name_parts) > 2 else ""

                    admin_entries.append(
                        {
                            "name": name,
                            "origin": origin,
                            "domicile": domicile,
                            "role": role,
                        }
                    )

    company_entry = company.copy()
    company_entry["administrators"] = admin_entries
    final_data.append(company_entry)


# Save data to JSON
with open("final_data.json", "w", encoding="utf-8") as outfile:
    json.dump(final_data, outfile, indent=4, ensure_ascii=False)

print("\nScraping complete. Data saved to final_data.json")
