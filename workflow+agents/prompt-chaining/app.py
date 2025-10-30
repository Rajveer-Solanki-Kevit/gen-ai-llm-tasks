from typing_extensions import TypedDict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
import os
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model="gpt-4o-mini")

class InputData(TypedDict):
    topic: str
    joke: str
    improved_joke: str
    final_joke: str
    

def generate_joke(input: InputData):
    msg = llm.invoke(f"Write a short joke about {input['topic']}")
    return {"joke": msg.content}


def check_punchline(state: InputData):
    if "?" in state["joke"] or "!" in state["joke"]:
        return "Pass"
    return "Fail"


def improve_joke(input: InputData):
    msg = llm.invoke(
        f"Improve the following joke to make it funnier: {input['joke']}"
    )
    return {"improved_joke": msg.content}


def finalize_joke(input: InputData):
    msg = llm.invoke(
        f"Finalize the following joke: {input['improved_joke']}"
    )
    return {"final_joke": msg.content}


workflow = StateGraph(InputData)

workflow.add_node("generate_joke", generate_joke)
workflow.add_node("improve_joke", improve_joke)
workflow.add_node("finalize_joke", finalize_joke)

workflow.add_edge(START, "generate_joke")
workflow.add_conditional_edges(
    "generate_joke", check_punchline, {"Fail": "improve_joke", "Pass": END}
)
workflow.add_edge("improve_joke", "finalize_joke")
workflow.add_edge("finalize_joke", END)

chain = workflow.compile()

state = chain.invoke({"topic": "cats"})
print("Initial joke:")
print(state["joke"])
print("\n--- --- ---\n")
if "improved_joke" in state:
    print("Improved joke:")
    print(state["improved_joke"])
    print("\n--- --- ---\n")

    print("Final joke:")
    print(state["final_joke"])
else:
    print("Joke failed - no punchline detected!")
