import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from scraping_script import scrape_gdp_data

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_gdp_questions():
    if not os.path.exists("gdp_all_data.json"):
        print("Scraping fresh data...")
        gdp_data = scrape_gdp_data()
    else:
        with open("gdp_all_data.json", "r", encoding="utf-8") as f:
            gdp_data = json.load(f)

    system_message = {
        "role": "system",
        "content": (
            "You are an assistant knowledgeable about global GDP data. "
            "You have access to a dataset of GDP by country from Wikipedia. "
            f"Here is the data:\n\n{json.dumps(gdp_data, indent=2)}"
        )
    }

    print("\nAsk questions about global GDP (type 'exit' to quit)\n")

    while True:
        user_query = input("You: ").strip()
        if user_query.lower() == "exit":
            break

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[system_message, {"role": "user", "content": user_query}],
                temperature=0.3
            )

            print("Bot:", response.choices[0].message.content)
            print("-" * 150)

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    ask_gdp_questions()
