import requests
import os


class Publication:
    def __init__(
        self,
        pub_id,
        creation_date,
        update_date,
        rubric,
        sub_rubric,
        language,
        registration_office,
        publication_number,
        publication_state,
        publication_date,
        cantons,
        title,
    ):
        self.pub_id = pub_id
        self.creation_date = creation_date
        self.update_date = update_date
        self.rubric = rubric
        self.sub_rubric = sub_rubric
        self.language = language
        self.registration_office = registration_office
        self.publication_number = publication_number
        self.publication_state = publication_state
        self.publication_date = publication_date
        self.cantons = cantons
        self.title = title

    def __repr__(self):
        return f"Publication({self.publication_number}, {self.title.get('fr', 'No Title')}, {self.cantons})"


def fetch_and_store_publications():
    url = "https://shab.ch/api/v1/publications"
    params = {
        "allowRubricSelection": "true",
        "cantons": "VS,NE,FR,GE,VD",
        "includeContent": "false",
        "pageRequest.page": 0,
        "pageRequest.size": 100,
        "publicationDate.end": "2025-01-05",
        "publicationDate.start": "2025-01-01",
        "publicationStates": "PUBLISHED",
        "searchPeriod": "CUSTOM",
        "subRubrics": "HR01",
    }

    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0",
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        publications = []

        for entry in data.get("content", []):
            meta = entry.get("meta", {})

            publication = Publication(
                pub_id=meta.get("id"),
                creation_date=meta.get("creationDate"),
                update_date=meta.get("updateDate"),
                rubric=meta.get("rubric"),
                sub_rubric=meta.get("subRubric"),
                language=meta.get("language"),
                registration_office=meta.get("registrationOffice", {}).get(
                    "displayName"
                ),
                publication_number=meta.get("publicationNumber"),
                publication_state=meta.get("publicationState"),
                publication_date=meta.get("publicationDate"),
                cantons=meta.get("cantons", []),
                title=meta.get("title", {}),
            )

            publications.append(publication)

            # Download the XML file for each publication
            download_publication_xml(publication.pub_id)

        return publications
    else:
        print(f"Request failed with status code {response.status_code}")
        return []


def download_publication_xml(pub_id):
    xml_url = f"https://shab.ch/api/v1/publications/{pub_id}/xml"
    headers = {
        "Accept": "application/xml",
        "User-Agent": "Mozilla/5.0",
    }

    response = requests.get(xml_url, headers=headers)

    if response.status_code == 200:
        xml_content = response.text
        save_xml_file(pub_id, xml_content)
    else:
        print(
            f"Failed to download XML for publication ID {pub_id}. Status code: {response.status_code}"
        )


def save_xml_file(pub_id, xml_content):
    folder_name = "shab_publications_xml"
    os.makedirs(folder_name, exist_ok=True)

    file_path = os.path.join(folder_name, f"{pub_id}.xml")

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(xml_content)

    print(f"XML saved: {file_path}")


# Fetch and store publications and their XML files
publications_list = fetch_and_store_publications()

# Print the stored objects
for pub in publications_list:
    print(pub)
