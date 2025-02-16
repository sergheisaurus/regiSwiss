from bs4 import BeautifulSoup
import requests

def extract_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def main():
    url = "https://www.uid.admin.ch/Detail.aspx?uid_id=CHE-411.469.047&lang=fr"
    html = extract_html(url)
    if html:
        soup = parse_html(html)
        print(soup.prettify())
    else:
        print("Failed to retrieve the webpage.")
    
    with open("output.html", "w") as file:
        file.write(soup.prettify())

if __name__ == "__main__":
    main()
