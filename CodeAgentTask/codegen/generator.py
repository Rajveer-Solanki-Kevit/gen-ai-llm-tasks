from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

def generate_code(prompt: str) -> str:
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful code generator."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )
    return resp.choices[0].message.content
