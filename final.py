import json
import pandas as pd

# Load the JSON file with VAT data
with open("final_data_vat.json", "r", encoding="utf-8") as file:
    companies = json.load(file)

# Flatten the data for CSV conversion
rows = []
for company in companies:
    base_info = {
        "Company Name": company.get("company_name", ""),
        "Company UID": company.get("company_uid", ""),
        "Publication Date": company.get("publication_date", ""),
        "Canton": company.get("cantion", ""),
        "Address": company.get("address", ""),
        "VAT Status": company.get("VAT_status", ""),
        "VAT Start Date": company.get("VAT_start_date", ""),
    }

    for admin in company.get("administrators", []):
        row = base_info.copy()
        row.update(
            {
                "Admin Name": admin.get("name", ""),
                "Admin Origin": admin.get("origin", ""),
                "Admin Domicile": admin.get("domicile", ""),
                "Admin Role": admin.get("role", ""),
            }
        )
        rows.append(row)

# Create a DataFrame and save to CSV
csv_filename = "final_data_vat.csv"
df = pd.DataFrame(rows)
df.to_csv(csv_filename, index=False, encoding="utf-8-sig")

print(f"Conversion complete. Data saved to {csv_filename}")
