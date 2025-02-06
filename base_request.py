import requests

url = "https://shab.ch/api/v1/publications"

params = {
    "allowRubricSelection": "true",
    "cantons": "VS,NE,FR,GE,VD",
    "includeContent": "False",
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
    print("Success!")
    data = response.json()
    print(data)
else:
    print(f"Request failed with status code {response.status_code}")

with open("data.json", "w") as f:
    f.write(response.text)
