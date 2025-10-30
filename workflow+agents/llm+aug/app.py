import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model="gpt-4o-mini")

class SearchQuery(BaseModel):
    search_query: str = Field(None, description="Query that is optimized web search.")
    justification: str = Field(
        None, description="Why this query is relevant to the user's request."
    )

structured_llm = llm.with_structured_output(SearchQuery)

output = structured_llm.invoke(
    "Provide a search query to find recent advancements in renewable energy technologies and justify why this query is relevant."
)
# print(output)

def multiply(a: int, b: int) -> int:
    return a * b

llm_with_tools = llm.bind_tools([multiply])

res = llm_with_tools.invoke(
    "What is the product of 12 and 15? Use the multiply tool to calculate."
)
print(res.tool_calls)
