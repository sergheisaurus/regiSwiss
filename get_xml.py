import requests
import os
import sys
import time

def fetch_publications():
    url = "https://shab.ch/api/v1/publications"
    params = {
        "allowRubricSelection": "true",
        "cantons": "NE",
        "includeContent": "false",
        "pageRequest.page": 0,
        "pageRequest.size": 100, # max value is 3000
        "publicationDate.end": "2024-03-01",
        "publicationDate.start": "2023-01-01",
        "publicationStates": "PUBLISHED",
        "searchPeriod": "CUSTOM",
        "subRubrics": "HR01",
    }

    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0",
    }

    response = requests.get(url, headers=headers, params=params, timeout=10)

    if response.status_code == 200:
        return response.json().get("content", [])
    else:
        print(f"Request failed with status code {response.status_code}")
        return []

def download_xml(pub_id):
    xml_url = f"https://shab.ch/api/v1/publications/{pub_id}/xml"
    headers = {
        "Accept": "application/xml",
        "User-Agent": "Mozilla/5.0",
    }

    response = requests.get(xml_url, headers=headers)

    if response.status_code == 200:
        folder_name = "shab_publications_xml"
        os.makedirs(folder_name, exist_ok=True)
        file_path = os.path.join(folder_name, f"{pub_id}.xml")

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(response.text)
    else:
        print(f"Failed to download XML for publication ID {pub_id}. Status code: {response.status_code}")

def main():
    publications = fetch_publications()
    saved_count = 0

    for publication in publications:
        pub_id = publication.get("meta", {}).get("id")
        if pub_id:
            download_xml(pub_id)
            saved_count += 1
            # Print live counter
            sys.stdout.write(f"\rTotal companies saved: {saved_count} / {len(publications)}")
            sys.stdout.flush()

    print()  # Move to the next line after the loop

if __name__ == "__main__":
    main()
