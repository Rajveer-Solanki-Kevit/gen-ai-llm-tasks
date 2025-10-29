from typing import Any
import json
import requests
from bs4 import BeautifulSoup

def scrape_gdp_data():
    url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {}

    soup = BeautifulSoup(response.content, "html.parser")

    def fetch_gdp_intro() -> str:
        for p in soup.select("#mw-content-text p")[:3]:
            text = p.get_text(strip=True)
            if text:
                return text
        return ""

    def fetch_gdp_table() -> list[dict]:
        table = soup.find("table", class_="wikitable")
        if not table:
            return []
        headers = [th.get_text(strip=True) for th in table.find("tr").find_all("th")]
        rows = table.find_all("tr")[1:]
        gdp_data = []
        for row in rows:
            cells = row.find_all(["td", "th"])
            if len(cells) == len(headers):
                record = {headers[i]: cells[i].get_text(strip=True) for i in range(len(headers))}
                gdp_data.append(record)
        return gdp_data

    def fetch_all_links() -> list[Any]:
        links = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.startswith("/wiki/") and not href.startswith("/wiki/Special:") and not href.startswith("/wiki/Help:"):
                full_url = "https://en.wikipedia.org" + href
                links.append(full_url)
        return links

    all_data = {
        "intro": fetch_gdp_intro(),
        "gdp_table": fetch_gdp_table(),
        "all_links": fetch_all_links()
    }

    with open("gdp_all_data.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)

    return all_data