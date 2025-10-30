# gen-ai-llm-tasks — Repository Overview

A small collection of example projects demonstrating Gen-AI / LLM tasks.

This repository groups three independent example folders that each contain a focused sample project, requirements, and a small CLI or script entrypoint. Each folder has its own `README.md` with detailed setup and run instructions. The three subprojects are:

- `CodeAgentTask/` — code generation and testing utilities (generator + tester).
- `OpenAIAssistantTask/` — an assistant CLI and streamlit web both for working with the OpenAI API.
- `RAG-Task/` — a retrieval-augmented generation example and a small web entrypoint.
- `workflow+agents/` — langgraph workflow and agents demo.

## Quick repository layout

```
CodeAgentTask/
OpenAIAssistantTask/
RAG-Task/
workflow+agents/
README.md         
```

## Getting started (recommended)

These projects are intentionally isolated. I recommend creating a separate Python virtual environment for each subfolder to avoid dependency conflicts.

1. Clone the repository (if you haven't already):

```bash
# replace <repo-url> with your repository URL
git clone <repo-url>
cd "Gen-AI-LLM Tasks"
```

2. Pick a subproject and follow its README. Example (for `CodeAgentTask`):

```bash
cd CodeAgentTask
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp example.env .env    # then edit .env with any API keys
python cli_agent.py    # or python main_task.py
```

Repeat the same pattern for `OpenAIAssistantTask` and `RAG-Task` — each folder contains a `requirements.txt` and an `example.env`.

## Notes and tips

- Python: these projects assume Python 3.8+. Use the matching `python3.x` binary when creating venvs if needed.
- Environment variables: copy `example.env` to `.env` and fill in secrets (e.g. `OPENAI_API_KEY`). Some scripts read `.env`; otherwise export variables in your shell using export.

## Where to find details

- `CodeAgentTask/README.md` — setup, per-folder venv, generator/tester usage.
- `OpenAIAssistantTask/README.md` — assistant CLI, scraping helper, environment setup.
- `RAG-Task/README.md` — RAG, running `app.py`, and env notes.
- `workflow+agents/README.md` — RAG, running `app.py`, and env notes.

Last updated: 2025-10-30
