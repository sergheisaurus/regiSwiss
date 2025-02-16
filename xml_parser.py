import os
import xml.etree.ElementTree as ET
import pandas as pd
import json

# Define the folder containing XML files
FOLDER_PATH = "shab_publications_xml"


# Function to extract required data from XML file
def extract_data_from_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Extracting elements based on verified structure
    publication_date = root.find(".//meta/publicationDate")
    canton = root.find(".//meta/cantons")
    company_name = root.find(".//content/commonsNew/company/name")
    company_uid = root.find(".//content/commonsNew/company/uid")

    address_element = root.find(".//content/commonsNew/company/address")
    if address_element is not None:
        street = address_element.find("street")
        house_number = address_element.find("houseNumber")
        zip_code = address_element.find("swissZipCode")
        town = address_element.find("town")
        address = f"{street.text if street is not None else ''} {house_number.text if house_number is not None else ''}, {zip_code.text if zip_code is not None else ''} {town.text if town is not None else ''}".strip()
    else:
        address = None

    return {
        "publication_date": publication_date.text
        if publication_date is not None
        else None,
        "cantion": canton.text if canton is not None else None,
        "company_name": company_name.text if company_name is not None else None,
        "company_uid": company_uid.text if company_uid is not None else None,
        "address": address,
    }


# Process all XML files in the folder
data = []
for file_name in os.listdir(FOLDER_PATH):
    if file_name.endswith(".xml"):
        file_path = os.path.join(FOLDER_PATH, file_name)
        data.append(extract_data_from_xml(file_path))

# Convert to DataFrame and save results as JSON
df = pd.DataFrame(data)
json_output_path = "extracted_data.json"
df.to_json(json_output_path, orient="records", indent=4)
print(f"Data saved to {json_output_path}")
