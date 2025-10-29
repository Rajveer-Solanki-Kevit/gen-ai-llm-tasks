import os
import json
import requests
from bs4 import BeautifulSoup
from typing import Any
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from langfuse import get_client

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
langfuse = get_client()

@st.cache_data(show_spinner=True)
def scrape_gdp_data():
    url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        st.error(f"Fail : {response.status_code}")
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


st.set_page_config(page_title="GDP Assistant", layout="wide")
st.title("Global GDP Chat Assistant")
st.markdown("Ask any question about **world GDP data (2023–2025)** below")

with st.spinner("Scraping GDP data..."):
    gdp_data = scrape_gdp_data()
st.success("GDP data scraped and ready!")

context_info = (
    "You are a knowledgeable assistant that answers questions about global GDP "
    "based on IMF, World Bank, and UN data (2023–2025). "
    "You have structured data including countries, GDP figures, and references. "
    f"Here is your available context: {json.dumps(gdp_data)[:3000]}..."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Type your question about GDP...")

if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        ans_place = st.empty()
        text_given = ""

        with langfuse.start_as_current_observation(
            as_type="generation",
            name="gdp_chat_response",
            model="gpt-4o-mini",
            input=prompt,
            metadata={"topic": "GDP", "source": "Streamlit"}
        ) as gen:
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": context_info},
                        {"role": "user", "content": prompt},
                    ]
                )
                text_given = response.choices[0].message.content
                ans_place.markdown(text_given)
                gen.update(output=text_given, metadata={"status": "completed"})

            except Exception as e:
                gen.update(output=str(e), metadata={"status": "error"})
                st.error(f"Failed: {e}")

    st.session_state.messages.append({"role": "assistant", "content": text_given})

langfuse.flush()
